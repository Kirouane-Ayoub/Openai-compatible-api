from openai import OpenAI

client = OpenAI(api_key="fake-api-key", base_url="http://localhost:8000")

res = client.chat.completions.create(
    model="gemini-1.5-flash",
    messages=[{"role": "user", "content": "Tell me a joke"}],
    stream=False,
)

print(res.choices[0].message.content)
