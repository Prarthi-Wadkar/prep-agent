from dotenv import load_dotenv
load_dotenv()

import os
import requests

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    print("GROQ_API_KEY not found - check your .env file")
else:
    r = requests.get(
        "https://api.groq.com/openai/v1/models",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    if r.status_code != 200:
        print(f"Request failed: {r.status_code}")
        print(r.text)
    else:
        for m in r.json()["data"]:
            print(m["id"])