"""Mock AI Provider for development and testing.

Returns deterministic responses without any external API calls.
"""

from padiem_ai.padiem_ai.ai.base import BaseAIProvider


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
