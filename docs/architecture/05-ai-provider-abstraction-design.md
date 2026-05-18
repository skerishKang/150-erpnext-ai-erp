# AI Provider 추상화 설계: Padiem AI ERP v1

| 항목 | 내용 |
|------|------|
| 문서 버전 | v1.0 |
| 작성일 | 2026-05-18 |
| 대상 | Padiem AI ERP 첫 개발 |
| 상태 | Draft |

---

## 1. 설계 목적

### 왜 추상화가 필요한가

AI ERP는 특정 AI 모델에 종속되면 안 됩니다. 오늘은 DeepSeek이 가성비가 좋을 수 있지만, 내년에는 다른 모델이 더 나을 수 있습니다. 모델을 바꿀 때마다 코드를 다시 작성하는 구조는 유지보수 비용이 높고, 장애 시 대체할 수 없습니다.

이 문서는 Padiem AI ERP 안에서 AI provider를 어떻게 설계해야 하는지를 정의합니다.

### 핵심 목표

| 목표 | 설명 |
|------|------|
| **Provider-agnostic** | 특정 모델이나 provider에 종속되지 않는 구조 |
| **교체 가능** | provider 변경 시 설정만으로 대응 가능 |
| **안전한 기본값** | 개발 초기에는 mock/local-safe mode로 시작 |
| **ERP 통합** | ERPNext Custom App인 `padiem_ai` 안에서 동작 |

### 초기 후보

- **DeepSeek via OpenGo-style/OpenAI-compatible provider**
- OpenAI-compatible API 형태를 활용하면 provider 교체가 쉬움

### 추후 확장 대상

- Mistral
- OpenAI
- Claude
- Gemini
- Local models
- Ollama-compatible models

---

## 2. 핵심 원칙

### Provider 설계 원칙

| 원칙 | 설명 |
|------|------|
| **Provider-agnostic** | 코드에서 특정 provider를 직접 참조하지 않음 |
| **Prompt와 Provider 분리** | prompt template은 별도 파일, provider는 호출만 담당 |
| **ERP 데이터와 AI 호출 분리** | data retrieval layer와 AI provider layer를 명확히 분리 |
| **Credential 미기록** | 실제 credential은 코드와 문서에 기록하지 않음 |
| **외부 전송 제한** | 외부 provider 사용은 관리자 설정과 명시적 동의 후 활성화 |
| **기본 mock mode** | 기본 개발 모드는 mock/local-safe mode |
| **최소 데이터 전달** | 외부 전송 시 최소 필요 데이터만 전달 |
| **자동 저장 금지** | AI 결과는 초안/요약/조회 결과이며 자동 저장하지 않음 |

### 안전한 개발 흐름

```
Phase 1: MockProvider로 개발 (외부 전송 없음)
Phase 2: DeepSeek provider 연결 (관리자 설정 후)
Phase 3: 다른 provider 추가 (필요 시)
```

---

## 3. Provider 계층 구조

### 클래스 구조

```
BaseAIProvider (abstract)
├── DeepSeekProvider
├── OpenAICompatibleProvider
├── MistralProvider
├── ClaudeProvider
├── GeminiProvider
├── OllamaProvider
└── MockProvider
```

### 각 Provider 역할

| Provider | 역할 | 시점 |
|----------|------|------|
| **BaseAIProvider** | 추상 인터페이스 정의 | Phase 1 |
| **MockProvider** | 개발/테스트용, 외부 호출 없음 | Phase 1 |
| **DeepSeekProvider** | DeepSeek API 호출 | Phase 2 |
| **OpenAICompatibleProvider** | OpenAI-compatible API 형태 | Phase 2 |
| **MistralProvider** | Mistral API 호출 | Phase 3+ |
| **ClaudeProvider** | Claude API 호출 | Phase 3+ |
| **GeminiProvider** | Gemini API 호출 | Phase 3+ |
| **OllamaProvider** | 로컬 Ollama 호출 | Phase 3+ |

### 관계 다이어그램

