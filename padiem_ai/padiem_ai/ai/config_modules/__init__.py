"""Focused configuration modules for the AI provider layer."""

from padiem_ai.ai.config_modules.deepseek import (
    get_deepseek_config,
    get_validated_deepseek_base_url,
    validate_deepseek_base_url,
)
from padiem_ai.ai.config_modules.defaults import (
    PROVIDER_DEFAULTS,
    SELECTED_PROVIDER,
    get_selected_provider_name,
)
from padiem_ai.ai.config_modules.env import (
    get_env_bool,
    get_env_str,
)
from padiem_ai.ai.config_modules.guard import (
    assert_provider_allowed,
    get_provider_config_status,
    is_deepseek_enabled,
    is_external_ai_enabled,
)

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
