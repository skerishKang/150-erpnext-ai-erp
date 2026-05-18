"""AI Provider Configuration Guard.

Provides safe configuration checks for AI providers.
Default: mock provider only, external calls disabled, no credentials required.

No external AI calls. No credentials stored or referenced.
"""


# Default provider configuration
# Real providers are disabled by default and require explicit enable + credentials
_PROVIDER_DEFAULTS = {
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
_SELECTED_PROVIDER = "mock"


def get_selected_provider_name() -> str:
    """Get the currently selected provider name.

    Returns:
        str: Provider name (default: "mock")
    """
    return _SELECTED_PROVIDER


def is_external_ai_enabled() -> bool:
    """Check if external AI calls are enabled in the current environment.

    Returns:
        bool: True if external AI calls are allowed, False otherwise.
              Default: False (mock only)
    """
    return False


def get_provider_config_status(provider_name: str) -> dict:
    """Get the configuration status of a provider.

    Args:
        provider_name: Provider name to check

    Returns:
        dict: Provider configuration status
    """
    name = provider_name.strip().lower()
    defaults = _PROVIDER_DEFAULTS.get(name)

    if defaults is None:
        return {
            "provider": name,
            "is_mock": False,
            "enabled": False,
            "external_call_allowed": False,
            "credentials_present": False,
            "status": "unknown_provider",
        }

    is_mock = defaults["is_mock"]
    enabled = defaults["enabled"]
    external_call_allowed = defaults["external_call_allowed"]
    requires_credentials = defaults["requires_credentials"]

    # Mock provider never needs credentials
    if is_mock:
        return {
            "provider": name,
            "is_mock": True,
            "enabled": True,
            "external_call_allowed": False,
            "credentials_present": False,
            "status": "ok",
        }

    # Real providers: check if enabled and credentials present
    if not enabled:
        return {
            "provider": name,
            "is_mock": False,
            "enabled": False,
            "external_call_allowed": False,
            "credentials_present": False,
            "status": "disabled_not_enabled",
        }

    # If enabled but requires credentials (placeholder — no actual credential check)
    if requires_credentials:
        return {
            "provider": name,
            "is_mock": False,
            "enabled": True,
            "external_call_allowed": False,
            "credentials_present": False,
            "status": "disabled_missing_config",
        }

    # Ollama-style: no credentials needed but still disabled by default
    return {
        "provider": name,
        "is_mock": False,
        "enabled": False,
        "external_call_allowed": False,
        "credentials_present": False,
        "status": "disabled_not_enabled",
    }


def assert_provider_allowed(provider_name: str) -> None:
    """Assert that a provider is allowed to make calls.

    Raises ValueError if the provider is not allowed.

    Args:
        provider_name: Provider name to check

    Raises:
        ValueError: If provider is not allowed (disabled, missing config, unknown)
    """
    status = get_provider_config_status(provider_name)

    if status["status"] == "ok":
        return

    if status["status"] == "unknown_provider":
        raise ValueError(f"Unknown provider: {provider_name}")

    if status["status"] == "disabled_not_enabled":
        raise ValueError(
            f"Provider '{provider_name}' is not enabled. "
            f"Set enabled=True in provider config to use this provider."
        )

    if status["status"] == "disabled_missing_config":
        raise ValueError(
            f"Provider '{provider_name}' is missing required configuration. "
            f"Provide the required credentials before using this provider."
        )

    raise ValueError(f"Provider '{provider_name}' is not allowed (status: {status['status']})")


# -- DeepSeek-specific helpers ------------------------------------------------

_DEEPSEEK_DEFAULT_BASE_URL = "https://api.deepseek.com/v1"
_DEEPSEEK_DEFAULT_MODEL = "deepseek-chat"


def _get_deepseek_env_var(name: str) -> str:
    """Read a DeepSeek config value from environment variables.

    Returns empty string if not set. Never logs or exposes the value.
    """
    import os
    return os.environ.get(name, "")


def get_deepseek_config() -> dict:
    """Get DeepSeek configuration from environment.

    Expected env vars (documented only, never committed with values):
        PA_DIEM_DEEPSEEK_API_KEY   — API key for DeepSeek
        PA_DIEM_DEEPSEEK_BASE_URL  — override base URL (optional)
        PA_DIEM_DEEPSEEK_MODEL     — model name (optional)

    Returns:
        dict with keys: api_key_present, base_url, model, external_call_allowed
        api_key_present is bool (True if env var is non-empty)
        base_url defaults to https://api.deepseek.com/v1
        model defaults to deepseek-chat
    """
    api_key = _get_deepseek_env_var("PA_DIEM_DEEPSEEK_API_KEY")
    base_url = _get_deepseek_env_var("PA_DIEM_DEEPSEEK_BASE_URL") or _DEEPSEEK_DEFAULT_BASE_URL
    model = _get_deepseek_env_var("PA_DIEM_DEEPSEEK_MODEL") or _DEEPSEEK_DEFAULT_MODEL

    return {
        "api_key_present": bool(api_key),
        "base_url": base_url,
        "model": model,
        "external_call_allowed": False,
    }