```
┌─────────────────────────────────────────────────┐
│              BaseAIProvider (abstract)           │
│                                                 │
│  generate_text(prompt, context, options)         │
│  generate_json(prompt, context, schema, options) │
│  summarize(context, prompt_template)             │
│  health_check()                                  │
│  estimate_cost()                                 │
│  get_provider_name()                             │
└───────────────┬─────────────────────────────────┘
                │
    ┌───────────┼───────────┬───────────────┐
    │           │           │               │
    ▼           ▼           ▼               ▼
┌────────┐ ┌────────┐ ┌────────┐    ┌────────────┐
│Mock    │ │DeepSeek│ │OpenAI  │    │Ollama      │
│Provider│ │Provider│ │Compat. │    │Provider    │
└────────┘ └────────┘ └────────┘    └────────────┘
```

---

## 4. 표준 인터페이스 정의

> **Note**: 아래 코드는 전략 문서용 pseudo-code입니다. 실제 구현 PR에서 Frappe/Python 방식으로 검증합니다.

### BaseAIProvider 인터페이스 (concept only)

```python
class BaseAIProvider:
    """AI provider 추상 인터페이스 (concept only)"""

    def generate_text(self, prompt: str, context: dict, options: dict) -> str:
        """텍스트 생성 요청"""
        raise NotImplementedError

    def generate_json(self, prompt: str, context: dict, schema: dict, options: dict) -> dict:
        """JSON 구조화 응답 요청"""
        raise NotImplementedError

    def summarize(self, context: dict, prompt_template: str) -> str:
        """데이터 요약 요청"""
        raise NotImplementedError

    def health_check(self) -> dict:
        """provider 상태 확인"""
        raise NotImplementedError

    def estimate_cost(self, prompt: str, context: dict) -> dict:
        """예상 비용 계산"""
        raise NotImplementedError

    def get_provider_name(self) -> str:
        """provider 이름 반환"""
        raise NotImplementedError
```

### 각 메서드 설명

| 메서드 | 입력 | 출력 | 설명 |
|--------|------|------|------|
| `generate_text` | prompt, context, options | string | 자유 형식 텍스트 생성 |
| `generate_json` | prompt, context, schema, options | dict | JSON 구조화 응답 생성 |
| `summarize` | context, prompt_template | string | 데이터 요약 |
| `health_check` | 없음 | dict (status, latency) | provider 연결 상태 확인 |
| `estimate_cost` | prompt, context | dict (tokens, cost) | 예상 비용 계산 |
| `get_provider_name` | 없음 | string | provider 이름 |

---

## 5. 공통 요청 구조

### AI 요청 항목

| 필드 | 타입 | 설명 |
|------|------|------|
| `feature_name` | string | 요청하는 기능 (briefing, query, quotation 등) |
| `user_id` | string | 요청한 사용자 ID |
| `provider_name` | string | 사용할 provider 이름 |
| `prompt_template_id` | string | 사용할 prompt template ID |
| `sanitized_context` | dict | 민감정보가 제거된 ERP 데이터 |
| `output_format` | string | 원하는 출력 형식 (text, json) |
| `max_tokens` | int | 최대 토큰 수 |
| `temperature` | float | 창의성 수준 (0.0~1.0) |
| `request_timestamp` | string | 요청 시간 |

### sanitized_context 개념

**핵심**: AI에게 보낼 때는 ERP 원문 데이터를 그대로 보내지 않고, 민감정보를 제거하거나 요약한 형태로 전달합니다.

**예시**:

```python
# ERP 원문 데이터 (내부)
raw_context = {
    "customer_name": "서울건설",
    "customer_id": "CUST-001",
    "outstanding_amount": 45000000,
    "due_date": "2026-04-20",
    "contact_email": "ceo@seoulbuild.kr",
    "phone": "02-1234-5678",
    "address": "서울시 강남구..."
}

# sanitized_context (AI에 전달)
sanitized_context = {
    "customer_name": "서울건설",
    "outstanding_amount": 45000000,
    "due_date": "2026-04-20",
    "days_overdue": 28
    # 이메일, 전화번호, 주소는 제외
}
```

**제거 대상**:
- 이메일 주소
- 전화번호
- 상세 주소
- 사업자등록번호
- 계좌번호
- 내부 ID (필요 시)

**유지 대상**:
- 거래처명 (표시용)
- 금액
- 날짜
- 상태
- 수량

