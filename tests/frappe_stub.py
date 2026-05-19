"""Test helpers for importing Frappe-dependent modules without a bench."""

from pathlib import Path
import sys
import types
from unittest.mock import MagicMock


class FrappePermissionError(Exception):
    """Permission error used by the test Frappe stub."""


def ensure_app_path() -> None:
    """Add the Frappe app package root to sys.path for tests."""
    repo_root = Path(__file__).resolve().parents[1]
    app_root = repo_root / "padiem_ai"
    app_root_str = str(app_root)
    if app_root_str not in sys.path:
        sys.path.insert(0, app_root_str)


def _whitelist(*args, **kwargs):
    """Passthrough replacement for frappe.whitelist."""
    if args and callable(args[0]) and len(args) == 1 and not kwargs:
        return args[0]

    def decorator(fn):
        return fn

    return decorator


def install_frappe_stub():
    """Install a minimal frappe module stub and return it."""
    frappe = types.ModuleType("frappe")
    frappe.PermissionError = FrappePermissionError
    frappe.has_permission = MagicMock(return_value=True)
    frappe.whitelist = _whitelist
    frappe.log_error = MagicMock()
    frappe.get_traceback = MagicMock(return_value="")
    frappe.get_list = MagicMock(return_value=[])
    frappe.utils = types.SimpleNamespace(
        now=MagicMock(return_value="2026-05-19 00:00:00")
    )
    frappe.db = types.SimpleNamespace(
        count=MagicMock(return_value=0),
        get_value=MagicMock(return_value=0),
    )

    sys.modules["frappe"] = frappe
    return frappe
