"""DeepSeek-specific configuration helpers."""

from padiem_ai.ai.config_modules.env import get_env_bool, get_env_str
from padiem_ai.ai.config_modules.guard import is_deepseek_enabled, is_external_ai_enabled

DEEPSEEK_DEFAULT_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_DEFAULT_MODEL = "deepseek-chat"


def is_private_or_blocked_ip(host: str) -> bool:
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


def is_blocked_hostname(host: str) -> bool:
    """Check if hostname is a blocked string variant."""
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
    """Validate and normalize DeepSeek base URL."""
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

    host_norm = host.strip().lower().rstrip(".")

    if is_private_or_blocked_ip(host_norm) or is_blocked_hostname(host_norm):
        raise ValueError(f"Blocked host: {host}. Private/localhost/metadata IPs not allowed.")

    path = parsed.path.rstrip("/")
    allowed_paths = ("", "/v1")
    if path not in allowed_paths:
        raise ValueError(f"Path '{parsed.path}' is not allowed. Only /v1 or no path.")

    default_host = "api.deepseek.com"
    if host_norm != default_host:
        if not get_env_bool("PA_DIEM_ALLOW_CUSTOM_DEEPSEEK_BASE_URL"):
            raise ValueError(
                f"Custom host '{host}' requires "
                f"PA_DIEM_ALLOW_CUSTOM_DEEPSEEK_BASE_URL=true"
            )

    normalized = f"https://{host_norm}/v1"
    return normalized


def get_validated_deepseek_base_url() -> str:
    """Get validated DeepSeek base URL from env or default."""
    raw_url = get_env_str("PA_DIEM_DEEPSEEK_BASE_URL") or DEEPSEEK_DEFAULT_BASE_URL
    return validate_deepseek_base_url(raw_url)


def get_deepseek_config() -> dict:
    """Get DeepSeek configuration from environment."""
    api_key = get_env_str("PA_DIEM_DEEPSEEK_API_KEY")
    base_url = get_validated_deepseek_base_url()
    model = get_env_str("PA_DIEM_DEEPSEEK_MODEL") or DEEPSEEK_DEFAULT_MODEL

    return {
        "api_key_present": bool(api_key),
        "base_url": base_url,
        "model": model,
        "external_call_allowed": is_external_ai_enabled() and is_deepseek_enabled() and bool(api_key),
    }
