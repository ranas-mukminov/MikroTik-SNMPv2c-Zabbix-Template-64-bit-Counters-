import types

import pytest

from ai_providers import openai_provider


class _DummyChatCompletion:
    @staticmethod
    def create(**_kwargs):  # pragma: no cover - trivial stub
        return {"choices": [{"message": {"content": "ok"}}]}


class _DummyOpenAI(types.SimpleNamespace):
    ChatCompletion = _DummyChatCompletion
    api_key: str | None = None


def test_openai_provider_requires_openai_package(monkeypatch):
    monkeypatch.setattr(openai_provider, "openai", None)
    provider = openai_provider.OpenAIProvider(api_key="dummy-key")

    with pytest.raises(RuntimeError, match="openai package is not installed"):
        provider.generate_cost_optimization_report({"scenario": "baseline"})


def test_openai_provider_requires_api_key(monkeypatch):
    monkeypatch.setattr(openai_provider, "openai", _DummyOpenAI())
    provider = openai_provider.OpenAIProvider(api_key=None)

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY is not configured"):
        provider.generate_blueprint_suggestions({"topology": "lab"})
