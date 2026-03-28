"""Ollama provider for local LLM inference."""

import os
import json
import yaml
import requests
from ai_providers_core.base import BaseProvider


class OllamaProvider(BaseProvider):
    """Provider for local Ollama LLM inference.
    
    Features:
    - Runs completely locally (no API calls, no internet required)
    - Supports any model in Ollama library
    - Zero cost (beyond initial model download)
    - Fast inference on local hardware
    """

    def __init__(self):
        """Initialize Ollama provider."""
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.spec_model = os.getenv("OLLAMA_SPEC_MODEL", "qwen2.5-coder:14b")
        self.proc_model = os.getenv("OLLAMA_PROC_MODEL", "qwen2.5-coder:14b")
        self.timeout = int(os.getenv("OLLAMA_TIMEOUT", "300"))

        # Validate connection
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                raise ConnectionError(f"Ollama returned {response.status_code}")
        except Exception as e:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self.base_url}. "
                f"Is it running? Start with: ollama serve\n{e}"
            )

    def generate_spec(self, user_message: str) -> str:
        """Generate specification using Ollama.

        Args:
            user_message: Code snippet or description

        Returns:
            YAML specification
        """
        return self._call_ollama(
            user_message,
            self.spec_model,
            system_prompt=(
                "You are an expert GeneXus specification generator. "
                "Convert code into a detailed YAML specification. "
                "Return ONLY valid YAML, no markdown, no explanations."
            ),
        )

    def generate_procedure(self, spec: str) -> str:
        """Generate procedure from specification using Ollama.

        Args:
            spec: YAML specification

        Returns:
            GeneXus procedure code
        """
        return self._call_ollama(
            spec,
            self.proc_model,
            system_prompt=(
                "You are an expert GeneXus procedure generator. "
                "Convert specifications into GeneXus procedure code. "
                "Return ONLY valid GeneXus code, no markdown, no explanations."
            ),
        )

    def _call_ollama(self, message: str, model: str, system_prompt: str) -> str:
        """Call Ollama API with streaming."""
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": model,
            "prompt": message,
            "system": system_prompt,
            "stream": False,
            "temperature": 0.7,
            "top_p": 0.9,
        }

        try:
            response = requests.post(
                url, json=payload, timeout=self.timeout, headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            result = response.json()
            response_text = result.get("response", "").strip()

            # Remove markdown code blocks if present
            response_text = self._remove_markdown_markers(response_text)

            return response_text

        except requests.exceptions.Timeout:
            raise TimeoutError(
                f"Ollama request timed out after {self.timeout}s. "
                f"Try increasing OLLAMA_TIMEOUT environment variable."
            )
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self.base_url}. "
                f"Is it running? Start with: ollama serve\n{e}"
            )
        except Exception as e:
            raise RuntimeError(f"Ollama API error: {e}")

    @staticmethod
    def _remove_markdown_markers(text: str) -> str:
        """Remove markdown code block markers."""
        if text.startswith("```"):
            # Remove opening ```language
            lines = text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines).strip()
        return text


# Auto-register this provider
def register():
    """Register Ollama provider with factory."""
    from ai_providers_core.factory import ProviderFactory

    ProviderFactory.register("ollama", OllamaProvider)
