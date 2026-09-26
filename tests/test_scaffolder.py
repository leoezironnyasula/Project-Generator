"""
tests/test_scaffolder.py
Basic sanity tests for the scaffolder.
Run with: pytest
"""
import shutil

from app.scaffolder.builder import scaffold_project
from app.generator.idea_generator import generate_random_project


def test_scaffold_project_creates_folder(tmp_path):
    # tmp_path is a pytest built-in fixture: a temporary directory
    # that gets cleaned up automatically after the test runs.
    project = generate_random_project()

    result_path = scaffold_project(project, base_path=str(tmp_path))

    assert result_path.exists()
    assert (result_path / "README.md").exists()