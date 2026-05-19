"""Provider configuration status and guard helpers."""

from padiem_ai.ai.config_modules.defaults import PROVIDER_DEFAULTS
from padiem_ai.ai.config_modules.env import get_env_bool, get_env_str


def is_external_ai_enabled() -> bool:
    """Check if external AI calls are enabled in the current environment."""
    return get_env_bool("PA_DIEM_ENABLE_EXTERNAL_AI")


def is_deepseek_enabled() -> bool:
    """Check if DeepSeek provider is explicitly enabled."""
    return get_env_bool("PA_DIEM_DEEPSEEK_ENABLED")


def get_provider_config_status(provider_name: str) -> dict:
    """Get the configuration status of a provider."""
    name = provider_name.strip().lower()
    defaults = PROVIDER_DEFAULTS.get(name)

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

    if name == "deepseek":
        enabled = is_deepseek_enabled()

    credentials_present = False
    if name == "deepseek":
        credentials_present = bool(get_env_str("PA_DIEM_DEEPSEEK_API_KEY"))

    if is_mock:
        return {
            "provider": name,
            "is_mock": True,
            "enabled": True,
            "external_call_allowed": False,
            "credentials_present": False,
            "status": "ok",
        }

    if not enabled:
        return {
            "provider": name,
            "is_mock": False,
            "enabled": False,
            "external_call_allowed": False,
            "credentials_present": credentials_present,
            "status": "disabled_not_enabled",
        }

    if requires_credentials and not credentials_present:
        return {
            "provider": name,
            "is_mock": False,
            "enabled": True,
            "external_call_allowed": False,
            "credentials_present": False,
            "status": "disabled_missing_config",
        }

    if not is_external_ai_enabled():
        return {
            "provider": name,
            "is_mock": False,
            "enabled": True,
            "external_call_allowed": False,
            "credentials_present": credentials_present,
            "status": "disabled_external_ai_off",
        }

    return {
        "provider": name,
        "is_mock": False,
        "enabled": True,
        "external_call_allowed": True,
        "credentials_present": credentials_present,
        "status": "ok",
    }


def assert_provider_allowed(provider_name: str) -> None:
    """Assert that a provider is allowed to make calls."""
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
