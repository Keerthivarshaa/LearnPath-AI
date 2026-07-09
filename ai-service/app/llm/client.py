"""
LLM Client - LearnPath AI

Responsible only for communicating with the language model.

The rest of the application (Prompt Builder, AI Tutor, FastAPI routes)
should never call Ollama directly. They should always go through this
client so that the backend can easily switch to another provider
(OpenAI, Gemini, Claude, etc.) in the future.
"""

from typing import Optional

import requests


class LLMClient:
    """
    Handles communication with the configured LLM backend.

    Currently supports:
        - Ollama (local SLM)

    Future:
        - OpenAI
        - Gemini
        - Claude
        - Azure OpenAI
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.2:3b",
        timeout: int = 120,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def generate(self, prompt: str) -> str:
        """
        Sends a prompt to the configured language model.

        Returns:
            Generated response text.

        Raises:
            RuntimeError if the model cannot be reached.
        """

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()

            data = response.json()

            return data.get(
                "response",
                "No response generated."
            )

        except requests.exceptions.RequestException as exc:
            raise RuntimeError(
                "Unable to connect to the configured LLM. "
                "Ensure Ollama is running."
            ) from exc


_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """
    Singleton accessor.
    """

    global _client

    if _client is None:
        _client = LLMClient()

    return _client