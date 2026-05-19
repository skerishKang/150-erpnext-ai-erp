"""Compatibility facade for AI provider configuration helpers.

Focused implementations live under `padiem_ai.ai.config_modules`.
This module keeps the existing import surface stable.
"""

from padiem_ai.ai.config_modules import (
    PROVIDER_DEFAULTS,
    SELECTED_PROVIDER,
    assert_provider_allowed,
    get_deepseek_config,
    get_env_bool,
    get_env_str,
    get_provider_config_status,
    get_selected_provider_name,
    get_validated_deepseek_base_url,
    is_deepseek_enabled,
    is_external_ai_enabled,
    validate_deepseek_base_url,
)
from padiem_ai.ai.config_modules.deepseek import (
    DEEPSEEK_DEFAULT_BASE_URL,
    DEEPSEEK_DEFAULT_MODEL,
    is_blocked_hostname,
    is_private_or_blocked_ip,
)

# Backwards-compatible private names for existing internal imports/tests.
_PROVIDER_DEFAULTS = PROVIDER_DEFAULTS
_SELECTED_PROVIDER = SELECTED_PROVIDER
_DEEPSEEK_DEFAULT_BASE_URL = DEEPSEEK_DEFAULT_BASE_URL
_DEEPSEEK_DEFAULT_MODEL = DEEPSEEK_DEFAULT_MODEL
_get_env_bool = get_env_bool
_get_env_str = get_env_str
_is_blocked_hostname = is_blocked_hostname
_is_private_or_blocked_ip = is_private_or_blocked_ip

__all__ = [
    "PROVIDER_DEFAULTS",
    "SELECTED_PROVIDER",
    "assert_provider_allowed",
    "get_deepseek_config",
    "get_env_bool",
    "get_env_str",
    "get_provider_config_status",
    "get_selected_provider_name",
    "get_validated_deepseek_base_url",
    "is_deepseek_enabled",
    "is_external_ai_enabled",
    "validate_deepseek_base_url",
]