---

## 6. 공통 응답 구조

### AI 응답 항목

| 필드 | 타입 | 설명 |
|------|------|------|
| `success` | boolean | 성공 여부 |
| `provider` | string | 사용된 provider 이름 |
| `model` | string | 사용된 모델 이름 |
| `output_text` | string | 텍스트 출력 |
| `output_json` | dict | JSON 출력 (지정 시) |
| `source_data_summary` | dict | 사용된 ERP 데이터 요약 |
| `warnings` | list | 경고 메시지 목록 |
| `latency_ms` | int | 응답 시간 (밀리초) |
| `token_usage` | dict | 토큰 사용량 (prompt, completion) |
| `created_at` | string | 응답 생성 시간 |

### 응답 예시

```json
{
    "success": true,
    "provider": "deepseek",
    "model": "deepseek-chat",
    "output_text": "오늘 확인할 사항: 미수금 연체 1건...",
    "output_json": null,
    "source_data_summary": {
        "invoices_checked": 3,
        "orders_checked": 5,
        "items_checked": 10
    },
    "warnings": [],
    "latency_ms": 1200,
    "token_usage": {
        "prompt_tokens": 500,
        "completion_tokens": 200
    },
    "created_at": "2026-05-18T09:00:00"
}
```

---

## 7. 기능별 Provider 사용 방식

### 기능별 상세

| 기능 | ERPNext 데이터 | AI가 하는 일 | 권장 출력 | 외부 provider | mock mode | 승인 필요 |
|------|---------------|-------------|-----------|--------------|-----------|----------|
| **CEO Daily Briefing** | Sales Invoice, Sales Order, Payment Entry, Stock Entry | 오늘 현황 요약 | text | 가능 | 가능 | 불필요 |
| **자연어 ERP Query** | 모든 DocType | 한국어 질문을 ERP 쿼리로 변환 | json | 가능 | 가능 | 불필요 |
| **Quotation Draft** | Customer, Item, Price List | 견적서 초안 생성 | json | 가능 | 가능 | **필요** |
| **Receivables Summary** | Sales Invoice, Customer | 미수금 현황 요약 | text | 가능 | 가능 | 불필요 |
| **Delivery & Stock** | Sales Order, Delivery Note, Stock Entry, Item, Bin | 배송/재고 상태 요약 | text | 가능 | 가능 | 불필요 |
| **Accountant Package** | Sales Invoice, Purchase Invoice, Payment Entry, Stock Entry | 회계사 자료 요약 | text | 가능 | 가능 | 불필요 |

### 기능별 Provider 선택 전략

| 기능 | 1차 후보 | 2차 후보 | 이유 |
|------|---------|---------|------|
| CEO Daily Briefing | DeepSeek | Mock | 요약 품질, 비용 |
| 자연어 ERP Query | DeepSeek | Mock | 한국어 이해력 |
| Quotation Draft | DeepSeek | Mock | 구조화 출력 |
| Receivables Summary | DeepSeek | Mock | 간단한 요약 |
| Delivery & Stock | DeepSeek | Mock | 간단한 요약 |
| Accountant Package | DeepSeek | Mock | 간단한 요약 |

---

## 8. Prompt Template 전략

### 기본 원칙

| 원칙 | 설명 |
|------|------|
| **하드코딩 금지** | prompt를 코드에 하드코딩하지 않음 |
| **파일 분리** | `prompts/` 폴더에 feature별 template로 관리 |
| **한국어 우선** | 한국어 business tone 우선 |
| **버전 관리** | prompt template에 버전 포함 |
| **구조 분리** | system instruction / user instruction / context 분리 |
| **Credential 금지** | prompt에 실제 key나 credential 포함 금지 |

### Prompt Template 파일 구조

```
padiem_ai/
└── prompts/
    ├── briefing_v1.json
    ├── query_v1.json
    ├── quotation_draft_v1.json
    ├── receivables_v1.json
    ├── delivery_stock_v1.json
    └── accountant_package_v1.json
```

### Template 형식 (concept only)

