"""
Defines constraints a user can apply when requesting a random project.
app/generator/constraints.py

E.g. "only give me beginner CLI projects" — this is the shape that
gets passed into the generator (once it supports filtering) to
narrow down what gets returned.
"""
from dataclasses import dataclass

from app.models.project import Domain, Difficulty


@dataclass
class GenerationConstraints:
    # None means "no restriction" for that field.
    domain: Domain | None = None
    difficulty: Difficulty | None = None
    language: str | None = None

    def matches(self, project) -> bool:
        """
        Checks whether a given Project satisfies these constraints.
        Used to filter the sample pool (or, later, to validate
        LLM output before returning it to the user).
        """
        if self.domain and project.domain != self.domain:
            return False
        if self.difficulty and project.difficulty != self.difficulty:
            return False
        if self.language and project.tech_stack.language.lower() != self.language.lower():
            return False
        return True