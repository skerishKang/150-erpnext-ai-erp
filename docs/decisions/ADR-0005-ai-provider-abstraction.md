# ADR-0005: AI Provider Abstraction

**Status:** Accepted

**Date:** 2026-05-16

## Context

The product relies on Large Language Models (LLMs) for AI features: quotation drafting, sales summary generation, inventory alerts, CEO daily briefings.

Using a single AI provider creates vendor lock-in and single point of failure. Different providers have different strengths (cost, latency, Korean language quality, reasoning capability, context window size).

## Decision

Use an **AI provider abstraction layer** that allows switching between providers without changing application code.

| Concern | Decision |
|---------|----------|
| Initial provider | DeepSeek (via OpenRouter or similar API gateway) |
| Future candidates | Mistral, OpenAI (GPT-4o), Claude (Anthropic), Gemini (Google), local models (Ollama, vLLM) |
| Interface | Unified prompt → structured output contract |
| Provider selection | Configurable per task type or globally |

## Rationale

- The product must not depend permanently on **one model vendor** — pricing, quality, and availability change rapidly.
- Korean language capability varies significantly across providers; abstraction allows A/B testing.
- Abstraction enables **fallback chains** (primary provider → secondary → local) for reliability.
- Enterprise customers may require **on-premise models** (data sovereignty) — abstraction makes this possible without code changes.
- Provider API pricing fluctuates; abstraction enables cost optimization.

## Abstraction Layer Design

```
┌─────────────────────────────────┐
│        AI Module (Padiem)        │
│  ┌───────────────────────────┐   │
│  │   AI Provider Adapter     │   │
│  │   (Abstract Interface)    │   │
│  └──────┬──────────┬─────────┘   │
│         │          │             │
│  ┌──────▼──┐ ┌─────▼──────┐     │
│  │ DeepSeek│ │ OpenAI     │ ...  │
│  │ Adapter │ │ Adapter    │      │
│  └─────────┘ └────────────┘      │
└─────────────────────────────────┘
```

Each adapter:
- Translates a standard request into the provider's API format
- Handles authentication, retry, rate limiting
- Returns a standard response structure
- Logs token usage and cost

## Consequences

**Positive:**
- No vendor lock-in
- Task-specific model selection (cheap model for simple tasks, powerful model for complex reasoning)
- Graceful degradation if primary provider is unavailable
- Ability to test and adopt new models quickly

**Negative:**
- Additional development effort for the abstraction layer
- May not fully utilize unique provider features (e.g., Claude's extended thinking, Gemini's multimodal)
- Testing matrix grows with number of providers

## Alternatives Considered

| Alternative | Reason against |
|-------------|----------------|
| Single provider (DeepSeek only) | Vendor lock-in, no fallback |
| Direct API calls without abstraction | Harder to switch, harder to track costs, no fallback |
| Use LangChain / LlamaIndex | Heavy dependency, overkill for our use case |

## Related Documents

- [AI Provider Strategy](../agents/03-technical/ai-provider-strategy.md)
- [AI Module Architecture](../architecture/02-ai-module-architecture.md)
