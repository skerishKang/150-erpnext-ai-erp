"""AI provider implementations.

Contains:
- MockProvider: active provider for dev/test (from PR #20)
- PlaceholderProvider: stub for future providers (no external calls)
"""

from padiem_ai.ai.base import BaseAIProvider


class MockProvider(BaseAIProvider):
    """Mock provider — no external calls, deterministic responses."""

    def generate_text(self, prompt: str, context: dict, options: dict = None) -> str:
        return "Mock response: AI integration pending."

    def generate_json(self, prompt: str, context: dict, schema: dict = None, options: dict = None) -> dict:
        return {"summary": "Mock summary", "alerts": []}

    def summarize(self, context: dict, prompt_template: str = "") -> str:
        return "Mock summary: AI integration pending."

    def health_check(self) -> dict:
        return {"status": "ok", "provider": "mock", "latency_ms": 0}

    def get_provider_name(self) -> str:
        return "mock"


class PlaceholderProvider(BaseAIProvider):
    """Placeholder for future providers — never makes external calls.

    Used for: kilocode, opencodego, nvidia, deepseek, mistral, ollama
    These providers are registered but not yet implemented.
    """

    def __init__(self, name: str):
        self._name = name

    def generate_text(self, prompt: str, context: dict, options: dict = None) -> str:
        raise NotImplementedError(
            f"Provider '{self._name}' is not yet implemented. "
            f"Use 'mock' provider for development and testing."
        )

    def generate_json(self, prompt: str, context: dict, schema: dict = None, options: dict = None) -> dict:
        raise NotImplementedError(
            f"Provider '{self._name}' is not yet implemented. "
            f"Use 'mock' provider for development and testing."
        )

    def summarize(self, context: dict, prompt_template: str = "") -> str:
        raise NotImplementedError(
            f"Provider '{self._name}' is not yet implemented. "
            f"Use 'mock' provider for development and testing."
        )

    def health_check(self) -> dict:
        return {
            "status": "not_implemented",
            "provider": self._name,
            "message": f"Provider '{self._name}' is registered but not yet implemented.",
        }

    def get_provider_name(self) -> str:
        return self._name
