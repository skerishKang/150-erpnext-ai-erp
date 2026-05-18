# 20 - CEO Briefing Mock Provider Routing Log

| 항목 | 내용 |
|------|------|
| 문서 버전 | v1.0 |
| 작성일 | 2026-05-18 |
| Issue | #32 |
| 브랜치 | `feat/issue-32-ceo-briefing-mock-provider-routing` |
| 상태 | 구현 완료, Docker 테스트 통과 |

---

## 1. 작업 목적

기존 CEO briefing 흐름을 AI Provider Registry를 경유하도록 연결합니다. mock provider만 사용하며, 외부 AI 호출은 하지 않습니다.

---

## 2. 수정된 파일

| 파일 | 유형 | 설명 |
|------|------|------|
| `padiem_ai/padiem_ai/api/briefing.py` | 수정 | Provider registry 경유 로직 추가 |
| `padiem_ai/padiem_ai/www/ceo_briefing.py` | 수정 | Provider info 표시 로직 추가 |
| `padiem_ai/padiem_ai/www/ceo_briefing.html` | 수정 | Provider info 표시 UI 추가 |
| `docs/implementation/20-ceo-briefing-mock-provider-routing-log.md` | 신규 | 구현 로그 |

---

## 3. API 응답 구조

### get_ceo_briefing

```json
{
    "success": true,
    "data": { "counts": {...}, "sales": {...}, ... },
    "briefing": {
        "title": "CEO Daily Briefing",
        "summary": "고객 6개사 / 공급업체 6개사 / ...",
        "sections": [
            {"title": "매출 현황", "content": "..."},
            {"title": "구매 현황", "content": "..."},
            {"title": "미수금 및 입금 현황", "content": "..."},
            {"title": "재고 및 운영 현황", "content": "..."},
            {"title": "주의 사항", "content": "..."}
        ],
        "raw_context": {...}
    },
    "provider": {
        "name": "mock",
        "status": "ok",
        "external_call": false
    },
    "provider_response": {
        "summary": "Mock summary: AI integration pending.",
        "model": "mock",
        "source": "provider_registry"
    },
    "ai_summary": "Mock provider response — no external AI call.",
    "timestamp": "2026-05-18 21:48:31"
}
```

---

## 4. Provider Routing 흐름

```
get_ceo_briefing()
  ├── Step 1: Read ERP data (get_ceo_briefing_context)
  ├── Step 2: Generate deterministic briefing (generate_mock_ceo_briefing)
  └── Step 3: Route through provider registry
        ├── _get_provider_info("mock") → {name, status, external_call}
        └── _get_mock_provider_response(briefing, "mock") → {summary, model, source}
```

---

## 5. Docker 테스트 결과

### API Endpoint

| 항목 | 상태 |
|------|------|
| success is True | PASS |
| data exists | PASS |
| briefing.title is "CEO Daily Briefing" | PASS |
| briefing.sections count is 5 | PASS |
| provider.name is "mock" | PASS |
| provider.status is "ok" | PASS |
| provider.external_call is False | PASS |
| provider_response.model is "mock" | PASS |
| provider_response.source is "provider_registry" | PASS |
| ai_summary contains "Mock provider" | PASS |

### Web Route (/ceo_briefing)

| 항목 | 상태 |
|------|------|
| Provider: mock 표시 | PASS |
| External call: No 표시 | PASS |
| AI provider registry: 연결됨 (mock only) 표시 | PASS |

---

## 6. 설계 원칙

| 원칙 | 준수 여부 |
|------|----------|
| Mock provider만 사용 | PASS |
| 외부 AI API 호출 없음 | PASS |
| Provider registry 경로 검증 | PASS |
| 기존 raw ERP context 유지 | PASS |
| 기존 deterministic briefing 유지 | PASS |
| /ceo_briefing 웹 라우트 동작 | PASS |
| 권한 체크 유지 | PASS |

---

## 7. #32 Close 판단

| 기준 | 상태 |
|------|------|
| CEO briefing flow가 provider registry 경유 | PASS |
| `get_ceo_briefing`에 provider metadata 포함 | PASS |
| `get_ceo_briefing`에 mock provider response 포함 | PASS |
| Raw ERP context 유지 | PASS |
| Deterministic briefing 유지 | PASS |
| `/ceo_briefing` 웹 라우트 동작 | PASS |
| 외부 AI provider 미호출 | PASS |
| 문서 생성 | PASS |

**판정**: #32 close 가능.

---

**문서 버전**: v1.0
**작성일**: 2026-05-18
**상태**: 구현 완료 — #32 close 대상
