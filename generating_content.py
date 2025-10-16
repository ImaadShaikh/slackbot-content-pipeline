import requests
import random

templates = [
    " Share 3 quick tips about {}",
    "Write a LinkedIn post explaining why {} matters in 2025",
    "Summarize key trends in {}",
    "Post a short data insight thread on {}",
]

def rule_based_idea(cluster_name, keywords):
    topic = random.choice(keywords) if keywords else cluster_name
    return random.choice(templates).format(topic)

def idea_generator(cluster_name, keywords):
    topic = ", ".join(keywords[:3]) or cluster_name
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": f"You are a creative strategist. Generate one short, catchy post idea related to {topic}.",
                "stream": False
            },
            timeout=60
        )
        data = response.json()
        return data.get("response", "").strip()

    except Exception as e:
        print(f"LLM failed, using failsafe: {e}")
        return rule_based_idea(cluster_name, keywords)

def generating_idea_via_clusters(clusters: dict):
    ideas = {}
    for name, words in clusters.items():
        ideas[name] = idea_generator(name, words)
    return ideas
