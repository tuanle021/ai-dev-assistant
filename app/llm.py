import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_llm(question: str, context: str) -> str:

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a technical documentation assistant.

Use ONLY the provided context.

Context:
{context}

Question:
{question}
"""

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(GROQ_URL, json=payload, headers=headers)

    result = response.json()

    # 🔥 IMPORTANT: handle API errors cleanly
    if response.status_code != 200:
        raise Exception(f"Groq API error: {result}")

    if "choices" not in result:
        raise Exception(f"Unexpected response: {result}")

    return result["choices"][0]["message"]["content"]