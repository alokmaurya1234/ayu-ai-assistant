from pydantic import BaseModel


class MemoryDecision(BaseModel):
    should_remember: bool
    reason: str


class ExtractedMemory(BaseModel):
    career_goal: str | None = None
    current_learning: list[str] = []
    preferences: list[str] = []
    ongoing_projects: list[str] = []