"""Default AI provider configuration."""

# Real providers are disabled by default and require explicit enable + credentials.
PROVIDER_DEFAULTS = {
    "mock": {
        "is_mock": True,
        "enabled": True,
        "external_call_allowed": False,
        "requires_credentials": False,
    },
    "deepseek": {
        "is_mock": False,
        "enabled": False,
        "external_call_allowed": False,
        "requires_credentials": True,
    },
    "kilocode": {
        "is_mock": False,
        "enabled": False,
        "external_call_allowed": False,
        "requires_credentials": True,
    },
    "opencodego": {
        "is_mock": False,
        "enabled": False,
        "external_call_allowed": False,
        "requires_credentials": True,
    },
    "nvidia": {
        "is_mock": False,
        "enabled": False,
        "external_call_allowed": False,
        "requires_credentials": True,
    },
    "mistral": {
        "is_mock": False,
        "enabled": False,
        "external_call_allowed": False,
        "requires_credentials": True,
    },
    "ollama": {
        "is_mock": False,
        "enabled": False,
        "external_call_allowed": False,
        "requires_credentials": False,
    },
}

# Current selected provider (default: mock)
SELECTED_PROVIDER = "mock"


def get_selected_provider_name() -> str:
    """Get the currently selected provider name."""
    return SELECTED_PROVIDER
