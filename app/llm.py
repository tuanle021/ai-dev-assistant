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

Answer the user's question using ONLY information explicitly present in the provided context.

Rules:
1. Do not use outside knowledge.
2. Do not make assumptions.
3. Do not infer information that is not stated in the context.
4. If the answer cannot be found in the context, respond exactly with:

"I cannot find this information in the provided documentation."

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
    print("\n===== CONTEXT SENT TO LLM =====")
    print(context)
    print("===== END CONTEXT =====\n")
    response = requests.post(GROQ_URL, json=payload, headers=headers)

    result = response.json()

    # 🔥 IMPORTANT: handle API errors cleanly
    if response.status_code != 200:
        raise Exception(f"Groq API error: {result}")

    if "choices" not in result:
        raise Exception(f"Unexpected response: {result}")

    return result["choices"][0]["message"]["content"]