```json
{
    "name": "ceo_daily_briefing",
    "version": "1.0",
    "language": "ko",
    "system_instruction": "당신은 중소기업 대표의 업무 보조 AI입니다. ERP 데이터를 읽고, 오늘 확인해야 할 사항을 간결하게 요약합니다.",
    "user_instruction": "아래 ERP 데이터를 바탕으로 오늘의 브리핑을 작성하세요.",
    "context_placeholder": "{{erp_data}}",
    "output_format": "text",
    "max_tokens": 1000,
    "temperature": 0.3,
    "constraints": [
        "3~5줄로 요약",
        "숫자는 원화(₩)로 표시",
        "긴급 사항은 [높음]으로 표시",
        "추천 행동을 1~2개 포함"
    ]
}
```

### Template 분리 구조

| 구분 | 설명 | 예시 |
|------|------|------|
| **System instruction** | AI의 역할과 규칙 | "당신은 중소기업 대표의 업무 보조 AI입니다" |
| **User instruction** | 구체적인 작업 지시 | "아래 ERP 데이터를 바탕으로 오늘의 브리핑을 작성하세요" |
| **Context** | ERP 데이터 (sanitized) | `{{erp_data}}` placeholder로 삽입 |
| **Constraints** | 출력 제약 조건 | "3~5줄로 요약", "숫자는 원화로 표시" |

---

## 9. Provider 설정 전략

### 설정 항목

| 항목 | 타입 | 설명 |
|------|------|------|
| `provider_name` | string | provider 이름 (deepseek, openai 등) |
| `model_name` | string | 모델 이름 (deepseek-chat, gpt-4 등) |
| `base_url` | string | API base URL |
| `credential_reference` | string | credential 위치 참조 (실제 key 아님) |
| `enabled` | boolean | 활성화 여부 |
| `allowed_features` | list | 이 provider를 사용할 수 있는 기능 목록 |
| `max_tokens` | int | 최대 토큰 수 |
| `timeout_seconds` | int | 타임아웃 (초) |
| `external_transfer_allowed` | boolean | 외부 전송 허용 여부 |

### credential_reference 설명

`credential_reference`는 실제 key가 아니라 **설정 위치 참조**만 의미합니다.

```python
# 올바른 예: 설정 위치 참조
{
    "provider_name": "deepseek",
    "credential_reference": "site_config.padiem_ai_api_key"
    # credential은 site_config 또는 환경변수 등 Git 밖의 안전한 위치에 저장
    # 저장 방식은 배포 환경별로 결정. 문서와 Git에는 절대 기록하지 않음
}

# 잘못된 예: 실제 key를 직접 기록
{
    "provider_name": "deepseek",
    "api_key": "<never commit real credential>"
}
```

### 설정 저장 위치

- **Frappe Site Config**: `sites/frontend/site_config.json` (Git 제외)
- **환경변수**: `PADIEM_AI_API_KEY` 등 (배포 환경별 검토)
- **데이터베이스**: v2에서 관리자 UI로 관리 검토

### 설정 예시 (concept only)

```python
# site_config.json (concept only)
{
    "padiem_ai_default_provider": "deepseek",
    "padiem_ai_providers": {
        "deepseek": {
            "model_name": "deepseek-chat",
            "base_url": "<configured outside git>",
            "credential_reference": "site_config.padiem_ai_api_key",
            "enabled": true,
            "allowed_features": ["briefing", "query", "quotation", "receivables"],
            "max_tokens": 2000,
            "timeout_seconds": 30,
            "external_transfer_allowed": true
        },
        "mock": {
            "model_name": "mock-v1",
            "base_url": null,
            "credential_reference": null,
            "enabled": true,
            "allowed_features": ["all"],
            "max_tokens": 1000,
            "timeout_seconds": 5,
            "external_transfer_allowed": false
        }
    }
}
```

---

## 10. DeepSeek/OpenGo-style 초기 후보

### 왜 DeepSeek인가

| 이유 | 설명 |
|------|------|
| **OpenAI-compatible API** | OpenAI API 형태를 지원하면 provider 교체가 쉬움 |
| **한국어 성능** | 한국어 처리 능력이 파일럿에서 검증 가능 |
| **비용 효율** | 다른 대형 모델 대비 비용이 낮을 수 있음 |
| **접근성** | API를 통한 호출이 가능 |

