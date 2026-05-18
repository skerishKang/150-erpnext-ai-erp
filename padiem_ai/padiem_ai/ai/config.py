"""AI Provider Configuration Guard.

Provides safe configuration checks for AI providers.
Default: mock provider only, external calls disabled, no credentials required.

Enablement chain for DeepSeek (all must be true):
    PA_DIEM_ENABLE_EXTERNAL_AI=true   — master switch for all external AI
    PA_DIEM_DEEPSEEK_ENABLED=true      — per-provider enable flag
    PA_DIEM_DEEPSEEK_API_KEY           — credential must be present

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


def _get_env_bool(name: str) -> bool:
    """Read a boolean environment variable. Defaults to False."""
    import os
    val = os.environ.get(name, "").strip().lower()
    return val in ("1", "true", "yes", "on")


def _get_env_str(name: str) -> str:
    """Read a string environment variable. Defaults to empty string."""
    import os
    return os.environ.get(name, "")


def get_selected_provider_name() -> str:
    """Get the currently selected provider name.

    Returns:
        str: Provider name (default: "mock")
    """
    return _SELECTED_PROVIDER


def is_external_ai_enabled() -> bool:
    """Check if external AI calls are enabled in the current environment.

    Reads PA_DIEM_ENABLE_EXTERNAL_AI env var.
    Default: False (mock only)

    Returns:
        bool: True if external AI calls are allowed, False otherwise.
    """
    return _get_env_bool("PA_DIEM_ENABLE_EXTERNAL_AI")


def is_deepseek_enabled() -> bool:
    """Check if DeepSeek provider is explicitly enabled.

    Reads PA_DIEM_DEEPSEEK_ENABLED env var.
    Default: False

    Returns:
        bool: True if DeepSeek is enabled, False otherwise.
    """
    return _get_env_bool("PA_DIEM_DEEPSEEK_ENABLED")


def get_provider_config_status(provider_name: str) -> dict:
    """Get the configuration status of a provider.

    For DeepSeek, checks env vars:
        PA_DIEM_DEEPSEEK_ENABLED — overrides enabled flag
        PA_DIEM_DEEPSEEK_API_KEY — checked for credentials_present

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
    requires_credentials = defaults["requires_credentials"]

    # Override enabled from env for deepseek
    if name == "deepseek":
        enabled = is_deepseek_enabled()

    # Check credential presence for deepseek
    credentials_present = False
    if name == "deepseek":
        credentials_present = bool(_get_env_str("PA_DIEM_DEEPSEEK_API_KEY"))

    # Determine external_call_allowed: master switch + provider enabled
    external_call_allowed = is_external_ai_enabled() and enabled

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

    # Real providers: check if enabled
    if not enabled:
        return {
            "provider": name,
            "is_mock": False,
            "enabled": False,
            "external_call_allowed": False,
            "credentials_present": credentials_present,
            "status": "disabled_not_enabled",
        }

    # If enabled but requires credentials, check presence
    if requires_credentials and not credentials_present:
        return {
            "provider": name,
            "is_mock": False,
            "enabled": True,
            "external_call_allowed": False,
            "credentials_present": False,
            "status": "disabled_missing_config",
        }

    # Enabled, credentials present (or not required), but master switch off
    if not is_external_ai_enabled():
        return {
            "provider": name,
            "is_mock": False,
            "enabled": True,
            "external_call_allowed": False,
            "credentials_present": credentials_present,
            "status": "disabled_external_ai_off",
        }

    # Fully enabled
    return {
        "provider": name,
        "is_mock": False,
        "enabled": True,
        "external_call_allowed": True,
        "credentials_present": credentials_present,
        "status": "ok",
    }


def assert_provider_allowed(provider_name: str) -> None:
    """Assert that a provider is allowed to make calls.

    Raises ValueError if the provider is not allowed (disabled, missing config, unknown).

    Args:
        provider_name: Provider name to check

    Raises:
        ValueError: If provider is not allowed
    """
    status = get_provider_config_status(provider_name)

    if status["status"] == "ok":
        return

    if status["status"] == "unknown_provider":
        raise ValueError(f"Unknown provider: {provider_name}")

    if status["status"] == "disabled_not_enabled":
        raise ValueError(
            f"Provider '{provider_name}' is not enabled. "
            f"Set PA_DIEM_DEEPSEEK_ENABLED=true to enable."
        )

    if status["status"] == "disabled_missing_config":
        raise ValueError(
            f"Provider '{provider_name}' is missing required configuration. "
            f"Set PA_DIEM_DEEPSEEK_API_KEY before using this provider."
        )

    if status["status"] == "disabled_external_ai_off":
        raise ValueError(
            f"Provider '{provider_name}' is enabled but external AI is off. "
            f"Set PA_DIEM_ENABLE_EXTERNAL_AI=true to allow external calls."
        )

    raise ValueError(f"Provider '{provider_name}' is not allowed (status: {status['status']})")


# -- DeepSeek-specific helpers ------------------------------------------------

_DEEPSEEK_DEFAULT_BASE_URL = "https://api.deepseek.com/v1"
_DEEPSEEK_DEFAULT_MODEL = "deepseek-chat"


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
        external_call_allowed requires both PA_DIEM_ENABLE_EXTERNAL_AI and PA_DIEM_DEEPSEEK_ENABLED
    """
    api_key = _get_env_str("PA_DIEM_DEEPSEEK_API_KEY")
    base_url = _get_env_str("PA_DIEM_DEEPSEEK_BASE_URL") or _DEEPSEEK_DEFAULT_BASE_URL
    model = _get_env_str("PA_DIEM_DEEPSEEK_MODEL") or _DEEPSEEK_DEFAULT_MODEL

    return {
        "api_key_present": bool(api_key),
        "base_url": base_url,
        "model": model,
        "external_call_allowed": is_external_ai_enabled() and is_deepseek_enabled() and bool(api_key),
    }
