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


def _is_private_or_blocked_ip(host: str) -> bool:
    """Check if host is a private or blocked IP address."""
    import ipaddress

    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False

    if ip.is_loopback:
        return True
    if ip.is_unspecified:
        return True
    if ip.is_link_local:
        return True

    if ip.is_private:
        return True

    if str(ip) == "169.254.169.254":
        return True

    return False


def _is_blocked_hostname(host: str) -> bool:
    """Check if hostname is a blocked string variant.

    Normalizes: strip, lower, rstrip(".")
    Blocked: localhost, localhost., LOCALHOST, LOCALHOST., *.localhost, *.local, 0, ::1
    """
    if not host:
        return True

    host_lower = host.strip().lower().rstrip(".")

    if host_lower in ("localhost", "0", "127.0.0.1"):
        return True

    if host_lower.endswith(".localhost") or host_lower.endswith(".local"):
        return True

    if host_lower == "::1":
        return True

    return False


def validate_deepseek_base_url(base_url: str) -> str:
    """Validate and normalize DeepSeek base URL.

    Allows:
    - https://api.deepseek.com/v1 (default)
    - https://api.deepseek.com/v1/ (normalized)
    - Custom host only with PA_DIEM_ALLOW_CUSTOM_DEEPSEEK_BASE_URL=true

    Blocks:
    - http:// (https only)
    - localhost, 127.0.0.1, ::1, and string variants
    - private IP ranges (10.x, 172.16-31.x, 192.168.x)
    - link-local (169.254.x)
    - metadata IP (169.254.169.254)
    - Empty host, userinfo, query, fragment
    - Non-443 ports
    - Non-/v1 paths

    Args:
        base_url: Base URL to validate

    Returns:
        str: Validated and normalized URL

    Raises:
        ValueError: If URL is blocked
    """
    from urllib.parse import urlparse

    if not base_url:
        raise ValueError("DeepSeek base URL cannot be empty")

    parsed = urlparse(base_url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Invalid scheme: {parsed.scheme}. Only https allowed.")

    if parsed.scheme == "http":
        raise ValueError("HTTP is not allowed. Use HTTPS only.")

    if parsed.username or parsed.password:
        raise ValueError("URL with userinfo (username/password) is not allowed.")

    if parsed.query:
        raise ValueError("URL with query string is not allowed.")

    if parsed.fragment:
        raise ValueError("URL with fragment is not allowed.")

    host = parsed.hostname
    if not host:
        raise ValueError("Host cannot be empty")

    if parsed.port is not None and parsed.port != 443:
        raise ValueError(f"Port {parsed.port} is not allowed. Only port 443 or no port.")

    # Conservative normalization: strip, lower, remove trailing dot
    host_norm = host.strip().lower().rstrip(".")

    if _is_private_or_blocked_ip(host_norm) or _is_blocked_hostname(host_norm):
        raise ValueError(f"Blocked host: {host}. Private/localhost/metadata IPs not allowed.")

    path = parsed.path.rstrip("/")
    allowed_paths = ("", "/v1")
    if path not in allowed_paths:
        raise ValueError(f"Path '{parsed.path}' is not allowed. Only /v1 or no path.")

    default_host = "api.deepseek.com"
    if host_norm != default_host:
        if not _get_env_bool("PA_DIEM_ALLOW_CUSTOM_DEEPSEEK_BASE_URL"):
            raise ValueError(
                f"Custom host '{host}' requires "
                f"PA_DIEM_ALLOW_CUSTOM_DEEPSEEK_BASE_URL=true"
            )

    normalized = f"https://{host_norm}/v1"
    return normalized


def get_validated_deepseek_base_url() -> str:
    """Get validated DeepSeek base URL from env or default.

    Returns:
        str: Validated base URL (always https)

    Raises:
        ValueError: If configured URL is invalid
    """
    raw_url = _get_env_str("PA_DIEM_DEEPSEEK_BASE_URL") or _DEEPSEEK_DEFAULT_BASE_URL
    return validate_deepseek_base_url(raw_url)


def get_deepseek_config() -> dict:
    """Get DeepSeek configuration from environment.

    Expected env vars (documented only, never committed with values):
        PA_DIEM_DEEPSEEK_API_KEY   — API key for DeepSeek
        PA_DIEM_DEEPSEEK_BASE_URL  — override base URL (optional)
        PA_DIEM_DEEPSEEK_MODEL     — model name (optional)

    Returns:
        dict with keys: api_key_present, base_url, model, external_call_allowed
        api_key_present is bool (True if env var is non-empty)
        base_url defaults to https://api.deepseek.com/v1 (validated)
        model defaults to deepseek-chat
        external_call_allowed requires both PA_DIEM_ENABLE_EXTERNAL_AI and PA_DIEM_DEEPSEEK_ENABLED

    Raises:
        ValueError: If PA_DIEM_DEEPSEEK_BASE_URL is invalid
    """
    api_key = _get_env_str("PA_DIEM_DEEPSEEK_API_KEY")
    base_url = get_validated_deepseek_base_url()
    model = _get_env_str("PA_DIEM_DEEPSEEK_MODEL") or _DEEPSEEK_DEFAULT_MODEL

    return {
        "api_key_present": bool(api_key),
        "base_url": base_url,
        "model": model,
        "external_call_allowed": is_external_ai_enabled() and is_deepseek_enabled() and bool(api_key),
    }
