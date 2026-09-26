"""
Builds a folder/file structure on disk for a given Project.
app/scaffolder/builder.py

This takes a Project object (from idea_generator) and creates
an actual starter directory for it, so the user gets a ready-to-open
folder instead of just an idea on screen.
"""
from pathlib import Path

from app.models.project import Project, Domain

# Maps each Domain to a basic starter layout.
# Keys are folder paths (relative to the new project root),
# values are lists of starter files to create inside that folder.
# This is intentionally simple for now — one flat template per domain.
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

    Args:
        project: the Project to scaffold (title, domain, etc.)
        base_path: where to create the new project folder (defaults to
                    the current directory)

    Returns:
        The Path to the newly created project folder.
    """
    # Turn the project title into a safe folder name.
    # e.g. "Local Notes API" -> "local-notes-api"
    folder_name = project.title.lower().replace(" ", "-")
    project_root = Path(base_path) / folder_name

    # Look up the template for this project's domain.
    # Fall back to a minimal generic layout if the domain has no
    # template defined yet (keeps this from crashing on new domains).
    template = DOMAIN_TEMPLATES.get(project.domain, {"": ["main.py", "README.md"]})

    for subfolder, files in template.items():
        folder_path = project_root / subfolder
        folder_path.mkdir(parents=True, exist_ok=True)

        for filename in files:
            file_path = folder_path / filename
            file_path.touch(exist_ok=True)

    # Write a starter README with the project's own description,
    # so the folder isn't just empty scaffolding.
    readme_path = project_root / "README.md"
    readme_path.write_text(
        f"# {project.title}\n\n"
        f"{project.description}\n\n"
        f"**Tech stack:** {project.tech_stack.summary()}\n\n"
        f"**Features:**\n" + "\n".join(f"- {f}" for f in project.features)
    )

    return project_root