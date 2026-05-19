"""Placeholder AI provider implementation."""

from padiem_ai.ai.base import BaseAIProvider


class PlaceholderProvider(BaseAIProvider):
    """Placeholder for future providers — never makes external calls.

    Used for: kilocode, opencodego, nvidia, mistral, ollama
    and any other provider registered before implementation.
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
