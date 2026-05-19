"""Tests for DeepSeek provider prompt construction without external calls."""

import unittest
from unittest.mock import patch

from frappe_stub import ensure_app_path

ensure_app_path()

from padiem_ai.ai.providers import DeepSeekProvider  # noqa: E402


class DeepSeekProviderPromptTests(unittest.TestCase):
    def setUp(self):
        self.provider = DeepSeekProvider()

    def test_serialize_context_is_deterministic_json(self):
        context = {"b": 2, "a": "한글"}

        result = self.provider._serialize_context(context)

        self.assertEqual(result, '{"a": "한글", "b": 2}')

    def test_serialize_context_handles_empty_context(self):
        self.assertEqual(self.provider._serialize_context({}), "")
        self.assertEqual(self.provider._serialize_context(None), "")

    def test_build_prompt_with_context_appends_context_section(self):
        result = self.provider._build_prompt_with_context(
            "Summarize this.",
            {"company": "Padiem", "count": 3},
        )

        self.assertTrue(result.startswith("Summarize this.\n\nContext:\n"))
        self.assertIn('"company": "Padiem"', result)
        self.assertIn('"count": 3', result)

    def test_build_prompt_with_context_keeps_prompt_when_context_empty(self):
        self.assertEqual(
            self.provider._build_prompt_with_context("Only prompt.", {}),
            "Only prompt.",
        )

    def test_build_summary_prompt_uses_default_prompt(self):
        result = self.provider._build_summary_prompt({"x": 1})

        self.assertTrue(result.startswith("Summarize the supplied context.\n\nContext:\n"))
        self.assertIn('"x": 1', result)

    def test_generate_text_includes_context_in_payload_without_external_call(self):
        with patch.object(self.provider, "_ensure_allowed") as ensure_allowed:
            with patch.object(self.provider, "_get_config", return_value={"model": "deepseek-test", "base_url": "https://api.deepseek.com/v1"}):
                with patch.object(self.provider, "_get_api_key", return_value="test-key"):
                    with patch.object(self.provider, "_call_deepseek_chat", return_value={"choices": [{"message": {"content": "ok"}}]}) as call_chat:
                        result = self.provider.generate_text("Prompt", {"x": 1})

        ensure_allowed.assert_called_once_with()
        self.assertEqual(result, "ok")
        payload = call_chat.call_args.args[0]
        self.assertEqual(payload["model"], "deepseek-test")
        content = payload["messages"][0]["content"]
        self.assertIn("Prompt\n\nContext:\n", content)
        self.assertIn('"x": 1', content)

    def test_generate_json_includes_context_and_parses_response(self):
        response = {"choices": [{"message": {"content": '{"ok": true}'}}]}
        with patch.object(self.provider, "_ensure_allowed"):
            with patch.object(self.provider, "_get_config", return_value={"model": "deepseek-test", "base_url": "https://api.deepseek.com/v1"}):
                with patch.object(self.provider, "_get_api_key", return_value="test-key"):
                    with patch.object(self.provider, "_call_deepseek_chat", return_value=response) as call_chat:
                        result = self.provider.generate_json("Return JSON", {"x": 1})

        self.assertEqual(result, {"ok": True})
        payload = call_chat.call_args.args[0]
        content = payload["messages"][0]["content"]
        self.assertIn("Return JSON\n\nContext:\n", content)
        self.assertIn('"x": 1', content)

    def test_summarize_does_not_duplicate_context(self):
        with patch.object(self.provider, "generate_text", return_value="summary") as generate_text:
            result = self.provider.summarize({"x": 1}, "Brief")

        self.assertEqual(result, "summary")
        prompt_arg, context_arg = generate_text.call_args.args
        self.assertIn("Brief\n\nContext:\n", prompt_arg)
        self.assertIn('"x": 1', prompt_arg)
        self.assertEqual(context_arg, {})


if __name__ == "__main__":
    unittest.main()
