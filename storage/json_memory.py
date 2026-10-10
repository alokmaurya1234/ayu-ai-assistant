import json
from pathlib import Path

MEMORY_FILE = Path(__file__).resolve().parents[1] / "memory.json"


def load_memory():
    if MEMORY_FILE.exists():
        with MEMORY_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)

    return {}


def save_memory(memory):
    with MEMORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4, ensure_ascii=False)