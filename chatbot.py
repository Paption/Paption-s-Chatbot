
from ollama import chat

MODEL = "qwen3.5:0.8b"

messages = [
    {
        "role": "system",
        "content": (
            "You are a friendly, helpful chatbot. "
            "Answer clearly and keep responses concise."
        ),
    }
]

print("Paption bot is ready!")
print("Type 'exit' to stop.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ("exit", "quit"):
        print("Bot: Goodbye!")
        break

    if not user_input:
        continue

    messages.append({
        "role": "user",
        "content": user_input,
    })

    try:
        print("Bot: ", end="", flush=True)

        response_text = ""

        # Generate a streaming response
        stream = chat(
            model=MODEL,
            messages=messages,
            stream=True,
        )

        for chunk in stream:
            text = chunk.message.content or ""
            print(text, end="", flush=True)
            response_text += text

        print("\n")
#create a line brake
        messages.append({
            "role": "assistant",
            "content": response_text,
        })

    except Exception as error:
        print(f"\nError: {error}")
        print("Check that Ollama is installed and running.\n")
