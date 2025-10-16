import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_KEY")
print("Using key:", SERPER_API_KEY[:8] + "..." if SERPER_API_KEY else " No key found")

url = "https://google.serper.dev/search"
headers = {
    "X-API-KEY": SERPER_API_KEY,
    "Content-Type": "application/json"
}
data = {"q": "best laptops 2025", "num": 3}

response = requests.post(url, headers=headers, json=data)
print("Status code:", response.status_code)
print("Response text:", response.text)
