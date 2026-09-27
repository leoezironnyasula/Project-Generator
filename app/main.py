"""
Entry point for the backend.
app/main.py

Routes:
- GET  /health     -> simple check that the server is alive
- GET  /generate   -> returns one randomly generated Project as JSON
                       (optional query params: domain, difficulty)
- POST /scaffold   -> generates a project AND creates its folder on disk
                       (same optional query params)
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.generator.idea_generator import generate_random_project
from app.generator.constraints import GenerationConstraints
from app.scaffolder.builder import scaffold_project
from app.core.config import settings
from app.core.exceptions import ScaffoldError
from app.models.project import Domain, Difficulty

app = FastAPI(title="Project Generator Backend")

# CORS: allows a frontend running on a different origin (e.g. an
# Electron app, or a dev server on a different port) to actually call
# this API. "*" means "allow any origin" -- fine for local development,
# but tighten this to your actual frontend's origin before shipping
# anything beyond your own machine.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _generate_with_constraints(domain: Domain | None, difficulty: Difficulty | None):
    """
    Generates a project, retrying a limited number of times if
    constraints are given and the result doesn't match.

    NOTE: with only 3 hardcoded fallback templates, narrow constraints
    (e.g. domain=game) may never match and will exhaust retries --
    that's expected until more templates exist or the LLM path
    respects constraints directly (it doesn't yet).
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


@app.get("/health")
def health_check() -> dict:
    """Basic health check endpoint."""
    return {"status": "ok"}


@app.get("/generate")
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


@app.post("/scaffold")
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
        # Clean error instead of a raw 500 stack trace.
        raise HTTPException(status_code=500, detail=f"Failed to scaffold project: {e}")

    return {
        "project": project.as_dict(),
        "created_at": str(created_path.resolve()),
    }