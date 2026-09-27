"""
Entry point for the desktop frontend.
frontend/main.py

Opens a native window loading our simple HTML/CSS/JS UI.
Requires: pip install pywebview
Run with: python main.py
(Your FastAPI backend must be running separately on port 8000.)
"""
import webview
from pathlib import Path

INDEX_PATH = Path(__file__).parent / "ui" / "index.html"

webview.create_window(
    title="Project Generator",
    url=str(INDEX_PATH),
    width=700,
    height=550,
)
webview.start()