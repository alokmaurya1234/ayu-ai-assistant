import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel


class MemoryDecision(BaseModel):
    should_remember: bool
    reason: str

class ExtractedMemory(BaseModel):
    career_goal: str | None = None
    current_learning: list[str] = []
    preferences: list[str] = []
    ongoing_projects: list[str] = []

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


def should_remember(recent_conversation, latest_user_message):
    recent_messages = recent_conversation[-5:]

    if not recent_messages:
        return False

    response = client.responses.parse(
        model="gpt-5.6-luna",
        instructions="""
        Decide whether the conversation contains persistent
        information worth remembering about the user.

        Remember long-term goals, stable preferences, personal
        facts, interests, and ongoing projects.

        Ignore greetings, casual questions, and temporary activities.

        Return a Boolean decision and a short reason.
        """,
        input=str(recent_messages),
        text_format=MemoryDecision,
    )

    decision = response.output_parsed

    if decision is None:
        return False

    print(f"Memory decision: {decision.should_remember}")
    print(f"Reason: {decision.reason}")

    return decision.should_remember

def extract_memory(recent_conversation):
    response = client.responses.parse(
        model="gpt-5.6-luna",
        instructions="""
        Extract useful, persistent information about the user.

        Identify:
        - Their current career goal
        - What they are learning
        - Their stable preferences
        - Their ongoing projects

        Only extract facts supported by the conversation.
        Do not invent information.
        Leave fields empty when information is unavailable.
        Return only the structured result.
        """,
        input=str(recent_conversation),
        text_format=ExtractedMemory,
    )

    extracted = response.output_parsed

    if extracted is None:
        return {}

    return extracted.model_dump(exclude_none=True)


def update_memory(existing_memory, new_memory):
    updated_memory = existing_memory | new_memory
    return updated_memory


def save_memory(memory):
    memory_file = "memory.json"

    with open(memory_file, "w") as file:
        json.dump(memory, file, indent=4)

def process_memory(recent_conversation):
    global memory

    # Step 1: Decide whether to remember
    if not should_remember(recent_conversation):
        return

    # Step 2: Extract facts
    new_memory = extract_memory(recent_conversation)

    # Step 3: Remove empty values
    new_memory = {
        key: value
        for key, value in new_memory.items()
        if value not in (None, "", [], {})
    }

    # Nothing useful was extracted
    if not new_memory:
        print("No useful memories extracted.")
        return

    # Step 4: Merge with existing memory
    memory = update_memory(memory, new_memory)

    # Step 5: Save to disk
    save_memory(memory)

    print("Memory updated successfully.")

memory = load_memory()


while True:
    user_message = input("You: ")

    if user_message.lower() == "exit":
        break

    conversation.append({
        "role": "user",
        "content": user_message
    })

    process_memory(conversation[-5:])
        
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