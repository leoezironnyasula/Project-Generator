"""
Generates a random project idea.
app/generator/idea_generator.py

UPDATED: now actually uses the LLM pipeline (llm/chain.py) when
settings.use_llm is True, instead of just probing the connection.
Falls back to the hardcoded templates if the LLM is unavailable or
returns something that can't be parsed -- so the app never crashes
just because Ollama isn't running.
"""
import random

from app.models.project import Project, Domain, Difficulty
from app.techstack.recommender import recommend_stack
from app.core.config import settings
from app.llm.chain import generate_project_via_llm
from app.core.exceptions import LLMConnectionError, LLMResponseError

# Hardcoded fallback pool. Each entry defines everything EXCEPT the
# tech stack -- that gets filled in dynamically by the recommender.
IDEA_TEMPLATES = [
    {
        "title": "Password Strength Auditor",
        "description": "A CLI tool that checks passwords against common patterns and estimates crack time.",
        "domain": Domain.CLI,
        "difficulty": Difficulty.BEGINNER,
        "features": ["strength scoring", "common password blacklist check", "colored terminal output"],
    },
    {
        "title": "Local Notes API",
        "description": "A small REST API for storing and searching personal notes, backed by a database.",
        "domain": Domain.WEB_API,
        "difficulty": Difficulty.INTERMEDIATE,
        "features": ["CRUD endpoints", "full-text search", "tag filtering"],
    },
    {
        "title": "File Organizer Bot",
        "description": "A script that watches a folder and auto-sorts files into subfolders by type.",
        "domain": Domain.AUTOMATION,
        "difficulty": Difficulty.BEGINNER,
        "features": ["live folder watching", "custom sorting rules", "undo log"],
    },
]


def _generate_from_templates() -> Project:
    """Builds a Project from the hardcoded template pool. Non-LLM fallback path."""
    template = random.choice(IDEA_TEMPLATES)
    stack = recommend_stack(template["domain"], template["difficulty"])

    return Project(
        title=template["title"],
        description=template["description"],
        domain=template["domain"],
        difficulty=template["difficulty"],
        tech_stack=stack,
        features=template["features"],
    )


def generate_random_project() -> Project:
    """
    Returns one randomly generated Project.

    If settings.use_llm is True, tries the real LLM pipeline first
    (llm/chain.py: prompt -> Ollama -> parsed Project). If that fails
    for ANY reason -- Ollama not running, or the model returned
    something that couldn't be parsed -- silently falls back to the
    hardcoded templates so the app stays usable either way.
    """
    if settings.use_llm:
        try:
            return generate_project_via_llm()
        except (LLMConnectionError, LLMResponseError) as e:
            # DEBUG: print the real reason instead of silently falling back,
            # so we can see in the terminal exactly what's going wrong.
            print(f"[DEBUG] LLM generation failed, falling back to templates: {e}")
    else:
        print("[DEBUG] USE_LLM is not enabled -- using hardcoded templates.")

    return _generate_from_templates()