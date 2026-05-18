"""Base AI Provider interface.

This is a concept-only skeleton. Actual implementation comes in a later PR.
"""


class BaseAIProvider:
    """Abstract base class for AI providers."""

    def generate_text(self, prompt: str, context: dict, options: dict = None) -> str:
        raise NotImplementedError

    def generate_json(self, prompt: str, context: dict, schema: dict = None, options: dict = None) -> dict:
        raise NotImplementedError

    def summarize(self, context: dict, prompt_template: str = "") -> str:
        raise NotImplementedError

    def health_check(self) -> dict:
        raise NotImplementedError

    def get_provider_name(self) -> str:
        raise NotImplementedError
