
"""
tests/test_generator.py
Basic sanity tests for the idea generator.
Run with: pytest
"""
from app.generator.idea_generator import generate_random_project
from app.models.project import Project
 
 
def test_generate_random_project_returns_project():
    # Should always return a real Project object, not None or a dict.
    result = generate_random_project()
    assert isinstance(result, Project)
 
 
def test_generated_project_has_required_fields():
    project = generate_random_project()
    # Basic shape check — catches typos/missing fields early.
    assert project.title
    assert project.description
    assert project.tech_stack is not None
 
