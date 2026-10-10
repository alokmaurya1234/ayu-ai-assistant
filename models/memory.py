
from pydantic import BaseModel, Field


class MemoryDecision(BaseModel):
    should_remember: bool
    reason: str


class ExtractedMemory(BaseModel):
    name: str | None = None
    age: int | None = None
    interest: str | None = None
    career_goal: str | None = None
    current_learning: list[str] = Field(default_factory=list)
    preferences: list[str] = Field(default_factory=list)
    ongoing_projects: list[str] = Field(default_factory=list)
