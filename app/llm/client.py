"""
Wrapper for talking to a local LLM (Ollama by default).
app/llm/client.py

Isolates all the HTTP/requests-library details here so the rest of
the app just calls ask_llm(prompt) and gets text back, without
knowing or caring whether it's Ollama, LM Studio, or something else.

Requires the `requests` library: pip install requests
"""
import requests

from app.core.config import settings
from app.core.exceptions import LLMConnectionError, LLMResponseError


def ask_llm(prompt: str) -> str:
    """
    Sends a prompt to the local LLM and returns its text response.

    Args:
        prompt: the full prompt text to send.

    Returns:
        The model's response as a plain string.

    Raises:
        LLMConnectionError: if the local server can't be reached at all
                             (e.g. Ollama isn't running).
        LLMResponseError: if the server responds but the response can't
                           be parsed as expected.
    """
    url = f"{settings.llm_base_url}/api/generate"

    payload = {
        "model": settings.llm_model,
        "prompt": prompt,
        "stream": False,  # get one full response instead of a token stream
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        # Most common case: Ollama isn't running locally.
        raise LLMConnectionError(
            f"Could not connect to local LLM at {url}. "
            f"Is Ollama running? (ollama serve)"
        ) from e
    except requests.exceptions.RequestException as e:
        raise LLMConnectionError(f"LLM request failed: {e}") from e

    try:
        data = response.json()
        return data["response"]
    except (KeyError, ValueError) as e:
        raise LLMResponseError(f"Unexpected LLM response format: {e}") from e