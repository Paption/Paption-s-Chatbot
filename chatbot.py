from ollama import chat

MODEL = "qwen3.5:0.8b"

#conversation history.
messages = [
    {
        "role": "system",
        "content": (
            "You are Paption, a friendly and helpful chatbot. "
            "Answer clearly and keep responses concise."
        ),
    }
]


def send_message(user_input):
    """
    Send a message to Ollama, stream the response,
    and save the conversation only after success.
    """

    # temporary conversation history .
    request_messages = messages + [
        {
            "role": "user",
            "content": user_input,
        }
    ]

    response_text = ""

    try:
        print("Bot: ", end="", flush=True)

        # Generate a streaming response.
        stream = chat(
            model=MODEL,
            messages=request_messages,
            stream=True,
        )

        for chunk in stream:
            text = chunk.message.content or ""
            print(text, end="", flush=True)
            response_text += text

        #response
        if not response_text.strip():
            print("\nThe model returned an empty response.\n")
            return

        print("\n")

        # Save the conversation
        messages.append({
            "role": "user",
            "content": user_input,
        })

        messages.append({
            "role": "assistant",
            "content": response_text,
        })

    except Exception as error:
        print(f"\n\nPaption is experiencing a problem: {error}")
        print("Please check that Ollama is installed and running.")
        print("Your conversation history has not been changed.\n")


def main():
    """Run the Paption Bot terminal chatbot."""

    print("Paption Bot is ready!")
    print(f"Model: {MODEL}")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_input = input("You: ").strip()

        except (KeyboardInterrupt, EOFError):
            print("\nBot: Goodbye!")
            break

        if user_input.lower() in ("exit", "quit"):
            print("Bot: Goodbye!")
            break

        if not user_input:
            continue

        send_message(user_input)


if __name__ == "__main__":
    main()
