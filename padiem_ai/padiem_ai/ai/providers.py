"""AI provider implementations.

Contains:
- MockProvider: active provider for dev/test (from PR #20)
- PlaceholderProvider: stub for future providers (no external calls)
"""

from padiem_ai.ai.base import BaseAIProvider


class MockProvider(BaseAIProvider):
    """Mock provider — no external calls, deterministic responses."""

    def generate_text(self, prompt: str, context: dict, options: dict = None) -> str:
        return "Mock response: AI integration pending."

    def generate_json(self, prompt: str, context: dict, schema: dict = None, options: dict = None) -> dict:
        return {"summary": "Mock summary", "alerts": []}

    def summarize(self, context: dict, prompt_template: str = "") -> str:
        return "Mock summary: AI integration pending."

    def health_check(self) -> dict:
        return {"status": "ok", "provider": "mock", "latency_ms": 0}

    def get_provider_name(self) -> str:
        return "mock"


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

    def generate_text(self, prompt: str, context: dict, options: dict = None) -> str:
        """Generate text via DeepSeek. Blocked by config guard if not enabled."""
        self._ensure_allowed()
        cfg = self._get_config()
        api_key = self._get_api_key()
        if not api_key:
            raise RuntimeError("DeepSeek API key not configured")

        messages = [{"role": "user", "content": prompt}]
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

        messages = [{"role": "user", "content": prompt}]
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
        prompt = prompt_template or str(context)
        return self.generate_text(prompt, context)

    def health_check(self) -> dict:
        """Check DeepSeek provider status. No external API call.

        Uses get_provider_config_status to reflect enable chain:
        - status="ok" when all chains pass
        - disabled_not_enabled / disabled_missing_config / disabled_external_ai_off otherwise
        Never exposes API key or makes external calls.
        """
        from padiem_ai.ai.config import get_provider_config_status
        status_info = get_provider_config_status("deepseek")
        return {
            "status": status_info["status"],
            "provider": "deepseek",
        }

    def get_provider_name(self) -> str:
        return "deepseek"


class PlaceholderProvider(BaseAIProvider):
    """Placeholder for future providers — never makes external calls.

    Used for: kilocode, opencodego, nvidia, deepseek, mistral, ollama
    These providers are registered but not yet implemented.
    """

    def __init__(self, name: str):
        self._name = name

    def generate_text(self, prompt: str, context: dict, options: dict = None) -> str:
        raise NotImplementedError(
            f"Provider '{self._name}' is not yet implemented. "
            f"Use 'mock' provider for development and testing."
        )

    def generate_json(self, prompt: str, context: dict, schema: dict = None, options: dict = None) -> dict:
        raise NotImplementedError(
            f"Provider '{self._name}' is not yet implemented. "
            f"Use 'mock' provider for development and testing."
        )

    def summarize(self, context: dict, prompt_template: str = "") -> str:
        raise NotImplementedError(
            f"Provider '{self._name}' is not yet implemented. "
            f"Use 'mock' provider for development and testing."
        )

    def health_check(self) -> dict:
        return {
            "status": "not_implemented",
            "provider": self._name,
            "message": f"Provider '{self._name}' is registered but not yet implemented.",
        }

    def get_provider_name(self) -> str:
        return self._name
