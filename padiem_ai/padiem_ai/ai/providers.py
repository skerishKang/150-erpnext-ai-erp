"""Compatibility facade for AI provider implementations.

Provider classes live in provider-specific modules under
`padiem_ai.ai.provider_modules`. Keep this module as the stable import surface
for existing code such as `from padiem_ai.ai.providers import MockProvider`.
"""

from padiem_ai.ai.provider_modules import (
    DeepSeekProvider,
    MockProvider,
    PlaceholderProvider,
)

__all__ = [
    "DeepSeekProvider",
    "MockProvider",
    "PlaceholderProvider",
]
