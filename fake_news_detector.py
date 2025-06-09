import requests
import json
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")

GROQ_MODEL = "llama-3.3-70b-versatile"

def detect_fake_news(news_content):
    if not GROQ_API_KEY:
        raise ValueError("Please set the GROQ_API_KEY before using this function.")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    You are a Fake News Detection AI.
    Return only strict JSON. Do NOT include any explanation or text outside the JSON.

    Classify the news below as "Fake" or "Real", explain why, and give a confidence percentage.

    Format:
    {{
    "verdict": "Fake" or "Real",
    "confidence": 0-100,
    "reason": "Brief explanation"
    }}

    News:
    \"\"\"{news_content}\"\"\"
    """

    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a fake news classifier AI."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        try:
            content = response.json()["choices"][0]["message"]["content"]
            return json.loads(content)
        except Exception as e:
            return {
                "verdict": "Error",
                "confidence": 0,
                "reason": f"Parse error: {str(e)}\nRaw: {content}"
            }
    else:
        return {
            "verdict": "Error",
            "confidence": 0,
            "reason": f"API error: {response.status_code} - {response.text}"
        }
