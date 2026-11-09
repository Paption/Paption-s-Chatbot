from ollama import chat

# Model configuration
MODEL = "qwen3.5:0.8b"

print("Testing Qwen without thinking...")

# Start streaming response
response = chat(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": "Say hello in one sentence."
        }
    ],
    stream=True,
    think=False
)

# Collect the response
answer = ""

for chunk in response:

    content = chunk.message.content or ""

    print(content, end="", flush=True)

    answer += content

print("\n\nFinal answer:")
print(answer)