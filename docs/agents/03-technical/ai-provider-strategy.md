# AI Provider Strategy

## Initial Provider

**DeepSeek** via OpenAI-compatible API (OpenGo-style provider).

### Why DeepSeek

- Cost-effective for Korean SME market
- Good Korean language support
- OpenAI-compatible API format (easy integration)
- Reasonable performance for ERP use cases

## Provider Abstraction (Required)

All AI calls must go through a provider abstraction layer.

```
Application Code
    │
    ▼
AI Provider Interface (abstract)
    │
    ├── DeepSeek (initial)
    ├── Mistral (future)
    ├── OpenAI (future)
    ├── Claude (future)
    ├── Gemini (future)
    ├── Local models (future)
    └── Ollama (future)
```

### Why Abstraction Is Required

1. **No vendor lock-in:** Switch providers without changing application code
2. **Cost optimization:** Route different tasks to different providers based on cost/performance
3. **Reliability:** Failover to backup provider if primary is down
4. **Customer choice:** Future customers may have provider preferences or data residency requirements

## Provider Interface

```python
class AIProvider:
    def chat(self, messages, **kwargs) -> str
    def stream(self, messages, **kwargs) -> Iterator[str]
    def embed(self, text) -> List[float]
```

Each provider implements this interface.

## Future Provider Roadmap

| Provider | Trigger |
|----------|---------|
| Mistral | If European data residency needed |
| OpenAI | If GPT-4 quality needed for complex queries |
| Claude | If long-context or analysis features needed |
| Gemini | If Google Cloud integration needed |
| Local models | If on-premise deployment required |
| Ollama | If customer wants self-hosted AI |

## Configuration

AI provider selection via environment variables:

```
AI_PROVIDER=deepseek
AI_API_KEY=sk-xxx
AI_MODEL=deepseek-chat
AI_BASE_URL=https://api.deepseek.com/v1
```
