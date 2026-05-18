"""AI Provider Registry.

Provides provider lookup by name. Currently 'mock' and 'deepseek' are active.
Other providers (kilocode, opencodego, nvidia, mistral, ollama)
are registered as placeholders and return not-implemented responses.

No external API calls are made by this module.
No credentials are stored or referenced.
"""

from padiem_ai.ai.providers import MockProvider, DeepSeekProvider, PlaceholderProvider

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

# Active providers (actually implemented and enabled)
_ACTIVE_PROVIDERS = {"mock"}

# Skeleton providers (structurally present but disabled by default)
_SKELETON_PROVIDERS = {"deepseek"}

# Placeholder providers (registered but not implemented)
_PLACEHOLDER_PROVIDERS = {"kilocode", "opencodego", "nvidia", "mistral", "ollama"}


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

    if name == "deepseek":
        return DeepSeekProvider()

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


def get_provider_config_status(provider_name: str) -> str:
    """Get the configuration status of a provider.

    Args:
        provider_name: Provider name (case-insensitive).

    Returns:
        Status string: "enabled", "disabled_not_enabled", "not_implemented".
    """
    name = _normalize(provider_name)

    if name not in SUPPORTED_PROVIDERS:
        return "unknown"

    if name in _ACTIVE_PROVIDERS:
        return "enabled"

    if name in _SKELETON_PROVIDERS:
        return "disabled_not_enabled"

    return "not_implemented"


def assert_provider_allowed(provider_name: str) -> None:
    """Assert that a provider is allowed to be used.

    Raises:
        ValueError: If the provider is not implemented (placeholder) or disabled.
    """
    name = _normalize(provider_name)
    status = get_provider_config_status(name)

    if status == "not_implemented":
        raise ValueError(
            f"Provider '{provider_name}' is not yet implemented. "
            f"Use 'mock' provider for development and testing."
        )

    if status == "disabled_not_enabled":
        raise ValueError(
            f"Provider '{provider_name}' is disabled and not enabled. "
            f"DeepSeek provider requires explicit enablement."
        )

    if status == "unknown":
        raise ValueError(
            f"Unknown provider: '{provider_name}'. "
            f"Supported providers: {', '.join(SUPPORTED_PROVIDERS)}"
        )
