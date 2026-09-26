"""
Recommends a tech stack for a given domain/difficulty.
app/techstack/recommender.py

Currently just wraps rules.py (random pick from the fixed options).
Later, this is where you'd add LLM-based reasoning, e.g. "pick a
stack that matches the user's stated experience level" — the rest
of the app only ever calls recommend_stack(), so swapping the
internals later won't require touching any callers.
"""
import random

from app.models.project import Domain, Difficulty, TechStack
from app.techstack.rules import get_options_for_domain
from app.core.exceptions import UnsupportedDomainError


def recommend_stack(domain: Domain, difficulty: Difficulty = Difficulty.BEGINNER) -> TechStack:
    """
    Picks a TechStack for the given domain.

    Args:
        domain: what kind of project this is (CLI, WEB_API, etc.)
        difficulty: currently unused, reserved for future logic like
                    "prefer simpler stacks for beginner difficulty"

    Raises:
        UnsupportedDomainError: if no stack options exist for this domain.
    """
    options = get_options_for_domain(domain)

    if not options:
        raise UnsupportedDomainError(
            f"No tech stack options defined for domain: {domain}"
        )

    # For now, just pick randomly. Difficulty-based filtering can be
    # added here later without changing the function's signature.
    return random.choice(options)