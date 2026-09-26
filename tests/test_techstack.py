"""
tests/test_techstack.py
Basic sanity tests for the tech stack recommender.
Run with: pytest
"""
from app.techstack.recommender import recommend_stack
from app.models.project import Domain


def test_recommend_stack_returns_valid_stack_for_known_domain():
    stack = recommend_stack(Domain.CLI)
    assert stack.language  # every stack must at least have a language