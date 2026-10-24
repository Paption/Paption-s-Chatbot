This is PaptionBot
Your Personal AI Chatbot

PaptionBot is a desktop AI chatbot built with Python and Ollama. It provides a graphical interface for interacting with a locally running language model, allowing users to communicate with AI directly from their desktop.

The project is part of my journey into Python development, artificial intelligence, and large language models (LLMs).

Some of its Features include:

AI-Powered Conversations:** Uses an Ollama language model to generate responses to user messages.
Desktop Interface:** Built with CustomTkinter for a graphical chat experience.
Local AI Inference:** Runs the language model locally through Ollama.
Threading:** Uses Python's threading module to support background tasks and help keep the interface responsive.
Paption Branding:** A personal project designed to grow into a more advanced AI assistant.

Tools Used

 Python        
 Ollama
 CustomTkinter 
 Qwen          
 Threading 

Inorder to run paption bot you require to have:
Python installed.
Ollama installed and running.
The required Python libraries installed.
Sufficient system resources to run your selected language model.

1. Install Ollama

Download and install Ollama from its official website:

https://ollama.com/

2. Download the AI Model

Open your terminal and run:

ollama pull qwen3.5:0.8b

Make sure the model is available locally before launching the chatbot.

3. Clone the Repository

Clone the project using Git:


git clone YOUR_GITHUB_REPOSITORY_URL

Navigate into the project directory:


cd PaptionBot

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository's actual URL.

4. Install Dependencies

Install the required Python packages:


pip install ollama customtkinter

5. Run PaptionBot

Run the Python file containing the chatbot application:

python main.py

Goals with Ppation bot

The goal of PaptionBot is to develop a functional personal AI assistant while gaining practical experience in:

Python application development.
GUI design with CustomTkinter.
Integrating AI models into software applications.
Working with Ollama and local language models.
Managing background tasks with threading.
Debugging and improving real-world software.

Developer

Paption-Leroy Khamati
An independent software development project focused on learning, experimentation, and building practical AI applications.

## 📄 License

PaptionBot is licensed under the MIT License.

You are free to use, copy, modify, distribute, and sublicense this software, including for commercial purposes, subject to the conditions of the license.

See the [LICENSE](LICENSE) file for the full license text.


*PaptionBot — Built with Python, powered by AI, and developed one feature at a time.*
