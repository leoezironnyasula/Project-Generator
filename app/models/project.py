"""
Core data models for the project generator.
app/models/project.py
"""
from dataclasses import dataclass, field
from enum import Enum


class Difficulty(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Domain(str, Enum):
    CLI = "cli"
    WEB_API = "web_api"
    WEB_FRONTEND = "web_frontend"
    DESKTOP_APP = "desktop_app"
    AUTOMATION = "automation"
    DATA = "data"
    GAME = "game"


@dataclass
class TechStack:
    language: str
    framework: str | None = None
    libraries: list[str] = field(default_factory=list)
    database: str | None = None

    def summary(self) -> str:
        parts = [self.language]
        if self.framework:
            parts.append(self.framework)
        if self.database:
            parts.append(self.database)
        return " + ".join(parts)


@dataclass
class Project:
    title: str
    description: str
    domain: Domain
    difficulty: Difficulty
    tech_stack: TechStack
    features: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "domain": self.domain.value,
            "difficulty": self.difficulty.value,
            "tech_stack": self.tech_stack.summary(),
            "features": self.features,
        }