from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:8001/v1")
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user", "content": "Write a short story on James."}],
    max_tokens=2048,
)
print(response.choices[0].message.content)