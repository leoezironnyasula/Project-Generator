"""
Heuristic (non-LLM) rules for picking a tech stack.
app/techstack/rules.py

This is the "dumb but reliable" fallback: fixed rules mapping a
project's domain to reasonable tech stack options. Used when no LLM
is available, or as a sanity-check against whatever the LLM suggests.
"""
from app.models.project import Domain, TechStack

# For each domain, a small list of reasonable stack options.
# The recommender (recommender.py) picks one of these, either
# randomly or based on difficulty.
STACK_OPTIONS: dict[Domain, list[TechStack]] = {
    Domain.CLI: [
        TechStack(language="Python", libraries=["argparse"]),
        TechStack(language="Python", libraries=["click"]),
        TechStack(language="Rust", libraries=["clap"]),
    ],
    Domain.WEB_API: [
        TechStack(language="Python", framework="FastAPI", database="SQLite"),
        TechStack(language="Python", framework="Flask", database="SQLite"),
        TechStack(language="JavaScript", framework="Express", database="MongoDB"),
    ],
    Domain.WEB_FRONTEND: [
        TechStack(language="JavaScript", framework="React"),
        TechStack(language="TypeScript", framework="Vue"),
    ],
    Domain.DESKTOP_APP: [
        TechStack(language="Python", framework="PyQt"),
        TechStack(language="C#", framework="WPF"),
    ],
    Domain.AUTOMATION: [
        TechStack(language="Python", libraries=["watchdog"]),
        TechStack(language="Python", libraries=["schedule"]),
    ],
    Domain.DATA: [
        TechStack(language="Python", libraries=["pandas", "matplotlib"]),
    ],
    Domain.GAME: [
        TechStack(language="Python", framework="Pygame"),
        TechStack(language="C#", framework="Unity"),
    ],
}


def get_options_for_domain(domain: Domain) -> list[TechStack]:
    """
    Returns the list of stack options defined for a domain.
    Returns an empty list if the domain has no rules defined yet —
    callers should handle that case rather than assuming a result.
    """
    return STACK_OPTIONS.get(domain, [])