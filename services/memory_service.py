from models.memory import MemoryDecision, ExtractedMemory
from storage.json_memory import save_memory


def should_remember(client, recent_conversation, latest_user_message):
    if not recent_conversation:
        return False

    response = client.responses.parse(
        model="gpt-5.6-luna",
        instructions="""
        Decide whether the latest user message contains persistent
        information worth remembering.

        Remember stable personal facts, long-term goals, preferences,
        interests, current learning, and ongoing projects.

        Use recent conversation only as context.
        Ignore greetings, thanks, arithmetic, and ordinary questions.
        Do not treat an assistant's suggestion as a fact about the user.
        """,
        input=f"""
        Recent context:
        {recent_conversation}

        Latest user message:
        {latest_user_message}
        """,
        text_format=MemoryDecision,
    )

    decision = response.output_parsed

    if decision is None:
        return False

    print(f"Memory decision: {decision.should_remember}")
    print(f"Reason: {decision.reason}")

    return decision.should_remember


def extract_memory(client, recent_conversation):
    response = client.responses.parse(
        model="gpt-5.6-luna",
        instructions="""
        Extract only useful, persistent information explicitly supported
        by the user's messages.

        Identify:
        - Career goal
        - Current learning
        - Stable preferences
        - Ongoing projects

        Ignore assistant suggestions and temporary questions.
        Leave unavailable fields empty. Do not invent facts.
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
    updated_memory = existing_memory.copy()

    for key, new_value in new_memory.items():
        old_value = updated_memory.get(key)

        if isinstance(old_value, list) and isinstance(new_value, list):
            updated_memory[key] = list(dict.fromkeys(old_value + new_value))
        else:
            updated_memory[key] = new_value

    return updated_memory





def process_memory(client, memory, recent_conversation, latest_user_message):
    try:
        should_save = should_remember(
            client,
            recent_conversation,
            latest_user_message,
        )

        if not should_save:
            return memory

        new_memory = extract_memory(client, recent_conversation)

        new_memory = {
            key: value
            for key, value in new_memory.items()
            if value not in (None, "", [], {})
        }

        if not new_memory:
            print("No useful memories extracted.")
            return memory

        updated_memory = update_memory(memory, new_memory)
        save_memory(updated_memory)

        print("Memory updated successfully.")
        return updated_memory

    except Exception as error:
        print(f"Memory processing failed: {error}")
        return memory
