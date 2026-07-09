"""
Ollama client for LearnPath AI.

Responsible only for talking to the local LLM.
"""

import requests


class OllamaClient:

    def __init__(
        self,
        model: str = "llama3.2:3b",
        host: str = "http://localhost:11434",
    ):
        self.model = model
        self.host = host

    def generate(self, prompt: str) -> str:

        response = requests.post(
            f"{self.host}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        return response.json()["response"]


_client = OllamaClient()


def generate_response(prompt: str) -> str:
    return _client.generate(prompt)