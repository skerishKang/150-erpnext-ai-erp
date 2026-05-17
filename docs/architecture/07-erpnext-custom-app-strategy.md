# ERPNext Custom App 전략: Padiem AI Module v1

| 항목 | 내용 |
|------|------|
| 문서 버전 | v1.0 |
| 작성일 | 2026-05-18 |
| 대상 | Padiem AI ERP 첫 개발 |
| 상태 | Draft |

---

## 1. 전략 요약

### 핵심 원칙

**ERPNext core를 직접 수정하지 않는다.**

Padiem AI ERP의 모든 AI 기능은 Frappe Custom App 방식으로 ERPNext 위에 얹습니다. ERPNext 표준 모듈(Selling, Buying, Stock, Accounts 일부)은 그대로 사용하고, AI 기능은 ERP 데이터 위에 별도 레이어로 설계합니다.

### 전략 한 줄

**"Extend, do not fork."** — 가져다 쓰고, 고치지 않는다.

### 실천 사항

| 원칙 | 설명 |
|------|------|
| Core 미수정 | ERPNext 표준 코드를 직접 수정하지 않음 |
| Custom App 확장 | Padiem AI 기능은 `padiem_ai` Custom App으로 구현 |
| 표준 모듈 그대로 | Selling, Buying, Stock 등 표준 모듈은 그대로 사용 |
| AI 별도 레이어 | AI 기능은 ERP 데이터 위에 얹는 독립 레이어 |

---

## 2. 왜 core fork를 피해야 하는가

### Core 수정의 위험성

| 위험 | 설명 |
|------|------|
| **업데이트 불가** | ERPNext 새 버전으로 업데이트할 때 충돌 발생 |
| **유지보수 비용 증가** | 고객별 분기 코드 관리 필요 |
| **보안 패치 적용 어려움** | ERPNext 보안 패치가 core 수정과 충돌할 수 있음 |
| **고객별 분기 관리** | 고객마다 다른 core 수정본 관리 위험 |
| **커뮤니티 기여 불가** | core를 수정하면 ERPNext 커뮤니티에 기여할 수 없음 |

### Custom App의 장점

| 장점 | 설명 |
|------|------|
| **업그레이드 용이** | ERPNext 업데이트 시 Custom App만 테스트하면 됨 |
| **독립적 개발** | Custom App만 별도로 개발, 테스트, 배포 가능 |
| **고객별 확장** | 고객별 Custom App 분리 가능 |
| **커뮤니티 호환** | ERPNext 표준 기능을 그대로 사용 |
| **안전한 MVP** | core를 건드리지 않으므로 실패해도 안전 |

### 결론

**초기 MVP에서는 확장 방식이 더 안전합니다.**

core를 수정하면 나중에 되돌리기 어렵습니다. Custom App으로 시작하면 실패해도 Custom App만 제거하면 됩니다.

---

## 3. Custom App 기본 구조

### 이름 구분

| 구분 | 이름 | 설명 |
|------|------|------|
| Frappe app name | `padiem_ai` | 코드, 디렉토리, API 경로에서 사용 |
| Product name | Padiem AI ERP | 사용자-facing 이름, 마케팅, 문서에서 사용 |

문서 전체에서 앱 이름은 `padiem_ai`, 제품명은 Padiem AI ERP로 통일합니다.

### 디렉토리 구조

