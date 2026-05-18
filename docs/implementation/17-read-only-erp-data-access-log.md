# 17 - Read-Only ERP Data Access Layer Log

| 항목 | 내용 |
|------|------|
| 문서 버전 | v1.0 |
| 작성일 | 2026-05-18 |
| Issue | #26 |
| 브랜치 | `feat/issue-26-read-only-erp-data-layer` |
| 상태 | 구현 완료, Docker 테스트 통과 |

---

## 1. 작업 목적

padiem_ai Custom App 안에서 ERPNext demo data를 안전하게 읽어오는 read-only 데이터 접근 레이어를 구현합니다. 외부 AI 호출 없이, ERPNext에 들어간 demo data를 구조화된 summary로 반환합니다.

---

## 2. 생성/수정된 파일

| 파일 | 유형 | 설명 |
|------|------|------|
| `padiem_ai/padiem_ai/erp/__init__.py` | 신규 | ERP data retrieval 패키지 |
| `padiem_ai/padiem_ai/erp/read_only.py` | 신규 | Read-only 데이터 접근 함수 9개 |
| `padiem_ai/padiem_ai/api/briefing.py` | 수정 | Read-only 레이어 호출로 변경 |
| `docs/implementation/17-read-only-erp-data-access-log.md` | 신규 | 구현 로그 |

---

## 3. 구현된 함수

### read_only.py

| 함수 | 설명 | 반환 |
|------|------|------|
| `get_demo_counts()` | 모든 demo DocType 레코드 수 | dict (DocType → count) |
| `get_sales_summary()` | Sales Invoice/Sales Order 요약 | dict (total_invoiced, total_outstanding 등) |
| `get_purchase_summary()` | Purchase Order 요약 | dict (purchase_order_count, total 등) |
| `get_inventory_summary()` | Stock Entry/Item 요약 | dict (total_items, stock_items 등) |
| `get_receivables_summary()` | 미수금 요약 | dict (outstanding_invoice_count, invoices 등) |
| `get_quotation_summary()` | Quotation 요약 | dict (quotation_count, total_quoted_value 등) |
| `get_delivery_summary()` | Delivery Note 요약 | dict (delivery_note_count 등) |
| `get_payment_summary()` | Payment Entry 요약 | dict (payment_count, total_received 등) |
| `get_ceo_briefing_context()` | CEO 브리핑용 통합 context | dict (counts, sales, purchases, ... warnings) |

### briefing.py

| Endpoint | 함수 | 설명 |
|----------|------|------|
| `padiem_ai.api.briefing.get_ceo_briefing` | `get_ceo_briefing_context()` | CEO 브리핑 데이터 반환 |
| `padiem_ai.api.briefing.get_counts` | `get_demo_counts()` | DocType 카운트 반환 |

---

## 4. Docker 테스트 결과

### bench console 테스트

```
=== get_demo_counts ===
  Customer: 6
  Supplier: 6
  Item: 11
  Quotation: 5
  Sales Order: 5
  Purchase Order: 3
  Stock Entry: 5
  Delivery Note: 3
  Sales Invoice: 3
  Payment Entry: 2
  Warehouse: 8

=== get_ceo_briefing_context ===
Keys: ['counts', 'sales', 'purchases', 'inventory', 'receivables', 'quotations', 'deliveries', 'payments', 'warnings']

Sales:
  total_invoiced: 0 (draft invoices only, docstatus=0)
  total_outstanding: 0 (submitted invoices only)
  submitted_invoice_count: 0
  draft_invoice_count: 3
  sales_order_count: 5
  total_sales_order_value: 175,800,000

Purchases:
  purchase_order_count: 3
  total_purchase_order_value: 106,000,000

Inventory:
  total_items: 11
  stock_items: 10
  stock_entry_count: 5

Receivables:
  outstanding_invoice_count: 3
  total_outstanding: 108,800,000
  invoices:
    - ACC-SINV-2026-00003 (Gwangju Design Studio) 8,800,000 due 2026-06-07
    - ACC-SINV-2026-00002 (Busan Tech Solutions) 25,000,000 due 2026-07-06
    - ACC-SINV-2026-00001 (Seoul Build Corp) 75,000,000 due 2026-06-20

Quotations:
  quotation_count: 5
  total_quoted_value: 175,800,000

Payments:
  payment_count: 2
  total_received: 38,800,000
  total_paid: 0

Warnings:
  - 3건의 미수금 invoices (총 108,800,000원)
  - 5건의 Sales Order 진행 중

ALL TESTS PASSED
```

### 주요 관찰

| 항목 | 값 | 비고 |
|------|-----|------|
| Sales Invoice (submitted) | 0건 | draft만 존재 (docstatus=0) |
| Sales Invoice (draft) | 3건 | import 시 draft로 생성됨 |
| 미수금 | 108,800,000원 | draft invoices의 outstanding |
| Sales Order | 5건, 175,800,000원 | |
| Purchase Order | 3건, 106,000,000원 | |
| 입금 | 38,800,000원 | Payment Entry 2건 |

---

## 5. 설계 원칙

| 원칙 | 준수 여부 |
|------|----------|
| Read-only 접근만 | PASS — insert/update/delete 없음 |
| frappe.get_all/get_list만 사용 | PASS |
| ERPNext 권한 준수 | PASS — `frappe.has_permission` 사용 |
| 외부 AI API 호출 없음 | PASS |
| Credential 없음 | PASS |
| ERPNext core 수정 없음 | PASS |

---

## 6. #26 Close 판단

| 기준 | 상태 |
|------|------|
| `padiem_ai/padiem_ai/erp/read_only.py` 존재 | PASS |
| `padiem_ai/padiem_ai/api/briefing.py` 업데이트 | PASS |
| `get_ceo_briefing_context()` 구조화된 dict 반환 | PASS |
| py_compile 통과 | PASS |
| Docker 내부 bench console 테스트 | PASS |
| 문서 생성 | PASS |

**판정**: #26 close 가능.

---

**문서 버전**: v1.0
**작성일**: 2026-05-18
**상태**: 구현 완료 — #26 close 대상