### OpenAI-compatible 장점

OpenAI-compatible API 형태를 지원하는 provider는 동일한 코드 구조로 호출할 수 있습니다.

```
DeepSeek:  POST https://api.deepseek.com/v1/chat/completions
OpenAI:    POST https://api.openai.com/v1/chat/completions
기타:      POST https://custom-provider.com/v1/chat/completions
```

endpoint URL과 credential만 다르게 설정하면 동일한 `OpenAICompatibleProvider`로 호출 가능합니다.

### 주의사항

| 주의 | 설명 |
|------|------|
| **provider 고정 금지** | DeepSeek에만 종속되지 않도록 구조 설계 |
| **비용 검증 필요** | 파일럿에서 실제 비용 확인 |
| **속도 검증 필요** | 응답 속도가 사용자 경험에 미치는 영향 확인 |
| **한국어 품질 검증** | 한국어 business terminology 처리 능력 확인 |
| **안정성 검증** | API 안정성, rate limit, 에러율 확인 |

---

## 11. Mock Provider 전략

### MockProvider가 필요한 이유

| 이유 | 설명 |
|------|------|
| **외부 전송 없음** | Docker/ERPNext/외부 API 없이도 테스트 가능 |
| **비용 없음** | API 비용 없이 개발/테스트 가능 |
| **빠른 반복** | 응답이 즉시 돌아와서 개발 속도 빠름 |
| **안전한 데모** | 고객 데이터 외부 전송 없이 데모 가능 |
| **장애 대체** | 외부 provider 장애 시 fallback으로 사용 |

### MockProvider 동작 (concept only)

```python
class MockProvider(BaseAIProvider):
    """개발/테스트용 Mock provider (concept only)"""

    def generate_text(self, prompt, context, options):
        # 미리 정의된 응답 반환
        return "이것은 Mock 응답입니다. 실제 AI 호출이 아닙니다."

    def generate_json(self, prompt, context, schema, options):
        # 스키마에 맞는 더미 JSON 반환
        return {"summary": "Mock 요약", "alerts": ["Mock 알림"]}

    def health_check(self):
        return {"status": "ok", "latency_ms": 0}
```

### MockProvider 사용 시점

| 시점 | MockProvider 사용 |
|------|-------------------|
| **Phase 1 개발** | 모든 기능에서 MockProvider 사용 |
| **Phase 2 테스트** | DeepSeek 연결 후에도 MockProvider로 테스트 |
| **데모** | 고객 데모 시 MockProvider로 안전하게 시연 |
| **장애 시나리오 테스트** | provider 장애 상황을 시뮬레이션하여 fallback 로직 검증 |

### 첫 구현 권장

**첫 구현 PR에서 MockProvider부터 만드는 것을 권장합니다.**

MockProvider가 있어야:
- UI와 API 흐름을 테스트할 수 있음
- 외부 provider 없이도 개발을 진행할 수 있음
- 고객 데이터 외부 전송 없이 데모할 수 있음

---

## 12. 보안/개인정보 원칙

### 기본 원칙

| 원칙 | 설명 |
|------|------|
| **API key 커밋 금지** | API key, secret, password를 코드에 포함하지 않음 |
| **외부 전송 최소화** | 고객 데이터 외부 전송을 최소화 |
| **민감정보 마스킹** | 이메일, 전화번호, 주소 등 민감정보 제거 검토 |
| **로그 제한** | AI 요청/응답 전체 로그 저장 금지 |
| **v1 로그 최소화** | feature_name, user, success, latency 정도만 기록 |
| **관리자만 설정** | 관리자만 provider 설정 가능 |
| **Role-based access** | ERPNext Role Permission Manager 준수 |
| **데이터 제한** | 사용자가 볼 수 없는 ERP 데이터는 AI도 볼 수 없음 |

### Natural-language ERP Query 보안 원칙

자연어 ERP Query 기능은 특히 주의가 필요합니다. AI가 ERP 데이터에 직접 접근하는 구조이므로 다음 원칙을 반드시 준수합니다.

