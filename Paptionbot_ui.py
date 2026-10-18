
import threading
import customtkinter as ctk
from ollama import chat

# -----------------------------
# CONFIGURATION
# -----------------------------

MODEL = "qwen3.5:0.8b"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class PaptionBot(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Paption Bot")
        self.geometry("1000x700")
        self.minsize(600, 450)

        # Conversation history
        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are Paption Bot, a friendly and helpful AI "
                    "assistant. Answer clearly and concisely."
                ),
            }
        ]

        self.create_interface()

    def create_interface(self):

        # Header
        self.header = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=0,
            height=70,
        )
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        self.title_label = ctk.CTkLabel(
            self.header,
            text="PAPTION",
            font=("Arial", 24, "bold"),
            text_color="#111111",
        )
        self.title_label.pack(side="left", padx=25, pady=15)

        self.subtitle = ctk.CTkLabel(
            self.header,
            text="AI ASSISTANT",
            font=("Arial", 11),
            text_color="#777777",
        )
        self.subtitle.pack(side="left", padx=5, pady=20)

        # Chat area
        self.chat_area = ctk.CTkScrollableFrame(
            self,
            fg_color="#F5F5F5",
            corner_radius=0,
        )
        self.chat_area.pack(
            fill="both",
            expand=True,
            padx=0,
            pady=0,
        )

        # Welcome message
        self.add_message(
            "Paption",
            "Rada Rada! Welcome to Paption Bot. How can I help you today?",
        )

        # Input section
        self.input_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=0,
        )
        self.input_frame.pack(fill="x", padx=0, pady=0)

        self.user_input = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Message Paption...",
            height=45,
            font=("Arial", 14),
            fg_color="#F2F2F2",
            text_color="#111111",
            border_color="#DDDDDD",
        )
        self.user_input.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(20, 10),
            pady=15,
        )

        self.user_input.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="Send",
            width=80,
            height=45,
            fg_color="#111111",
            hover_color="#333333",
            text_color="#FFFFFF",
            command=self.send_message,
        )
        self.send_button.pack(
            side="right",
            padx=(0, 20),
            pady=15,
        )

        # Status
        self.status_label = ctk.CTkLabel(
            self,
            text="Powered by Ollama",
            font=("Arial", 10),
            text_color="#888888",
        )
        self.status_label.pack(pady=(0, 8))

    def add_message(self, sender, message):

        # Message container
        container = ctk.CTkFrame(
            self.chat_area,
            fg_color="transparent",
        )
        container.pack(fill="x", padx=15, pady=8)

        # Sender label
        sender_label = ctk.CTkLabel(
            container,
            text=sender,
            font=("Arial", 12, "bold"),
            text_color="#111111",
            anchor="w",
        )
        sender_label.pack(anchor="w", padx=5)

        # Message text
        message_label = ctk.CTkLabel(
            container,
            text=message,
            font=("Arial", 14),
            text_color="#222222",
            justify="left",
            anchor="w",
            wraplength=650,
        )
        message_label.pack(anchor="w", padx=5, pady=(3, 0))

        return message_label

    def send_message(self, event=None):

        user_text = self.user_input.get().strip()

        if not user_text:
            return "break"

        self.user_input.delete(0, "end")

        # Display the user's message
        self.add_message("You", user_text)

        # Add to conversation history
        self.messages.append({
            "role": "user",
            "content": user_text,
        })

        # Take a snapshot of conversation history
        messages_snapshot = self.messages.copy()

        # Prevent repeated submissions while waiting
        self.send_button.configure(state="disabled")
        self.user_input.configure(state="disabled")
        self.status_label.configure(
            text="Paption is thinking... chill kiasi"
        )

        # Run Ollama in a background thread
        threading.Thread(
            target=self.get_response,
            args=(messages_snapshot,),
            daemon=True,
        ).start()

        return "break"

    def get_response(self, messages_snapshot):

        try:
            response = chat(
                model=MODEL,
                messages=messages_snapshot,
            )

            answer = response.message.content or "No response received."

            self.after(
                0,
                lambda: self.display_response(answer),
            )

        except Exception as error:

            error_message = str(error)

            self.after(
                0,
                lambda: self.display_response(
                    f"Paption is experiencing a problem:\n{error_message}"
                ),
            )

    def display_response(self, answer):

        self.add_message("Paption", answer)

        # Save successful AI responses to conversation history
        if not answer.startswith("Paption is experiencing a problem:"):
            self.messages.append({
                "role": "assistant",
                "content": answer,
            })

        self.send_button.configure(state="normal")
        self.user_input.configure(state="normal")
        self.user_input.focus_set()

        self.status_label.configure(text="Powered by Ollama")


if __name__ == "__main__":
    app = PaptionBot()
    app.mainloop()
