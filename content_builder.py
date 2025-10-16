import os
import requests
from dotenv import load_dotenv

load_dotenv()


SERPER_API_KEY = os.getenv('SERPER_KEY')
SERPER_URL = "https://google.serper.dev/search"

def fetching_results(query):
    headers= {
        "X-API-Key" : SERPER_API_KEY,
        "Content-Type": 'application/json'
    }

    data = {'q':query, 'num':5}
    response = requests.post(SERPER_URL, headers= headers , json = data)
    response.raise_for_status()
    results = response.json()
    return results.get('organic', [])


def gen_results(results, cluster_name):

    if not results:
        return f"no results found {cluster_name}"
    
    headline = [r.get("title") for r in results if r.get('title')]
    descript = [r.get('desc') for r in results if r.get('desc')]

    outline = f"content for {cluster_name}:\n"
    outline += "1. Introduction\n"
    outline += f"Overview of {cluster_name}:\n"
    outline += "2. Key Pointers:\n"

    for head in headline[:5]:
        outline += f" {head}\n"

    outline += "3. contents\n"
    for dsp in descript[:3]:
        outline += f"{dsp}\n"

    
    outline += "4. Conclusion\n"

    return outline


def gen_clusters(clusters: dict):

    outlines = {}
    for name , keyword in sorted(clusters.items()):
        q = ", ".join(keyword[:3])
        res = fetching_results(q)
        outlines[name] =  gen_results(res, name)

    return outlines


def get_content(keyword: str):

    results = fetching_results(keyword)
    return gen_results(results, keyword)
    
