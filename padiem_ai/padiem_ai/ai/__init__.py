"""AI provider abstraction layer.

Exports:
- BaseAIProvider: abstract interface
- MockProvider: active dev/test provider
- PlaceholderProvider: stub for future providers
- get_provider: provider lookup by name
- list_providers: list supported provider names
- is_provider_available: check if provider name is supported
- get_default_provider: get mock provider instance
"""

from padiem_ai.ai.base import BaseAIProvider
from padiem_ai.ai.providers import MockProvider, PlaceholderProvider
from padiem_ai.ai.registry import (
    get_provider,
    list_providers,
    is_provider_available,
    get_default_provider,
)
