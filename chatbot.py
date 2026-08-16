import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

chat = client.chats.create(
    model="gemini-3.6-flash"
)

print("🤖 Chintu's AI Chatbot")
print("Type 'exit' to stop.\n")

while True:
    user_message = input("You: ")

    if user_message.lower() == "exit":
        print("Bot: Goodbye!")
        break

    response = chat.send_message(user_message)

    print("Bot:", response.text)