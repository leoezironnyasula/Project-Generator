"""
Parses LLM output into a structured Project object.
app/llm/chain.py

This is the missing link flagged earlier: idea_generator.py can call
ask_llm() and get text back, but that text needs to become a real
Project (with proper Domain/Difficulty enums, a TechStack, etc.)
before the rest of the app can use it. That parsing happens here.
"""
import json
from pathlib import Path

from app.llm.client import ask_llm
from app.models.project import Project, TechStack, Domain, Difficulty
from app.core.exceptions import LLMResponseError

# Path to the prompt template file, relative to this file's location.
PROMPT_PATH = Path(__file__).parent.parent / "generator" / "prompts" / "idea_prompt.txt"


def _load_prompt() -> str:
    """Reads the prompt template from disk."""
    return PROMPT_PATH.read_text()


def _parse_json_response(raw_text: str) -> dict:
    """
    Extracts a JSON object from the LLM's raw text response.

    Local LLMs often wrap JSON in markdown code fences (```json ... ```)
    even when told not to, so this strips those if present before
    attempting to parse.
    """
    cleaned = raw_text.strip()

    if cleaned.startswith("```"):
        # Remove the opening fence (``` or ```json) and closing fence.
        lines = cleaned.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        cleaned = "\n".join(lines)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise LLMResponseError(f"Could not parse LLM output as JSON: {e}\nRaw output: {raw_text}") from e


def _build_project_from_data(data: dict) -> Project:
    """
    Converts a parsed JSON dict into a real Project object, mapping
    string values onto the Domain/Difficulty enums and validating
    that required fields are present.
    """
    try:
        domain = Domain(data["domain"])
        difficulty = Difficulty(data["difficulty"])
    except (KeyError, ValueError) as e:
        # Either a required field was missing, or the LLM returned a
        # value that isn't one of our enum options (e.g. "web" instead
        # of "web_api").
        raise LLMResponseError(f"Invalid or missing domain/difficulty in LLM output: {e}") from e

    tech_stack = TechStack(
        language=data.get("language", "Python"),
        framework=data.get("framework"),
        libraries=data.get("libraries", []) or [],
        database=data.get("database"),
    )

    # Basic sanity checks -- the JSON can be technically valid but
    # still nonsense (empty strings, absurd lengths). This won't catch
    # every bad case, but it catches the cheap/common ones without
    # needing a whitelist of "real" languages, which would be fragile.
    if not tech_stack.language.strip():
        raise LLMResponseError("LLM returned an empty language field.")
    if len(data.get("title", "")) > 100:
        raise LLMResponseError("LLM returned an unreasonably long title -- likely malformed output.")
    if not data.get("features"):
        raise LLMResponseError("LLM returned a project with no features.")

    try:
        return Project(
            title=data["title"],
            description=data["description"],
            domain=domain,
            difficulty=difficulty,
            tech_stack=tech_stack,
            features=data.get("features", []) or [],
        )
    except KeyError as e:
        raise LLMResponseError(f"Missing required field in LLM output: {e}") from e


def generate_project_via_llm() -> Project:
    """
    Full pipeline: build prompt -> ask the LLM -> parse the response
    into a Project.

    Raises:
        LLMConnectionError: if the LLM server can't be reached
                             (propagated from ask_llm, not caught here).
        LLMResponseError: if the response can't be parsed into a
                           valid Project.
    """
    prompt = _load_prompt()
    raw_response = ask_llm(prompt)
    data = _parse_json_response(raw_response)
    return _build_project_from_data(data)