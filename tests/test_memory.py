
from models.memory import ExtractedMemory
from services.memory_service import update_memory
from unittest.mock import Mock
import services.memory_service as memory_service


def test_memory_schema_defaults():
    memory = ExtractedMemory()

    assert memory.name is None
    assert memory.current_learning == []
    assert memory.preferences == []


def test_update_memory_preserves_existing_list_items():
    existing = {"current_learning": ["Python"]}
    new = {"current_learning": ["LangChain"]}

    result = update_memory(existing, new)

    assert result["current_learning"] == ["Python", "LangChain"]


def test_update_memory_removes_duplicate_items():
    existing = {"current_learning": ["Python"]}
    new = {"current_learning": ["Python", "LangChain"]}

    result = update_memory(existing, new)

    assert result["current_learning"] == ["Python", "LangChain"]


def test_update_memory_does_not_modify_original():
    existing = {"current_learning": ["Python"]}
    new = {"current_learning": ["LangChain"]}

    update_memory(existing, new)

    assert existing == {"current_learning": ["Python"]}


def test_new_scalar_value_updates_old_value():
    existing = {"career_goal": "Web developer"}
    new = {"career_goal": "GenAI engineer"}

    result = update_memory(existing, new)

    assert result["career_goal"] == "GenAI engineer"




from unittest.mock import Mock

import services.memory_service as memory_service


def test_process_memory_does_not_save_when_not_needed(monkeypatch):
    client = Mock()
    memory = {"current_learning": ["Python"]}

    monkeypatch.setattr(
        memory_service,
        "should_remember",
        lambda *args: False,
    )

    def unexpected_extraction(*args):
        raise AssertionError("Extraction should not run")

    monkeypatch.setattr(
        memory_service,
        "extract_memory",
        unexpected_extraction,
    )

    monkeypatch.setattr(
        memory_service,
        "save_memory",
        lambda *args: (_ for _ in ()).throw(
            AssertionError("Memory should not be saved")
        ),
    )

    result = memory_service.process_memory(
        client,
        memory,
        [{"role": "user", "content": "What is RAG?"}],
        "What is RAG?",
    )

    assert result == {"current_learning": ["Python"]}


def test_process_memory_saves_useful_memory(monkeypatch):
    client = Mock()
    memory = {"current_learning": ["Python"]}
    saved = {}

    monkeypatch.setattr(
        memory_service,
        "should_remember",
        lambda *args: True,
    )

    monkeypatch.setattr(
        memory_service,
        "extract_memory",
        lambda *args: {
            "current_learning": ["LangChain"],
            "career_goal": "GenAI engineer",
        },
    )

    def fake_save_memory(updated_memory):
        saved.update(updated_memory)

    monkeypatch.setattr(
        memory_service,
        "save_memory",
        fake_save_memory,
    )

    result = memory_service.process_memory(
        client,
        memory,
        [{"role": "user", "content": "I'm learning LangChain"}],
        "I'm learning LangChain",
    )

    assert result["current_learning"] == ["Python", "LangChain"]
    assert result["career_goal"] == "GenAI engineer"
    assert saved == result


def test_process_memory_does_not_save_empty_extraction(monkeypatch):
    client = Mock()
    memory = {"current_learning": ["Python"]}
    save_calls = []

    monkeypatch.setattr(
        memory_service,
        "should_remember",
        lambda *args: True,
    )

    monkeypatch.setattr(
        memory_service,
        "extract_memory",
        lambda *args: {},
    )

    monkeypatch.setattr(
        memory_service,
        "save_memory",
        lambda *args: save_calls.append(args),
    )

    result = memory_service.process_memory(
        client,
        memory,
        [{"role": "user", "content": "Something unclear"}],
        "Something unclear",
    )

    assert result == memory
    assert save_calls == []




import json

from storage import json_memory


def test_save_and_load_memory(tmp_path, monkeypatch):
    test_file = tmp_path / "memory.json"

    monkeypatch.setattr(json_memory, "MEMORY_FILE", test_file)

    original_memory = {
        "name": "Alok",
        "career_goal": "GenAI engineer",
        "current_learning": ["Python", "LangChain"],
    }

    json_memory.save_memory(original_memory)
    loaded_memory = json_memory.load_memory()

    assert loaded_memory == original_memory


