import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

conversation = []


def load_memory():
    memory_file = "memory.json"

    if os.path.exists(memory_file):
        with open(memory_file, "r") as file:
            return json.load(file)

    return {}


def update_memory(existing_memory, new_memory):
    updated_memory = existing_memory | new_memory
    return updated_memory


def save_memory(memory):
    memory_file = "memory.json"

    with open(memory_file, "w") as file:
        json.dump(memory, file, indent=4)


memory = load_memory()


while True:
    user_message = input("You: ")

    if user_message.lower() == "exit":
        break

    conversation.append({
        "role": "user",
        "content": user_message
    })

    context = f"""
    User information:
    {memory}

    Conversation:
    {conversation}
    """

    response = client.responses.create(
        model="gpt-5.6-luna",
        instructions="""
        You are Ayu, a friendly and emotionally aware AI assistant.
        Keep your responses natural, conversational, and concise.
        """,
        input=context
    )

    assistant_message = response.output_text

    conversation.append({
        "role": "assistant",
        "content": assistant_message
    })

    print(f"Ayu: {assistant_message}")