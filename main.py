import os

from dotenv import load_dotenv
from openai import OpenAI

from services.memory_service import process_memory
from storage.json_memory import load_memory


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

conversation = []
memory = load_memory()

while True:
    user_message = input("You: ")

    if user_message.lower() == "exit":
        break

    conversation.append({
        "role": "user",
        "content": user_message
    })

    memory = process_memory(
    client,
    memory,
    conversation[-5:],
    user_message,
    )
        
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