```
padiem_ai/                          ← Frappe app root
├── hooks.py                        # Frappe hooks
├── setup.py                        # 패키지 설정
├── requirements.txt                # Python 의존성
└── padiem_ai/                      ← Python package
    ├── __init__.py
    ├── api/                        # Backend API endpoints
    │   ├── __init__.py
    │   ├── briefing.py             # CEO Daily Briefing
    │   ├── query.py                # Natural-language ERP Query
    │   ├── quotation.py            # Quotation Draft Assistant
    │   ├── receivables.py          # Receivables Summary
    │   ├── delivery_stock.py       # Delivery & Stock Summary
    │   └── accountant.py           # Accountant Package Status
    ├── ai/                         # AI provider abstraction
    │   ├── __init__.py
    │   ├── base.py                 # Abstract base class
    │   ├── deepseek.py             # DeepSeek adapter
    │   ├── openai.py               # OpenAI adapter
    │   ├── claude.py               # Claude adapter
    │   └── mock.py                 # Mock adapter (개발/테스트용)
    ├── prompts/                    # AI prompt templates
    │   ├── briefing.json
    │   ├── query.json
    │   ├── quotation_draft.json
    │   └── receivables.json
    ├── data/                       # ERP data retrieval
    │   ├── __init__.py
    │   ├── sales.py
    │   ├── purchase.py
    │   ├── inventory.py
    │   └── master.py
    ├── audit/                      # Audit logging
    │   ├── __init__.py
    │   └── log.py
    ├── dashboard/                  # CEO dashboard logic
    │   ├── __init__.py
    │   └── page.py
    ├── page/                       # Frappe Custom Page definitions
    │   └── padiem_dashboard/
    │       └── padiem_dashboard.js
    └── public/                     # Frontend assets
        ├── js/
        │   └── padiem_dashboard.js
        └── css/
            └── padiem_dashboard.css
```

### 각 레이어 역할

