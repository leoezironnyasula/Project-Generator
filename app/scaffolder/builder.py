"""
Builds a folder/file structure on disk for a given Project.
app/scaffolder/builder.py

UPDATED: all 7 domains now have real starter templates (previously
only CLI, WEB_API, and AUTOMATION did -- the other 4 fell back to a
generic layout).
"""
from pathlib import Path

from app.models.project import Project, Domain
from app.core.exceptions import ScaffoldError

# Each domain maps to a dict of {subfolder: [files]}.
# "" means the project root itself.
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
    Domain.WEB_FRONTEND: {
        "": ["index.html", "style.css", "script.js", "README.md"],
    },
    Domain.DESKTOP_APP: {
        "": ["main.py", "requirements.txt", "README.md"],
        "ui": [],  # empty folder for UI assets/files, filled in as the project grows
    },
    Domain.DATA: {
        "": ["main.py", "requirements.txt", "README.md"],
        "data": [],       # raw/input data files go here
        "notebooks": [],  # exploratory analysis notebooks go here
    },
    Domain.GAME: {
        "": ["main.py", "requirements.txt", "README.md"],
        "assets": [],  # sprites, sounds, etc.
    },
}


def scaffold_project(project: Project, base_path: str = ".") -> Path:
    """
    Creates a starter folder structure for the given project, using
    the template that matches its domain. Every Domain now has a real
    template, so the old generic fallback is kept only as a safety
    net in case a new Domain is ever added without updating this dict.
    """
    folder_name = project.title.lower().replace(" ", "-")
    project_root = Path(base_path) / folder_name

    template = DOMAIN_TEMPLATES.get(project.domain, {"": ["main.py", "README.md"]})

    try:
        for subfolder, files in template.items():
            folder_path = project_root / subfolder
            # mkdir happens even for empty-file-list folders (e.g. "assets"),
            # so the folder itself still gets created.
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
        raise ScaffoldError(f"Could not create project files at {project_root}: {e}") from e

    return project_root