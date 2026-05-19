"""DeepSeek AI provider implementation."""

from padiem_ai.ai.base import BaseAIProvider


class DeepSeekProvider(BaseAIProvider):
    """DeepSeek provider — client implementation behind config guard.

    All external calls are gated by config guard (ai/config.py).
    Without explicit enablement + credentials, no network call is made.
    Default behavior: returns disabled/missing_config status.
    """

    _TIMEOUT_SECONDS = 30

    def _get_config(self) -> dict:
        """Load DeepSeek config from environment via config helper."""
        from padiem_ai.ai.config import get_deepseek_config
        return get_deepseek_config()

    def _get_api_key(self) -> str:
        """Return API key from env. Never logs or exposes the key."""
        import os
        return os.environ.get("PA_DIEM_DEEPSEEK_API_KEY", "")

    def _build_chat_payload(self, messages: list, model: str, options: dict = None) -> dict:
        """Build OpenAI-compatible chat completion payload."""
        payload = {
            "model": model,
            "messages": messages,
        }
        if options:
            if "temperature" in options:
                payload["temperature"] = options["temperature"]
            if "max_tokens" in options:
                payload["max_tokens"] = options["max_tokens"]
        return payload

    def _call_deepseek_chat(self, payload: dict, api_key: str, base_url: str) -> dict:
        """Make a single DeepSeek chat completion call.

        Returns parsed JSON response dict.
        Raises on timeout/HTTP error — caller must catch.
        """
        import urllib.request
        import urllib.error
        import json

        url = f"{base_url.rstrip('/')}/chat/completions"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self._TIMEOUT_SECONDS) as resp:
                raw = resp.read()
                return json.loads(raw)
        except urllib.error.HTTPError as e:
            # Read and discard body — do not log headers or key
            _ = e.read()
            raise RuntimeError(
                f"DeepSeek HTTP error: status={e.code}"
            ) from e
        except urllib.error.URLError as e:
            raise RuntimeError(
                f"DeepSeek connection error: {e.reason}"
            ) from e
        except TimeoutError:
            raise RuntimeError(
                f"DeepSeek request timed out after {self._TIMEOUT_SECONDS}s"
            )

    def _ensure_allowed(self) -> None:
        """Verify config guard allows DeepSeek usage. Raises if not.

        Checks:
        1. Master switch: PA_DIEM_ENABLE_EXTERNAL_AI
        2. Provider flag: PA_DIEM_DEEPSEEK_ENABLED
        3. Credential: PA_DIEM_DEEPSEEK_API_KEY
        """
        from padiem_ai.ai.config import assert_provider_allowed, is_external_ai_enabled
        if not is_external_ai_enabled():
            raise RuntimeError(
                "External AI calls are disabled. "
                "Set PA_DIEM_ENABLE_EXTERNAL_AI=true to allow external AI."
            )
        assert_provider_allowed("deepseek")

    def _extract_text(self, response: dict) -> str:
        """Extract text content from DeepSeek chat completion response."""
        try:
            choices = response.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "")
            return ""
        except (KeyError, IndexError, TypeError):
            return ""

    def _serialize_context(self, context: dict) -> str:
        """Serialize context predictably for prompt construction."""
        if not context:
            return ""

        import json
        try:
            return json.dumps(context, ensure_ascii=False, sort_keys=True, default=str)
        except (TypeError, ValueError):
            return str(context)

    def _build_prompt_with_context(self, prompt: str, context: dict) -> str:
        """Build a prompt that explicitly includes context when supplied."""
        context_text = self._serialize_context(context)
        if not context_text:
            return prompt
        return f"{prompt}\n\nContext:\n{context_text}"

    def _build_summary_prompt(self, context: dict, prompt_template: str = "") -> str:
        """Build a summary prompt that always includes the supplied context."""
        base_prompt = prompt_template or "Summarize the supplied context."
        return self._build_prompt_with_context(base_prompt, context)

    def generate_text(self, prompt: str, context: dict, options: dict = None) -> str:
        """Generate text via DeepSeek. Blocked by config guard if not enabled."""
        self._ensure_allowed()
        cfg = self._get_config()
        api_key = self._get_api_key()
        if not api_key:
            raise RuntimeError("DeepSeek API key not configured")

        content = self._build_prompt_with_context(prompt, context)
        messages = [{"role": "user", "content": content}]
        payload = self._build_chat_payload(messages, cfg["model"], options)
        response = self._call_deepseek_chat(payload, api_key, cfg["base_url"])
        return self._extract_text(response)

    def generate_json(self, prompt: str, context: dict, schema: dict = None, options: dict = None) -> dict:
        """Generate JSON via DeepSeek. Blocked by config guard if not enabled."""
        self._ensure_allowed()
        cfg = self._get_config()
        api_key = self._get_api_key()
        if not api_key:
            raise RuntimeError("DeepSeek API key not configured")

        content = self._build_prompt_with_context(prompt, context)
        messages = [{"role": "user", "content": content}]
        payload = self._build_chat_payload(messages, cfg["model"], options)
        response = self._call_deepseek_chat(payload, api_key, cfg["base_url"])
        text = self._extract_text(response)
        import json
        try:
            return json.loads(text)
        except (json.JSONDecodeError, TypeError):
            return {"raw": text, "parse_error": True}

    def summarize(self, context: dict, prompt_template: str = "") -> str:
        """Summarize context via DeepSeek. Blocked by config guard if not enabled."""
        prompt = self._build_summary_prompt(context, prompt_template)
        return self.generate_text(prompt, {})

    def health_check(self) -> dict:
        """Check DeepSeek provider status without making an external API call."""
        from padiem_ai.ai.config import get_provider_config_status

        status_info = get_provider_config_status("deepseek")

        config_info = {
            "enabled": status_info.get("enabled", False),
            "external_call_allowed": status_info.get("external_call_allowed", False),
            "credentials_present": status_info.get("credentials_present", False),
        }

        if status_info["status"] != "ok":
            return {
                "status": status_info["status"],
                "provider": "deepseek",
                "external_call": False,
                "message": "DeepSeek provider is not ready for external calls.",
                "config": config_info,
            }

        return {
            "status": "ok",
            "provider": "deepseek",
            "external_call": False,
            "message": "DeepSeek provider is configured and allowed. Health check did not call external API.",
            "config": config_info,
        }

    def get_provider_name(self) -> str:
        return "deepseek"
