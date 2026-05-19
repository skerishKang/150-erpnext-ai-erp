"""Environment variable helpers for AI provider configuration."""


def get_env_bool(name: str) -> bool:
    """Read a boolean environment variable. Defaults to False."""
    import os

    val = os.environ.get(name, "").strip().lower()
    return val in ("1", "true", "yes", "on")


def get_env_str(name: str) -> str:
    """Read a string environment variable. Defaults to empty string."""
    import os

    return os.environ.get(name, "")
