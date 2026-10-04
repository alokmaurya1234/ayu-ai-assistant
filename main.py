import os

from dotenv import load_dotenv
from openai import OpenAI
import json




load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


conversation = []

def load_memory():
    persistent_data = "memory.json"

    if os.path.exists(persistent_data):
        with open(persistent_data, "r") as file:
            data = json.load(file)
            # print(data)
    return data

memory = load_memory()
# conversation.append({"role": "memory",
#                      "content": memory })    

while True:

   
    # def save_memory(memory):
    #     pass

    

    user_message = input("You: ")

    if user_message.lower() == "exit":
        break

    conversation.append({
        "role": "user",
        "content": user_message
    })

    context = f"""
        user information : {memory}
        coversation : {conversation}
    """
    response = client.responses.create(
        model="gpt-6-luna",
        instructions="""
        You are Ayu, a friendly and emotionally aware AI assistant.
        Keep your responses natural, conversational and concise.
        """,
        input= context
    )

    assistant_message = response.output_text

    conversation.append({
        "role": "assistant",
        "content": assistant_message
    })

    print(f"Ayu: {assistant_message}")