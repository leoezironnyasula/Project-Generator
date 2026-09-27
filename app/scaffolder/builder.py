"""
Builds a folder/file structure on disk for a given Project.
app/scaffolder/builder.py
"""
from pathlib import Path

from app.models.project import Project, Domain
from app.core.exceptions import ScaffoldError

DOMAIN_TEMPLATES: dict[Domain, dict[str, list[str]]] = {
    Domain.CLI: {
        "": ["main.py", "requirements.txt", "README.md"],
        "tests": ["test_main.py"],
    },
    Domain.WEB_API: {
        "": ["requirements.txt", "README.md"],
        "app": ["__init__.py", "main.py"],
        "tests": ["test_main.py"],
    },
    Domain.AUTOMATION: {
        "": ["main.py", "requirements.txt", "README.md"],
    },
}


def scaffold_project(project: Project, base_path: str = ".") -> Path:
    """
    Creates a starter folder structure for the given project.
    Raises ScaffoldError (instead of a raw OSError) on any disk failure,
    so callers -- like the API layer -- can catch one known exception
    type and return a clean error message.
    """
    folder_name = project.title.lower().replace(" ", "-")
    project_root = Path(base_path) / folder_name

    template = DOMAIN_TEMPLATES.get(project.domain, {"": ["main.py", "README.md"]})

    try:
        for subfolder, files in template.items():
            folder_path = project_root / subfolder
            folder_path.mkdir(parents=True, exist_ok=True)

            for filename in files:
                file_path = folder_path / filename
                file_path.touch(exist_ok=True)

        readme_path = project_root / "README.md"
        readme_path.write_text(
            f"# {project.title}\n\n"
            f"{project.description}\n\n"
            f"**Tech stack:** {project.tech_stack.summary()}\n\n"
            f"**Features:**\n" + "\n".join(f"- {f}" for f in project.features)
        )
    except OSError as e:
        # Covers permission errors, disk full, invalid path characters, etc.
        raise ScaffoldError(f"Could not create project files at {project_root}: {e}") from e

    return project_root