import threading
import customtkinter as ctk

from ollama import chat
from PIL import Image
from pathlib import Path


# CONFIGURATION

MODEL = "qwen3.5:0.8b"

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "paption_logo_updated.png"
ICON_PATH = BASE_DIR / "paption_icon_updated.ico"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# PAPTION BOT APPLICATION

class PaptionBot(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Paption Bot")
        self.geometry("1000x700")
        self.minsize(600, 450)

        if ICON_PATH.exists():
            self.iconbitmap(str(ICON_PATH))

        # Conversation history
        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are Paption Bot, a friendly and helpful "
                    "AI assistant. Answer clearly and concisely."
                )
            }
        ]

        # HEADER

        self.header_frame = ctk.CTkFrame(
            self,
            height=85,
            corner_radius=0,
            fg_color="#202020"
        )

        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)

        # Logo
        if LOGO_PATH.exists():

            self.logo_image = ctk.CTkImage(
                light_image=Image.open(LOGO_PATH),
                dark_image=Image.open(LOGO_PATH),
                size=(70, 70)
            )

            self.logo_label = ctk.CTkLabel(
                self.header_frame,
                image=self.logo_image,
                text=""
            )

            self.logo_label.pack(
                side="left",
                padx=15,
                pady=5
            )

        # Title
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Paption Bot",
            font=("Arial", 22, "bold"),
            text_color="#FFFFFF"
        )

        self.title_label.pack(
            side="left",
            padx=10
        )

        # Status
        self.status_label = ctk.CTkLabel(
            self.header_frame,
            text="Powered by Ollama",
            font=("Arial", 12),
            text_color="#A0A0A0"
        )

        self.status_label.pack(
            side="right",
            padx=20
        )

        # CHAT AREA

        self.chat_area = ctk.CTkScrollableFrame(
            self,
            fg_color="#171717",
            corner_radius=0
        )

        self.chat_area.pack(
            fill="both",
            expand=True,
            padx=0,
            pady=0
        )

        # Welcome message
        self.add_message(
            "Paption",
            "Hello! I'm Paption Bot. How can I help you today?"
        )

        # INPUT AREA

        self.input_frame = ctk.CTkFrame(
            self,
            fg_color="#202020",
            corner_radius=0,
            height=85
        )

        self.input_frame.pack(
            fill="x",
            side="bottom"
        )

        self.input_frame.pack_propagate(False)

        # Message entry
        self.message_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Message Paption Bot...",
            height=45,
            corner_radius=20,
            fg_color="#303030",
            text_color="#FFFFFF",
            border_color="#454545",
            font=("Arial", 14)
        )

        self.message_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(20, 10),
            pady=18
        )

        self.message_entry.bind(
            "<Return>",
            self.send_message
        )

        # Send button
        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="Send",
            width=90,
            height=45,
            corner_radius=20,
            fg_color="#8B5CF6",
            hover_color="#7C3AED",
            text_color="#FFFFFF",
            command=self.send_message
        )

        self.send_button.pack(
            side="right",
            padx=(5, 20),
            pady=18
        )

        self.message_entry.focus()

    # MESSAGE DISPLAY

    def add_message(self, sender, message):

        is_user = sender == "You"

        row = ctk.CTkFrame(
            self.chat_area,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            padx=20,
            pady=8
        )

        bubble_color = "#34304A" if is_user else "#262626"
        alignment = "e" if is_user else "w"

        bubble = ctk.CTkFrame(
            row,
            fg_color=bubble_color,
            corner_radius=16
        )

        bubble.pack(
            anchor=alignment,
            padx=5
        )

        sender_label = ctk.CTkLabel(
            bubble,
            text=sender,
            font=("Arial", 11, "bold"),
            text_color="#B7A6FF",
            anchor="w"
        )

        sender_label.pack(
            anchor="w",
            padx=12,
            pady=(8, 0)
        )

        message_label = ctk.CTkLabel(
            bubble,
            text=message,
            font=("Arial", 14),
            text_color="#FFFFFF",
            justify="left",
            anchor="w",
            wraplength=650
        )

        message_label.pack(
            anchor="w",
            padx=12,
            pady=(3, 8)
        )

        self.after(
            100,
            lambda: self.chat_area._parent_canvas.yview_moveto(1.0)
        )

        return message_label

    # SEND MESSAGE

    def send_message(self, event=None):

        user_text = self.message_entry.get().strip()

        if not user_text:
            return

        self.message_entry.delete(0, "end")

        self.add_message("You", user_text)

        self.messages.append({
            "role": "user",
            "content": user_text
        })

        messages_snapshot = list(self.messages)

        self.message_entry.configure(state="disabled")
        self.send_button.configure(state="disabled")

        self.status_label.configure(
            text="Paption is thinking..."
        )

        response_label = self.add_message(
            "Paption",
            " "
        )

        threading.Thread(
            target=self.get_response,
            args=(messages_snapshot, response_label),
            daemon=True
        ).start()

    # OLLAMA RESPONSE

    def get_response(self, messages_snapshot, response_label):

        answer = ""

        try:

            response = chat(
                model=MODEL,
                messages=messages_snapshot,
                stream=True,
                think=False,
                keep_alive="10m",
                options={
                    "num_predict": 150
                }
            )

            for chunk in response:

                content = chunk.message.content or ""

                if content:

                    answer += content

                    self.after(
                        0,
                        self.append_chunk,
                        response_label,
                        answer
                    )

            if not answer.strip():
                raise RuntimeError("No response received from the model.")

            self.after(
                0,
                self.display_response,
                answer,
                True
            )

        except Exception as error:

            error_message = (
                f"Paption is experiencing a problem: {error}"
            )

            self.after(
                0,
                self.append_chunk,
                response_label,
                error_message
            )

            self.after(
                0,
                self.display_response,
                error_message,
                False
            )

    # UPDATE STREAMING MESSAGE

    def append_chunk(self, response_label, answer):

        response_label.configure(text=answer)

        self.chat_area._parent_canvas.yview_moveto(1.0)

    # FINISH RESPONSE

    def display_response(self, answer, success=True):

        if success:

            self.messages.append({
                "role": "assistant",
                "content": answer
            })

        else:

            if self.messages and self.messages[-1]["role"] == "user":
                self.messages.pop()

        self.message_entry.configure(state="normal")
        self.send_button.configure(state="normal")

        self.status_label.configure(
            text="Powered by Ollama"
        )

        self.message_entry.focus()


# RUN APPLICATION

if __name__ == "__main__":

    app = PaptionBot()
    app.mainloop()