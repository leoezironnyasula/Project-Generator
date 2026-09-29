"""
Entry point for the backend.
app/main.py

Now just wires everything together: creates the app, sets up CORS,
and mounts the routes defined in app/api/routes.py. All the actual
endpoint logic lives in that file, not here.

Run with:
    uvicorn app.main:app --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

app = FastAPI(title="Project Generator Backend")

# Allows a frontend on a different origin (e.g. your PyWebView UI) to
# call this API. "*" = any origin, fine for local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all routes from routes.py onto the app.
app.include_router(router)