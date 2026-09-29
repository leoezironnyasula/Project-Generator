"""
API route definitions.
app/api/routes.py

All the actual endpoint logic lives here now, instead of directly in
main.py. main.py's only job becomes creating the app, setting up
CORS, and including this router -- the standard FastAPI pattern once
an app has more than a couple of routes.
"""
from fastapi import APIRouter, HTTPException, Query

from app.generator.idea_generator import generate_random_project
from app.generator.constraints import GenerationConstraints
from app.scaffolder.builder import scaffold_project
from app.core.config import settings
from app.core.exceptions import ScaffoldError
from app.models.project import Domain, Difficulty

# APIRouter groups related routes together. main.py mounts this
# whole group onto the app with a single app.include_router() call.
router = APIRouter()


def _generate_with_constraints(domain: Domain | None, difficulty: Difficulty | None):
    """
    Generates a project, retrying a limited number of times if
    constraints are given and the result doesn't match.
    """
    constraints = GenerationConstraints(domain=domain, difficulty=difficulty)
    max_attempts = 10

    for _ in range(max_attempts):
        project = generate_random_project()
        if constraints.matches(project):
            return project

    raise HTTPException(
        status_code=404,
        detail=f"Could not generate a project matching domain={domain}, difficulty={difficulty} "
               f"after {max_attempts} attempts. Try loosening the constraints.",
    )


@router.get("/health")
def health_check() -> dict:
    """Basic health check endpoint."""
    return {"status": "ok"}


@router.get("/generate")
def generate_project(
    domain: Domain | None = Query(default=None),
    difficulty: Difficulty | None = Query(default=None),
) -> dict:
    """
    Generates one random project idea and returns it as JSON.
    Optionally filter by domain and/or difficulty via query params,
    e.g. /generate?domain=cli&difficulty=beginner
    """
    project = _generate_with_constraints(domain, difficulty)
    return project.as_dict()


@router.post("/scaffold")
def scaffold_new_project(
    domain: Domain | None = Query(default=None),
    difficulty: Difficulty | None = Query(default=None),
) -> dict:
    """
    Generates a random project (optionally filtered) AND creates its
    starter folder on disk.
    """
    project = _generate_with_constraints(domain, difficulty)

    try:
        created_path = scaffold_project(project, base_path=settings.default_output_dir)
    except ScaffoldError as e:
        raise HTTPException(status_code=500, detail=f"Failed to scaffold project: {e}")

    return {
        "project": project.as_dict(),
        "created_at": str(created_path.resolve()),
    }