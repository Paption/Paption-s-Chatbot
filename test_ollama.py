
from ollama import chat
import time

print("Sending test message...")
start = time.time()

response = chat(
    model="qwen3.5:0.8b",
    messages=[
        {"role": "user", "content": "Reply with: Hello Leroy!"}
    ],
    stream=False,
)

print("Response:", response.message.content)
print("Time taken:", round(time.time() - start, 2), "seconds")
