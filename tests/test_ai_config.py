"""Tests for AI provider configuration guard behavior."""

import os
import unittest
from unittest.mock import patch

from frappe_stub import ensure_app_path

ensure_app_path()

from padiem_ai.ai import config  # noqa: E402


class AiConfigTests(unittest.TestCase):
    def test_selected_provider_defaults_to_mock(self):
        self.assertEqual(config.get_selected_provider_name(), "mock")

    def test_mock_provider_status_is_ok_without_env(self):
        with patch.dict(os.environ, {}, clear=True):
            status = config.get_provider_config_status("mock")

        self.assertEqual(status["status"], "ok")
        self.assertTrue(status["is_mock"])
        self.assertFalse(status["external_call_allowed"])
        self.assertFalse(status["credentials_present"])

    def test_deepseek_status_disabled_by_default(self):
        with patch.dict(os.environ, {}, clear=True):
            status = config.get_provider_config_status("deepseek")

        self.assertEqual(status["status"], "disabled_not_enabled")
        self.assertFalse(status["enabled"])
        self.assertFalse(status["external_call_allowed"])
        self.assertFalse(status["credentials_present"])

    def test_deepseek_status_missing_config_when_enabled_without_key(self):
        with patch.dict(os.environ, {"PA_DIEM_DEEPSEEK_ENABLED": "true"}, clear=True):
            status = config.get_provider_config_status("deepseek")

        self.assertEqual(status["status"], "disabled_missing_config")
        self.assertTrue(status["enabled"])
        self.assertFalse(status["external_call_allowed"])
        self.assertFalse(status["credentials_present"])

    def test_deepseek_status_external_ai_off_when_key_present_but_master_off(self):
        env = {
            "PA_DIEM_DEEPSEEK_ENABLED": "true",
            "PA_DIEM_DEEPSEEK_API_KEY": "test-key",
        }
        with patch.dict(os.environ, env, clear=True):
            status = config.get_provider_config_status("deepseek")

        self.assertEqual(status["status"], "disabled_external_ai_off")
        self.assertTrue(status["enabled"])
        self.assertFalse(status["external_call_allowed"])
        self.assertTrue(status["credentials_present"])

    def test_deepseek_status_ok_when_full_enable_chain_present(self):
        env = {
            "PA_DIEM_ENABLE_EXTERNAL_AI": "true",
            "PA_DIEM_DEEPSEEK_ENABLED": "true",
            "PA_DIEM_DEEPSEEK_API_KEY": "test-key",
        }
        with patch.dict(os.environ, env, clear=True):
            status = config.get_provider_config_status("deepseek")

        self.assertEqual(status["status"], "ok")
        self.assertTrue(status["enabled"])
        self.assertTrue(status["external_call_allowed"])
        self.assertTrue(status["credentials_present"])

    def test_assert_provider_allowed_blocks_unknown_provider(self):
        with self.assertRaises(ValueError) as ctx:
            config.assert_provider_allowed("unknown")

        self.assertIn("Unknown provider", str(ctx.exception))

    def test_validate_deepseek_base_url_normalizes_default(self):
        self.assertEqual(
            config.validate_deepseek_base_url("https://api.deepseek.com/v1/"),
            "https://api.deepseek.com/v1",
        )

    def test_validate_deepseek_base_url_blocks_http_localhost_and_query(self):
        for url in (
            "http://api.deepseek.com/v1",
            "https://localhost/v1",
            "https://127.0.0.1/v1",
            "https://api.deepseek.com/v1?x=1",
        ):
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    config.validate_deepseek_base_url(url)

    def test_get_deepseek_config_uses_defaults_and_preserves_key_boolean(self):
        env = {
            "PA_DIEM_ENABLE_EXTERNAL_AI": "true",
            "PA_DIEM_DEEPSEEK_ENABLED": "true",
            "PA_DIEM_DEEPSEEK_API_KEY": "test-key",
        }
        with patch.dict(os.environ, env, clear=True):
            result = config.get_deepseek_config()

        self.assertEqual(result["base_url"], "https://api.deepseek.com/v1")
        self.assertEqual(result["model"], "deepseek-chat")
        self.assertTrue(result["api_key_present"])
        self.assertTrue(result["external_call_allowed"])
        self.assertNotIn("api_key", result)


if __name__ == "__main__":
    unittest.main()