| 원칙 | 설명 |
|------|------|
| **임의 SQL 생성/실행 금지** | AI가 임의 SQL을 생성하거나 실행하지 않음 |
| **임의 DocType 접근 금지** | AI가 임의 DocType에 접근하지 않음 |
| **Allowlisted 매핑만 사용** | DocType, field, filter는 사전에 정의된 allowlisted 매핑만 사용 |
| **권한 검사 후 read-only** | ERPNext 권한 검사 후 read-only query만 수행 |
| **Write query 금지** | UPDATE, DELETE, INSERT 등 write query는 금지 |

### v1 로그 항목

| 항목 | 저장 | 설명 |
|------|------|------|
| feature_name | 예 | 기능 이름 |
| user_id | 예 | 요청한 사용자 |
| success | 예 | 성공/실패 여부 |
| latency_ms | 예 | 응답 시간 |
| provider_name | 예 | 사용된 provider |
| prompt | 아니오 | 개인정보 포함 가능 |
| response | 아니오 | 개인정보 포함 가능 |
| raw_context | 아니오 | ERP 원문 데이터 |

### 관리자 설정 권한

```python
# provider 설정은 관리자만 가능
if not frappe.has_role("System Manager"):
    frappe.throw("AI provider 설정은 관리자만 변경할 수 있습니다.")
```

---

## 13. 장애 대응 전략

### 장애 유형별 대응

| 장애 유형 | 대응 |
|----------|------|
| **provider timeout** | 지정 시간 내 응답 없으면 degraded mode (deterministic/cached summary) |
| **provider rate limit** | rate limit 초과 시 대기 후 재시도 또는 fallback |
| **provider error** | API 에러 시 사용자에게 기술 오류 노출하지 않음 |
| **invalid JSON response** | JSON 파싱 실패 시 텍스트 응답으로 fallback |
| **hallucination risk** | 출력 검증 로직, source_data_summary 포함 |

### Fallback 전략

```
1차: 외부 provider (DeepSeek 등)
  ↓ 실패 시
2차: Cached summary (이전 AI 응답 캐시)
  ↓ 실패 시
3차: Deterministic summary (ERP 데이터 직접 집계, 규칙 기반)
```

**주의**: MockProvider는 개발/테스트/안전 데모용입니다. 운영 환경에서는 provider 장애 시 deterministic summary, cached summary, degraded mode로 fallback합니다. 운영에서 mock 응답을 실제 업무 응답처럼 보여주지 않습니다.

### 사용자 경험 보호

```python
# 기술 오류를 사용자에게 그대로 노출하지 않음
try:
    response = provider.generate_text(prompt, context, options)
except ProviderTimeoutError:
    return {
        "success": False,
        "degraded": True,
        "fallback_used": True,
        "user_message": "AI 서비스를 일시적으로 사용할 수 없어 ERP 기본 요약을 표시합니다.",
        "fallback_data": get_deterministic_summary(context)
    }
except ProviderError as e:
    return {
        "success": False,
        "degraded": True,
        "fallback_used": True,
        "user_message": "AI 서비스를 일시적으로 사용할 수 없어 ERP 기본 요약을 표시합니다.",
        "fallback_data": get_deterministic_summary(context)
    }
```

---

## 14. 비용 통제 전략

### 비용 절감 방법

| 방법 | 설명 |
|------|------|
| **Feature별 max token 제한** | 각 기능에 최대 토큰 수 설정 |
| **Daily briefing cache** | 같은 날 반복 요청 시 캐시된 응답 사용 |
| **Repeated query cache** | 동일한 반복 질문 캐시 후보 |
| **사전 집계** | large data summarization은 먼저 ERP query로 집계 후 최소 context만 전달 |
| **사용량 제한** | 사용자별/회사별 사용량 제한 후보 |

### 기능별 토큰 제한 (권장)

| 기능 | max_tokens (completion) | 이유 |
|------|------------------------|------|
| CEO Daily Briefing | 500 | 3~5줄 요약 |
| 자연어 ERP Query | 1000 | 표 형태 응답 |
| Quotation Draft | 1500 | 견적서 구조 |
| Receivables Summary | 500 | 간단한 요약 |
| Delivery & Stock | 500 | 간단한 요약 |
| Accountant Package | 800 | 체크리스트 형태 |

### 캐시 전략

