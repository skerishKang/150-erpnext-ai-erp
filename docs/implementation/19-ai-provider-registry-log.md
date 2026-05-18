# 19 - AI Provider Registry Log

| 항목 | 내용 |
|------|------|
| 문서 버전 | v1.0 |
| 작성일 | 2026-05-18 |
| Issue | #19 |
| PR | #20 skeleton 위에 구축 |
| 상태 | Provider registry 구현 완료, Docker 검증은 #21에서 별도 진행 |

---

## 1. 작업 목적

PR #20으로 merge된 `padiem_ai` manual skeleton 위에 AI Provider Registry를 추가합니다. 이번 작업은 외부 AI API 연결이 아니라 provider 선택 구조와 placeholder 구조를 만드는 것입니다.

---

## 2. PR #20 Skeleton 위에 추가된 내용

| 파일 | 유형 | 설명 |
|------|------|------|
| `padiem_ai/ai/providers.py` | 신규 | MockProvider + PlaceholderProvider |
| `padiem_ai/ai/registry.py` | 신규 | Provider lookup, list, availability check |
| `padiem_ai/ai/__init__.py` | 수정 | 모든 주요 클래스/함수 export |
| `padiem_ai/ai/mock.py` | 수정 | providers.py에서 re-export (호환성) |
| `padiem_ai/README.md` | 수정 | Provider registry 상태 설명 추가 |

---

## 3. ProviderRegistry 구조

### 주요 함수

| 함수 | 입력 | 출력 | 설명 |
|------|------|------|------|
| `get_provider(name)` | provider 이름 | BaseAIProvider 인스턴스 | mock → MockProvider, 나머지 → PlaceholderProvider |
| `list_providers()` | 없음 | list of str | 지원하는 7개 provider 이름 |
| `is_provider_available(name)` | provider 이름 | bool | 지원 여부 확인 |
| `get_default_provider()` | 없음 | MockProvider | 기본 provider 반환 |

### 동작 원칙

- provider 이름은 lowercase normalize
- mock은 MockProvider 반환 (활성)
- kilocode/opencodego/nvidia/deepseek/mistral/ollama는 PlaceholderProvider 반환
- unknown provider 요청 시 ValueError 반환
- 외부 API 호출 없음

---

## 4. MockProvider 동작 방식

MockProvider는 외부 호출 없이 deterministic 응답을 반환합니다.

```python
# MockProvider 동작
provider = get_provider("mock")
provider.health_check()    # {"status": "ok", "provider": "mock", "latency_ms": 0}
provider.generate_text()    # "Mock response: AI integration pending."
provider.generate_json()    # {"summary": "Mock summary", "alerts": []}
provider.summarize()        # "Mock summary: AI integration pending."
```

---

## 5. PlaceholderProvider 동작 방식

PlaceholderProvider는 등록되었지만 구현되지 않은 provider입니다. 절대 네트워크 호출을 하지 않습니다.

```python
# PlaceholderProvider 동작
provider = get_provider("kilocode")
provider.health_check()    # {"status": "not_implemented", "provider": "kilocode", ...}
provider.generate_text()    # NotImplementedError 발생
provider.generate_json()    # NotImplementedError 발생
provider.summarize()        # NotImplementedError 발생
```

---

## 6. 지원 Provider 목록

| Provider | 상태 | 클래스 | 외부 호출 |
|----------|------|--------|----------|
| mock | 활성 | MockProvider | 없음 |
| kilocode | placeholder | PlaceholderProvider | 없음 |
| opencodego | placeholder | PlaceholderProvider | 없음 |
| nvidia | placeholder | PlaceholderProvider | 없음 |
| deepseek | placeholder | PlaceholderProvider | 없음 |
| mistral | placeholder | PlaceholderProvider | 없음 |
| ollama | placeholder | PlaceholderProvider | 없음 |

**실제 활성 provider**: mock only

---

## 7. #18/#21과의 관계

| Issue | 관계 |
|-------|------|
| #18 | skeleton 생성 이슈. 이 PR에서 닫지 않음 |
| #21 | Docker install verification. 별도 이슈로 유지 |
| #19 | 이 PR에서 닫음 (provider registry 구현 완료) |

---

## 8. Local Test Results

### py_compile

| 파일 | 결과 |
|------|------|
| `padiem_ai/ai/base.py` | OK |
| `padiem_ai/ai/providers.py` | OK |
| `padiem_ai/ai/registry.py` | OK |
| `padiem_ai/ai/mock.py` | OK |
| `padiem_ai/ai/__init__.py` | OK |

### Functional Tests

```
list_providers: ['mock', 'kilocode', 'opencodego', 'nvidia', 'deepseek', 'mistral', 'ollama']
count: 7

mock health_check: {'status': 'ok', 'provider': 'mock', 'latency_ms': 0}
mock provider_name: mock

kilocode provider_name: kilocode
kilocode health_check: {'status': 'not_implemented', 'provider': 'kilocode', ...}

is_provider_available(mock): True
is_provider_available(kilocode): True
is_provider_available(unknown): False

ValueError for unknown: Unknown provider: 'unknown_provider'. Supported providers: mock, kilocode, opencodego, nvidia, deepseek, mistral, ollama

ALL TESTS PASSED
```

---

## 9. 다음 단계

| 작업 | Issue | 설명 |
|------|-------|------|
| Docker install verification | #21 | `install-app` 및 API endpoint 테스트 |
| KiloCode/OpenCodeGo API spec 확인 | 새 Issue | 실제 provider adapter 설계 |
| Provider settings validation | 새 Issue | site_config 기반 provider 설정 검증 |
| CEO dashboard API 연결 | 새 Issue | briefing API에 provider 연결 |

---

## 10. Language Hygiene 검사

| 패턴 | 결과 |
|------|------|
| `�` | 0건 |
| `初期` | 0건 |
| `到期` | 0건 |
| `列表` | 0건 |
| `不满意` | 0건 |
| `有哪些` | 0건 |
| `미到期` | 0건 |

**검사 통과**: 모든 금지 패턴 0건 확인.

---

**문서 버전**: v1.0
**작성일**: 2026-05-18
**상태**: Provider registry 구현 완료