| 레이어 | 역할 | 언어 |
|--------|------|------|
| **api/** | Frappe whitelisted API endpoints | Python |
| **ai/** | AI provider abstraction (DeepSeek, OpenAI 등) | Python |
| **prompts/** | AI prompt templates | JSON |
| **data/** | ERPNext 데이터 조회 레이어 | Python |
| **audit/** | AI 요청/응답 로그 | Python |
| **dashboard/** | CEO 대시보드 로직 | Python |
| **page/** | Frappe Custom Page 정의 | JavaScript |
| **public/** | Frontend assets (JS, CSS) | JavaScript, CSS |

---

## 4. 첫 구현 대상

### v1 구현 우선순위

| 순위 | 기능 | API | 설명 |
|------|------|-----|------|
| 1 | AI CEO Dashboard Custom Page | - | 대시보드 페이지 자체 |
| 2 | Natural-language ERP Query API | `/api/method/padiem_ai.api.query` | 한국어로 ERP 데이터 조회 |
| 3 | CEO Daily Briefing API | `/api/method/padiem_ai.api.briefing` | 매일 아침 현황 요약 |
| 4 | Receivables Summary API | `/api/method/padiem_ai.api.receivables` | 미수금 현황 요약 |
| 5 | Quotation Draft Assistant API | `/api/method/padiem_ai.api.quotation` | 견적서 초안 생성 |
| 6 | Delivery & Stock Summary API | `/api/method/padiem_ai.api.delivery_stock` | 배송/재고 요약 |
| 7 | Accountant Package Status API | `/api/method/padiem_ai.api.accountant` | 회계사 자료 상태 |

### 구현 단계

```
Phase 1: Custom App skeleton
  └── hooks.py, setup.py, 기본 디렉토리 구조

Phase 2: CEO Dashboard Custom Page
  └── Frappe Custom Page, 기본 레이아웃

Phase 3: Read-only ERP query APIs
  └── briefing, receivables, delivery_stock, accountant

Phase 4: AI provider abstraction 연결
  └── DeepSeek adapter, mock adapter

Phase 5: Quotation draft assistant
  └── quotation draft API, 초안 생성 로직

Phase 6: Audit/logging/permission hardening
  └── AI audit log, 권한 강화
```

---

## 5. ERPNext 데이터 접근 원칙

### 기본 원칙

| 원칙 | 설명 |
|------|------|
| **ORM 사용** | `frappe.get_all`, `frappe.get_doc` 등 Frappe ORM 사용 |
| **직접 DB 쿼리 기본 금지** | `frappe.db.sql` 사용 금지. 예외적으로 성능상 필요한 경우 CTO 승인 후 사용 |
| **권한 우회 금지** | `ignore_permissions=True` 사용 금지 |
| **Role-based permission** | ERPNext Role Permission Manager 준수 |
| **데이터 제한** | AI가 볼 수 있는 데이터는 사용자가 볼 수 있는 데이터로 제한 |

### 올바른 데이터 접근 예시

```python
# 올바른 방법: Frappe ORM 사용
def get_overdue_invoices():
    return frappe.get_all(
        "Sales Invoice",
        filters={
            "outstanding_amount": [">", 0],
            "due_date": ["<", frappe.utils.today()],
            "docstatus": 1
        },
        fields=["name", "customer", "outstanding_amount", "due_date"]
    )
```

```python
# 잘못된 방법: 직접 DB 쿼리
def get_overdue_invoices():
    return frappe.db.sql("""
        SELECT name, customer, outstanding_amount, due_date
        FROM `tabSales Invoice`
        WHERE outstanding_amount > 0 AND due_date < CURDATE()
    """, as_dict=True)
```

### 권한 확인

```python
# API 호출 시 사용자 권한 확인
@frappe.whitelist()
def get_ceo_briefing():
    # 사용자가 Sales Invoice를 읽을 수 있는지 확인
    if not frappe.has_permission("Sales Invoice", "read"):
        frappe.throw("Sales Invoice 읽기 권한이 없습니다.")

    # 데이터 조회
    invoices = frappe.get_all(...)

    return {"invoices": invoices}
```

---

## 6. AI 기능별 구현 위치

### 기능별 상세

| 기능 | ERPNext 데이터 | Backend API | Frontend 위치 | 저장 | 사람 승인 |
|------|---------------|-------------|---------------|------|----------|
| **CEO Daily Briefing** | Sales Invoice, Sales Order, Payment Entry, Stock Entry | `/api/method/padiem_ai.api.briefing.get` | Custom Page 상단 카드 | 저장 안 함 | 불필요 (조회만) |
| **자연어 ERP Query** | 모든 DocType | `/api/method/padiem_ai.api.query.search` | Custom Page 우측 패널 | 저장 안 함 | 불필요 (조회만) |
| **Quotation Draft** | Customer, Item, Price List | `/api/method/padiem_ai.api.quotation.draft` | Custom Page 하단 입력줄 | **HITL 승인 후 별도 PR에서 검토** | **필요** |
| **Receivables Summary** | Sales Invoice, Customer | `/api/method/padiem_ai.api.receivables.get` | Custom Page 하단 좌측 카드 | 저장 안 함 | 불필요 (조회만) |
| **Delivery & Stock** | Sales Order, Delivery Note, Stock Entry, Item, Bin | `/api/method/padiem_ai.api.delivery_stock.get` | Custom Page 하단 중앙 카드 | 저장 안 함 | 불필요 (조회만) |
| **Accountant Package** | Sales Invoice, Purchase Invoice, Payment Entry, Stock Entry | `/api/method/padiem_ai.api.accountant.get` | Custom Page 하단 우측 카드 | 저장 안 함 | 불필요 (조회만) |

### API 응답 구조 (통일)

```python
# 모든 API 응답은 다음 구조를 따름
{
    "success": True,
    "data": {
        # 실제 데이터
    },
    "ai_summary": "AI가 생성한 요약 텍스트",
    "timestamp": "2026-05-18T09:00:00"
}
```

### AI provider 호출 구조

```python
# 각 API endpoint에서 AI provider 호출
@frappe.whitelist()
def get_ceo_briefing():
    # 1. ERP 데이터 조회
    context = BriefingContextBuilder().build(frappe.session.user)

    # 2. AI provider에 프롬프트 전달
    provider = get_ai_provider()
    response = provider.generate(
        prompt=load_prompt("briefing"),
        context=context,
        schema=BRIEFING_SCHEMA
    )

    # 3. 응답 반환
    return {
        "success": True,
        "data": context,
        "ai_summary": response["summary"],
        "timestamp": frappe.utils.now()
    }
```

---

## 7. Custom Page 전략

### 페이지 경로

**`/app/padiem-ai-dashboard`**

또는

**`/app/padiem-dashboard`**

### 페이지 구조

```
┌──────────────────────────────────────────────────────────┐
│  Padiem AI ERP - CEO Dashboard                           │
│  (Frappe Custom Page)                                    │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  CEO Daily Briefing Card (전체 폭)                │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────────┐    │
│  │ Action   │ │ KPI Cards│ │ AI Query Panel        │    │
│  │ Items    │ │          │ │                       │    │
│  └──────────┘ └──────────┘ └──────────────────────┘    │
│                                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────────┐    │
│  │Receivables│ │ Delivery │ │ Accountant Package   │    │
│  │ Summary  │ │ & Stock  │ │ Status               │    │
│  └──────────┘ └──────────┘ └──────────────────────┘    │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Quotation Draft Input (전체 폭)                  │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

### ERPNext Desk과의 관계

| 항목 | v1 | v2 |
|------|----|----|
| Custom Page | CEO Dashboard 1개 | 역별별 대시보드 추가 |
| Desk Workspace | 기존 Workspace 유지 | Custom Workspace 추가 |
| 메뉴 | "Padiem AI" 메뉴 추가 | 역할별 메뉴 분리 |
| 접근 권한 | 관리자, CEO만 접근 | 역할별 접근 권한 분리 |

### Frappe Custom Page 등록

> **Note**: 아래 코드는 전략 문서용 pseudo-code입니다. 실제 구현 PR에서 Frappe Custom Page 등록 방식으로 검증합니다.

```python
# hooks.py (concept only)
app_name = "padiem_ai"

# Custom Page 등록 (실제 구현 시 Frappe 방식으로 검증)
page_info = {
    "padiem-dashboard": {
        "title": "Padiem AI Dashboard",
        "icon": "octicon octicon-graph",
        "type": "page",
        "link": "/app/padiem-dashboard",
        "label": "Padiem AI"
    }
}
```

---

## 8. Hooks 전략

### v1에서 사용할 Hooks

| Hook | 용도 | v1 포함 |
|------|------|---------|
| `app_include_js` | Frontend JS 파일 로드 | 예 |
| `app_include_css` | Frontend CSS 파일 로드 | 예 |
| `fixtures` | Custom Field, Role 등 고정 데이터 | 예 |
| `doc_events` | DocType 이벤트 후크 | **최소화** |
| `scheduled_tasks` | 정기 실행 작업 | **v2에서 검토** |
| `notification` | 알림 후크 | **v1에서 제외** |
| `email` | 이메일 후크 | **v1에서 제외** |

### v1 hooks.py 예시

```python
# hooks.py

app_name = "padiem_ai"
app_title = "Padiem AI"
app_publisher = "Padiem"
app_description = "AI ERP for Korean SMEs"
app_version = "0.1.0"

# Frontend assets
app_include_js = [
    "/assets/padiem_ai/js/padiem_dashboard.js"
]
app_include_css = [
    "/assets/padiem_ai/css/padiem_dashboard.css"
]

# Fixtures (Custom Field, Role 등)
fixtures = [
    "Custom Field",
    "Role"
]
```

### doc_events는 v1에서 최소화

v1에서는 doc_events를 사용하지 않습니다. AI 기능은 사용자가 직접 API를 호출하는 방식으로 동작합니다.

**v2에서 검토할 doc_events**:
- `on_submit` of Sales Invoice → 미수금 알림
- `on_update` of Sales Order → 납기 알림

### notification/email hooks는 v1에서 제외

자동 발송 위험 때문에 v1에서는 notification/email hooks를 사용하지 않습니다. 모든 알림과 이메일은 사람이 직접 발송합니다.

---

## 9. Custom Fields 전략

### v1에서는 Custom Fields를 최소화한다

| 후보 | v1 포함 | 설명 |
|------|---------|------|
| AI summary cache field | 아니오 | 초기에는 만들지 않음 |
| AI audit log DocType | 아니오 | v1.5 또는 v2 후보 |
| Quotation draft status | 아니오 | 실제 저장 기능 들어갈 때 검토 |
| AI response cache | 아니오 | v2에서 검토 |

### v1에서 Custom Field가 필요한 경우

v1에서는 Custom Field를 만들지 않습니다. 모든 AI 출력은 화면에서만 표시하고 ERPNext DocType에는 저장하지 않습니다.

### v2에서 검토할 Custom Fields

| Custom Field | 대상 DocType | 용도 |
|-------------|-------------|------|
| `ai_summary` | Sales Invoice | AI가 생성한 요약 저장 |
| `ai_draft_status` | Quotation | 초안 상태 추적 |
| `ai_last_briefing` | Company | 마지막 브리핑 시간 |

---

## 10. 보안 및 감사 원칙

### 기본 원칙

| 원칙 | 설명 |
|------|------|
| **API key 커밋 금지** | API key, secret, password를 코드에 포함하지 않음 |
| **AI 요청/응답 로그** | 개인정보·거래정보 포함 가능성이 있으므로 설계 필요 |
| **v1에서는 로그 최소화** | 필수 로그만 기록, 상세 로그는 v2에서 확장 |
| **고객 데이터 외부 전송** | 기본값은 mock/local-safe mode로 시작. 외부 provider 사용은 관리자 설정과 명시적 동의 후 활성화. 외부 전송 시 최소 필요 데이터만 전달 |
| **Role-based access** | 관리자만 AI provider 설정 가능 |
| **사용자 권한 준수** | AI가 볼 수 있는 데이터는 사용자가 볼 수 있는 데이터로 제한 |

### AI API key 관리

AI provider credential은 site_config 또는 환경변수에 저장하며, 저장 방식은 배포 환경별로 검토합니다. 문서와 Git에는 절대 기록하지 않습니다.

```python
# site_config.json 또는 환경변수 (concept only)
{
    "padiem_ai_provider": "deepseek",
    "padiem_ai_api_key": "<configured outside git>"
}
```

`site_config.json`은 `.gitignore`에 포함되어 있어야 합니다.

### AI Audit Log (v2 후보)

v1에서는 간단한 로그만 기록합니다. v2에서 AI Audit Log DocType을 만들 수 있습니다.

| 필드 | 설명 |
|------|------|
| user | AI 기능을 호출한 사용자 |
| action | briefing, query, draft 등 |
| timestamp | 호출 시간 |
| success | 성공/실패 여부 |

**v1에서는**:
- AI 요청/응답 전체를 로그에 기록하지 않음
- 개인정보 포함 가능성이 있으므로 최소한만 기록

---

## 11. 하지 않을 것

### 명확한 제외 항목

| 하지 않을 것 | 이유 |
|-------------|------|
| **ERPNext core 직접 수정** | 업그레이드 불가, 유지보수 비용 증가 |
| **자동 전표 생성** | AI가 ERP 데이터를 자동으로 수정하지 않음 |
| **자동 이메일 발송** | 발송은 사람이 직접 해야 함 |
| **자동 승인** | 모든 AI 출력물은 사람 승인 후 실행 |
| **세무 신고/급여 처리** | v1 범위 외 |
| **고객별 하드코딩** | 모든 설정은 설정 파일에서 관리 |
| **직접 DB 쿼리** | Frappe ORM 사용 원칙, 직접 쿼리 기본 금지 (CTO 승인 예외) |
| **권한 우회** | `ignore_permissions=True` 사용 금지 |

### v1에서 하지 않지만 v2에서 검토할 것

| 항목 | v2 검토 시점 |
|------|-------------|
| doc_events hooks | 자동 알림 기능 추가 시 |
| scheduled tasks | 정기 브리핑 자동 생성 시 |
| Custom Fields | AI 출력을 ERP에 저장할 시 |
| notification/email hooks | 자동 알림 기능 추가 시 |
| AI Audit Log DocType | 상세 감사 로그 필요 시 |

---

## 12. 개발 단계 제안

### Phase 1: Custom App skeleton

**목표**: `padiem_ai` Custom App 기본 구조 생성

**작업**:
- `bench new-app padiem_ai` 실행 (로컬 개발 환경에서)
- hooks.py 설정
- 기본 디렉토리 구조 생성
- requirements.txt 작성

**결과물**: 설치 가능한 Custom App

---

### Phase 2: CEO Dashboard Custom Page

**목표**: Frappe Custom Page로 CEO Dashboard 페이지 생성

**작업**:
- Custom Page 등록 (hooks.py)
- 페이지 레이아웃 구현 (HTML/CSS/JS)
- ERPNext Desk 메뉴에 추가

**결과물**: `/app/padiem-dashboard` 접근 가능

---

### Phase 3: Read-only ERP query APIs

**목표**: ERPNext 데이터를 읽는 API 엔드포인트 구현

**작업**:
- briefing API (CEO Daily Briefing)
- receivables API (미수금 요약)
- delivery_stock API (배송/재고 요약)
- accountant API (회계사 자료 상태)

**결과물**: 4개 API 엔드포인트, 각각 JSON 응답 반환

---

### Phase 4: AI provider abstraction 연결

**목표**: AI provider와 ERP 데이터를 연결

**작업**:
- AI provider abstract base class 구현
- DeepSeek adapter 구현
- Mock adapter 구현 (개발/테스트용)
- API key 관리 (site_config.json)

**결과물**: AI provider 호출 가능, Mock adapter로 테스트 가능

---

### Phase 5: Quotation draft assistant

**목표**: 견적서 초안 생성 기능 구현

**작업**:
- quotation draft API 구현
- Customer, Item, Price List 데이터 조회
- AI가 견적서 초안 생성
- 사용자는 ERPNext 표준 Quotation 생성 화면에서 검토·수정 후 저장

**결과물**: 견적서 초안 생성 가능. 저장 기능은 별도 구현 PR에서 HITL 승인 흐름을 갖춘 뒤 검토

---

### Phase 6: Audit/logging/permission hardening

**목표**: 보안 및 감사 강화

**작업**:
- AI 요청/응답 로그 기록
- 권한 확인 강화
- 에러 처리 개선
- Rate limiting

**결과물**: 프로덕션 배포 가능 수준

---

## 13. 첫 개발 PR 후보

### 구현 순서

| 순위 | PR 제목 | 설명 |
|------|---------|------|
| 1 | `feat: create padiem_ai custom app skeleton` | Custom App 기본 구조 |
| 2 | `feat: add AI CEO dashboard custom page` | CEO Dashboard Custom Page |
| 3 | `feat: add read-only ERP summary APIs` | briefing, receivables, delivery_stock, accountant |
| 4 | `feat: connect AI provider abstraction` | DeepSeek/Mock adapter 연결 |
| 5 | `feat: add quotation draft assistant` | 견적서 초안 생성 |
| 6 | `feat: add audit logging and permission hardening` | 보안 강화 |

### PR 작성 원칙

- 각 PR은 1개 기능만 포함
- 테스트 코드 포함
- 문서 업데이트 포함
- ERPNext core 수정 없음

---

## 14. 성공 기준

### Custom App 성공 조건

| 조건 | 확인 방법 |
|------|-----------|
| `bench new-app`으로 생성 가능 | 로컬 환경에서 테스트 |
| `bench install-app`으로 설치 가능 | ERPNext에 설치 테스트 |
| ERPNext 업데이트 후에도 동작 | 업데이트 테스트 |
| Custom Page가 Desk에서 접근 가능 | 브라우저에서 확인 |
| API가 JSON 응답 반환 | curl/Postman 테스트 |
| AI provider Mock adapter 동작 | 개발 환경 테스트 |

---

**문서 버전**: v1.0
**작성일**: 2026-05-18
**상태**: Draft