```python
# Daily briefing 캐시 (concept only)
def get_ceo_briefing():
    cache_key = f"ceo_briefing:{frappe.utils.today()}:{frappe.session.user}"

    # 캐시 확인
    cached = frappe.cache().get(cache_key)
    if cached:
        return cached

    # AI 호출
    response = provider.generate_text(...)

    # 캐시 저장 (1시간)
    frappe.cache().set(cache_key, response, timeout=3600)

    return response
```

---

## 15. 구현 단계 제안

### Phase 1: Provider interface 문서화 및 MockProvider 설계

**목표**: BaseAIProvider 인터페이스와 MockProvider 구현

**작업**:
- BaseAIProvider abstract class 정의
- MockProvider 구현
- Provider factory (설정 기반 provider 선택)
- 단위 테스트

**결과물**: MockProvider로 AI 기능 테스트 가능

---

### Phase 2: DeepSeek/OpenGo-style provider adapter 설계

**목표**: DeepSeek provider adapter 구현

**작업**:
- OpenAICompatibleProvider 구현
- DeepSeek endpoint 설정
- Credential 관리 (site_config)
- 통합 테스트

**결과물**: DeepSeek API 호출 가능

---

### Phase 3: Prompt template 구조 설계

**목표**: Prompt template 파일 구조와 로딩 로직 구현

**작업**:
- `prompts/` 폴더 구조 정의
- Template 로딩 로직 구현
- Template 버전 관리
- Context placeholder 치환 로직

**결과물**: Feature별 prompt template 관리 가능

---

### Phase 4: CEO Briefing에 provider 연결

**목표**: CEO Daily Briefing 기능에 AI provider 연결

**작업**:
- BriefingContextBuilder 구현
- Briefing API에 provider 연결
- MockProvider와 DeepSeekProvider 모두 테스트
- UI에 AI 요약 표시

**결과물**: CEO Daily Briefing이 AI로 동작

---

### Phase 5: Natural-language Query에 provider 연결

**목표**: 자연어 ERP Query 기능에 AI provider 연결

**작업**:
- QueryParser 구현 (한국어 → ERP 쿼리)
- Query API에 provider 연결
- JSON 응답 파싱
- UI에 쿼리 결과 표시

**결과물**: 한국어로 ERP 데이터 조회 가능

---

### Phase 6: Logging/cost/permission hardening

**목표**: 보안, 비용, 감사 강화

**작업**:
- AI 사용 로그 기록
- 비용 추적
- Rate limiting
- 권한 확인 강화

**결과물**: 프로덕션 배포 가능 수준

---

## 16. 하지 않을 것

### 명확한 제외 항목

| 하지 않을 것 | 이유 |
|-------------|------|
| **실제 API key 문서화** | 보안 위험 |
| **특정 provider 종속** | 교체 불가 구조 |
| **AI 자동 수정 구조** | AI가 ERP 데이터를 자동으로 수정하지 않음 |
| **고객 원문 전체 전달** | 민감정보 보호 |
| **외부 provider 무단 활성화** | 관리자 동의 필요 |
| **회계/세무/급여 자동 판단** | v1 범위 외 |

---

## 17. 첫 개발 PR 후보

### 구현 순서

| 순위 | PR 제목 | 설명 |
|------|---------|------|
| 1 | `feat: add AI provider interface and mock provider` | BaseAIProvider + MockProvider |
| 2 | `feat: add DeepSeek OpenGo-style provider adapter` | OpenAICompatibleProvider + DeepSeek 설정 |
| 3 | `feat: add prompt template registry` | Template 파일 구조 + 로딩 로직 |
| 4 | `feat: connect provider to CEO briefing API` | Briefing에 provider 연결 |
| 5 | `feat: add AI provider settings validation` | 설정 검증 로직 |
| 6 | `feat: add minimal AI usage logging` | 최소한의 사용 로그 |

### PR 작성 원칙

- 각 PR은 1개 기능만 포함
- MockProvider로 먼저 테스트
- 외부 provider 테스트는 별도 PR
- 테스트 코드 포함
- ERPNext core 수정 없음

---

**문서 버전**: v1.0
**작성일**: 2026-05-18
**상태**: Draft
