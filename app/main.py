"""
Entry point for the backend.
app/main.py

Runs a FastAPI server with two routes:
- GET /health    -> simple check that the server is alive
- GET /generate  -> returns one randomly generated Project as JSON

Run with:
    uvicorn app.main:app --reload
"""
from fastapi import FastAPI

from app.generator.idea_generator import generate_random_project

# Create the FastAPI application instance.
# This "app" object is what uvicorn looks for when we run the server.
app = FastAPI(title="Project Generator Backend")


@app.get("/health")
def health_check() -> dict:
    """
    Basic health check endpoint.
    Lets us (or the frontend) confirm the backend is running
    without needing to trigger any real logic.
    """
    return {"status": "ok"}


@app.get("/generate")
def generate_project() -> dict:
    """
    Generates one random project idea and returns it as JSON.

    Right now this pulls from the hardcoded sample list in
    idea_generator.py. Later, this same route will return LLM-generated
    projects instead — the route itself won't need to change, since
    generate_random_project() always returns a Project object,
    and .as_dict() always turns it into the same JSON shape.
    """
    project = generate_random_project()
    return project.as_dict()