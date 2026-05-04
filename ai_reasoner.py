import requests

API_URL = "http://localhost:11434/api/generate"

# Replace this with the exact model name from `ollama list`
MODEL = "qwen:4b"

def explain_personalization(events, modules):
 prompt = f"""
You are an AI product analyst.

Given:
User events: {events}
Homepage modules: {modules}

Explain:
- Why these modules were chosen
- What assumptions are being made
- Risk of wrong personalization
- Confidence level (low/medium/high)

Be critical. Do not blindly justify.
"""

 response = requests.post(
  API_URL,
  json={
   "model": MODEL,
   "prompt": prompt,
   "stream": False,
   "options": {"temperature": 0.2}
  },
  timeout=120
 )

 response.raise_for_status()
 return response.json()["response"]