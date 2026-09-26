"""
Generates a random project idea.
app/generator/idea_generator.py

For now this is hardcoded (no LLM call yet) so we can test the full
pipeline: generator -> models -> main.py output. Once this works,
we'll swap the hardcoded list for a call to app/llm/client.py.
"""
import random

from app.models.project import Difficulty, Domain, Project, TechStack

# A small hardcoded pool of sample projects.
# Each one is a fully-formed Project object using the dataclasses
# we defined in app/models/project.py.
SAMPLE_PROJECTS: list[Project] = [
    Project(
        title="Password Strength Auditor",
        description="A CLI tool that checks passwords against common patterns and estimates crack time.",
        domain=Domain.CLI,
        difficulty=Difficulty.BEGINNER,
        tech_stack=TechStack(language="Python", libraries=["argparse", "re"]),
        features=["strength scoring", "common password blacklist check", "colored terminal output"],
    ),
    Project(
        title="Local Notes API",
        description="A small REST API for storing and searching personal notes, backed by SQLite.",
        domain=Domain.WEB_API,
        difficulty=Difficulty.INTERMEDIATE,
        tech_stack=TechStack(language="Python", framework="Flask", database="SQLite"),
        features=["CRUD endpoints", "full-text search", "tag filtering"],
    ),
    Project(
        title="File Organizer Bot",
        description="A script that watches a folder and auto-sorts files into subfolders by type.",
        domain=Domain.AUTOMATION,
        difficulty=Difficulty.BEGINNER,
        tech_stack=TechStack(language="Python", libraries=["watchdog", "shutil"]),
        features=["live folder watching", "custom sorting rules", "undo log"],
    ),
]


def generate_random_project() -> Project:
    """
    Picks and returns one random Project from the sample pool.

    Later, this function's body will change to call the local LLM
    (via app/llm/client.py) instead of picking from a fixed list —
    but the function signature (returns a Project) stays the same,
    so nothing else in the app needs to change when we do that swap.
    """
    return random.choice(SAMPLE_PROJECTS)