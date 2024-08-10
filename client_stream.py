import sys

from openai import OpenAI

client = OpenAI(api_key="fake-api-key", base_url="http://localhost:8000")

res = client.chat.completions.create(
    model="gemini-1.5-flash",
    messages=[{"role": "user", "content": "Tell me a joke"}],
    stream=True,
)

for chunk in res:
    sys.stdout.write(chunk.choices[0].delta.content or "")
    sys.stdout.flush()
