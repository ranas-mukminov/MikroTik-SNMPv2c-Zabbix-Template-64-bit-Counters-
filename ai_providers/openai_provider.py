from __future__ import annotations

import os
from typing import Any, Dict

from .base import AIProvider

try:
    import openai
except ImportError:  # pragma: no cover - optional dependency
    openai = None


class OpenAIProvider(AIProvider):
    """Example provider using OpenAI's Chat Completions API."""

    def __init__(self, model: str = "gpt-4o-mini", api_key: str | None = None) -> None:
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def _ensure_client(self) -> None:
        if openai is None:
            raise RuntimeError("openai package is not installed")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")
        openai.api_key = self.api_key

    def generate_blueprint_suggestions(self, payload: Dict[str, Any]) -> str:
        self._ensure_client()
        response = openai.ChatCompletion.create(  # type: ignore[attr-defined]
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an IaC assistant."},
                {"role": "user", "content": f"Suggest improvements: {payload}"},
            ],
            temperature=0.3,
        )
        return response["choices"][0]["message"]["content"].strip()

    def generate_cost_optimization_report(self, payload: Dict[str, Any]) -> str:
        self._ensure_client()
        response = openai.ChatCompletion.create(  # type: ignore[attr-defined]
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a FinOps assistant."},
                {"role": "user", "content": f"Summarize results: {payload}"},
            ],
            temperature=0.4,
        )
        return response["choices"][0]["message"]["content"].strip()
