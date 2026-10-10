
import json
import os
from pathlib import Path

MEMORY_FILE = Path(__file__).resolve().parents[1] / "memory.json"


def load_memory():
    if not MEMORY_FILE.exists():
        return {}

    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as file:
            memory = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Memory file contains invalid JSON: {MEMORY_FILE}. "
            "Restore a valid backup before continuing."
        ) from error

    if not isinstance(memory, dict):
        raise ValueError(
            f"Memory file must contain a JSON object: {MEMORY_FILE}"
        )

    return memory


def save_memory(memory):
    if not isinstance(memory, dict):
        raise TypeError("Memory must be a dictionary.")

    temp_file = MEMORY_FILE.with_suffix(".tmp")

    try:
        with temp_file.open("w", encoding="utf-8") as file:
            json.dump(
                memory,
                file,
                indent=4,
                ensure_ascii=False,
            )
            file.flush()
            os.fsync(file.fileno())

        temp_file.replace(MEMORY_FILE)

    finally:
        if temp_file.exists():
            temp_file.unlink()