def test_load_memory_returns_empty_dict_when_file_missing(
    tmp_path, monkeypatch
):
    test_file = tmp_path / "missing.json"

    monkeypatch.setattr(json_memory, "MEMORY_FILE", test_file)

    assert json_memory.load_memory() == {}


def test_saved_json_is_readable(tmp_path, monkeypatch):
    test_file = tmp_path / "memory.json"

    monkeypatch.setattr(json_memory, "MEMORY_FILE", test_file)

    memory = {"name": "Alok", "interest": "GenAI"}

    json_memory.save_memory(memory)

    with test_file.open("r", encoding="utf-8") as file:
        loaded = json.load(file)

    assert loaded == memory



def test_process_memory_handles_decision_failure(monkeypatch):
    client = Mock()
    memory = {"current_learning": ["Python"]}

    def failing_decision(*args):
        raise RuntimeError("Simulated API failure")

    monkeypatch.setattr(
        memory_service,
        "should_remember",
        failing_decision,
    )

    result = memory_service.process_memory(
        client,
        memory,
        [{"role": "user", "content": "I'm learning LangChain"}],
        "I'm learning LangChain",
    )

    assert result == memory



def test_process_memory_handles_extraction_failure(monkeypatch):
    client = Mock()
    memory = {"current_learning": ["Python"]}

    monkeypatch.setattr(
        memory_service,
        "should_remember",
        lambda *args: True,
    )

    def failing_extraction(*args):
        raise RuntimeError("Simulated extraction failure")

    monkeypatch.setattr(
        memory_service,
        "extract_memory",
        failing_extraction,
    )

    result = memory_service.process_memory(
        client,
        memory,
        [{"role": "user", "content": "I'm learning LangChain"}],
        "I'm learning LangChain",
    )

    assert result == memory



def test_process_memory_handles_save_failure(monkeypatch):
    client = Mock()
    memory = {"current_learning": ["Python"]}

    monkeypatch.setattr(
        memory_service,
        "should_remember",
        lambda *args: True,
    )

    monkeypatch.setattr(
        memory_service,
        "extract_memory",
        lambda *args: {"current_learning": ["LangChain"]},
    )

    def failing_save(*args):
        raise OSError("Simulated disk failure")

    monkeypatch.setattr(
        memory_service,
        "save_memory",
        failing_save,
    )

    result = memory_service.process_memory(
        client,
        memory,
        [{"role": "user", "content": "I'm learning LangChain"}],
        "I'm learning LangChain",
    )

    assert result == memory



def test_no_memory_decision_does_not_save_or_modify_file(
    tmp_path, monkeypatch
):
    from storage import json_memory

    test_file = tmp_path / "memory.json"
    original_content = '{\n  "name": "Alok",\n  "current_learning": ["Python"]\n}'

    test_file.write_text(original_content, encoding="utf-8")

    monkeypatch.setattr(
        json_memory, "MEMORY_FILE", test_file
    )

    monkeypatch.setattr(
        memory_service, "should_remember", lambda *args: False
    )

    def unexpected_extraction(*args):
        raise AssertionError("Extraction should not run")

    monkeypatch.setattr(
        memory_service, "extract_memory", unexpected_extraction
    )

    result = memory_service.process_memory(
        Mock(),
        json_memory.load_memory(),
        [{"role": "user", "content": "What is REST?"}],
        "What is REST?",
    )

    assert result["name"] == "Alok"
    assert test_file.read_text(encoding="utf-8") == original_content



import pytest


def test_load_corrupted_json_raises_error(tmp_path, monkeypatch):
    test_file = tmp_path / "memory.json"
    test_file.write_text('{"name":', encoding="utf-8")

    monkeypatch.setattr(json_memory, "MEMORY_FILE", test_file)

    with pytest.raises(ValueError, match="invalid JSON"):
        json_memory.load_memory()


def test_load_json_list_raises_error(tmp_path, monkeypatch):
    test_file = tmp_path / "memory.json"
    test_file.write_text('["Alok", "Python"]', encoding="utf-8")

    monkeypatch.setattr(json_memory, "MEMORY_FILE", test_file)

    with pytest.raises(ValueError, match="JSON object"):
        json_memory.load_memory()
