"""AI Provider Registry.

Provides provider lookup by name. Currently only 'mock' is active.
Other providers (kilocode, opencodego, nvidia, deepseek, mistral, ollama)
are registered as placeholders and return not-implemented responses.

No external API calls are made by this module.
No credentials are stored or referenced.
"""

from padiem_ai.ai.providers import MockProvider, PlaceholderProvider

# Supported provider names (lowercase)
SUPPORTED_PROVIDERS = [
    "mock",
    "kilocode",
    "opencodego",
    "nvidia",
    "deepseek",
    "mistral",
    "ollama",
]

# Default provider
DEFAULT_PROVIDER = "mock"

# Active providers (actually implemented)
_ACTIVE_PROVIDERS = {"mock"}

# Placeholder providers (registered but not implemented)
_PLACEHOLDER_PROVIDERS = {"kilocode", "opencodego", "nvidia", "deepseek", "mistral", "ollama"}


def _normalize(name: str) -> str:
    """Normalize provider name to lowercase."""
    return name.strip().lower()


def get_provider(provider_name: str = None):
    """Get a provider instance by name.

    Args:
        provider_name: Provider name (case-insensitive). Defaults to DEFAULT_PROVIDER.

    Returns:
        BaseAIProvider instance (MockProvider or PlaceholderProvider).

    Raises:
        ValueError: If provider name is not in SUPPORTED_PROVIDERS.
    """
    if provider_name is None:
        provider_name = DEFAULT_PROVIDER

    name = _normalize(provider_name)

    if name not in SUPPORTED_PROVIDERS:
        raise ValueError(
            f"Unknown provider: '{provider_name}'. "
            f"Supported providers: {', '.join(SUPPORTED_PROVIDERS)}"
        )

    if name in _ACTIVE_PROVIDERS:
        return MockProvider()

    # Placeholder provider
    return PlaceholderProvider(name)


def list_providers() -> list:
    """List all supported provider names.

    Returns:
        List of provider name strings (lowercase).
    """
    return list(SUPPORTED_PROVIDERS)


def is_provider_available(provider_name: str) -> bool:
    """Check if a provider name is in the supported list.

    Args:
        provider_name: Provider name (case-insensitive).

    Returns:
        True if the provider is supported (active or placeholder).
    """
    return _normalize(provider_name) in SUPPORTED_PROVIDERS


def get_default_provider():
    """Get the default provider instance.

    Returns:
        MockProvider instance.
    """
    return get_provider(DEFAULT_PROVIDER)
