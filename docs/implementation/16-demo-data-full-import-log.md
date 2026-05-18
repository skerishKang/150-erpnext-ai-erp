# 16 - Demo Data Full Import Log

| 항목 | 내용 |
|------|------|
| 문서 버전 | v1.0 |
| 작성일 | 2026-05-18 |
| Issue | #3 |
| 브랜치 | `test/issue-3-full-demo-data-import` |
| main base | `30a0ed7` |
| 상태 | 전체 import 성공 |

---

## 1. 작업 목적

ERPNext fictional demo dataset 전체 import를 수행하고 결과를 문서화합니다.

---

## 2. Docker 환경

| 항목 | 값 |
|------|-----|
| Docker Desktop | 실행됨 |
| ERPNext site | `frontend` |
| bench 컨테이너 | `backend` (frappe_docker-backend-1) |
| padiem_ai 설치 | 확인됨 |
| Desk 접속 | 200 OK |

---

## 3. CSV Column Count 검사

```
PASS: all CSV rows have matching column counts
```

---

## 4. Fresh Backup

| 항목 | 값 |
|------|-----|
| 생성 시간 | 2026-05-18 19:16:56 |
| DB 백업 | `20260518_191653-frontend-database.sql.gz` (909KB) |
| Public files | `20260518_191653-frontend-files.tar` (10KB) |
| Private files | `20260518_191653-frontend-private-files.tar` (10KB) |
| 커밋 여부 | **커밋하지 않음** |

---

## 5. Missing Master Data 생성/확인

### Supplier Groups

| Group | 상태 |
|-------|------|
| Raw Material | 기존 존재 |
| Components | **생성** |
| Packaging | **생성** |
| Logistics | **생성** |

### Item Groups

| Group | 상태 |
|-------|------|
| Raw Material | 기존 존재 |
| Components | **생성** |
| Construction Materials | **생성** |
| Electronics | **생성** |
| Electrical | **생성** |

### Customer Groups

| Group | 상태 |
|-------|------|
| Commercial | 기존 존재 |
| Services | **생성** (Gwangju Design Studio용) |

### UOMs

| UOM | 상태 |
|-----|------|
| Meter | 기존 존재 |
| Set | 기존 존재 |
| Bag | 기존 존재 |
| Sheet | 기존 존재 |
| Piece | 기존 존재 (이전 테스트에서 생성) |
| Hour | 기존 존재 |

### Modes of Payment

| Mode | 상태 |
|------|------|
| Wire Transfer | 기존 존재 |
| Bank Transfer | **미존재** → CSV를 "Wire Transfer"로 수정 |

---

## 6. Import 순서

| 순서 | DocType | CSV 파일 | 레코드 수 |
|------|---------|----------|----------|
| 1 | Warehouse | 01-warehouses.csv | 2 |
| 2 | Customer | 02-customers.csv | 5 |
| 3 | Supplier | 03-suppliers.csv | 5 |
| 4 | Item | 04-items.csv | 10 |
| 5 | Quotation | 05-quotations.csv | 5 |
| 6 | Sales Order | 06-sales-orders.csv | 5 |
| 7 | Purchase Order | 07-purchase-orders.csv | 3 |
| 8 | Stock Entry | 08-stock-entries.csv | 5 |
| 9 | Delivery Note | 09-delivery-notes.csv | 3 |
| 10 | Sales Invoice | 10-sales-invoices.csv | 3 |
| 11 | Payment Entry | 11-payment-entries.csv | 2 |

---

## 7. Import 결과

### 전체 결과

| DocType | Expected | Imported | Failed | 상태 |
|---------|----------|----------|--------|------|
| Warehouse | 2 | 2 | 0 | PASS |
| Customer | 5 | 5 | 0 | PASS |
| Supplier | 5 | 5 | 0 | PASS |
| Item | 10 | 10 | 0 | PASS |
| Quotation | 5 | 5 | 0 | PASS |
| Sales Order | 5 | 5 | 0 | PASS |
| Purchase Order | 3 | 3 | 0 | PASS |
| Stock Entry | 5 | 5 | 0 | PASS |
| Delivery Note | 3 | 3 | 0 | PASS |
| Sales Invoice | 3 | 3 | 0 | PASS |
| Payment Entry | 2 | 2 | 0 | PASS |
| **합계** | **48** | **48** | **0** | **PASS** |

### 상세 결과

#### Warehouse (2/2 PASS)

| Record | 상태 |
|--------|------|
| Main Warehouse - PDC | OK |
| Busan Distribution Center - PDC | OK |

#### Customer (5/5 PASS)

| Record | 상태 | 비고 |
|--------|------|------|
| Seoul Build Corp | OK | |
| Busan Tech Solutions | OK | |
| Incheon Manufacturing | OK | |
| Daejeon Smart Farm | OK | |
| Gwangju Design Studio | OK | Customer Group "Services" 생성 필요 |

#### Supplier (5/5 PASS)

| Record | 상태 |
|--------|------|
| Korea Steel Distribution | OK |
| Dae gu Electronics | OK |
| Jeju Natural Materials | OK |
| Sejong Packaging Solutions | OK |
| Gangwon Logistics | OK |

#### Item (10/10 PASS)

| Record | 상태 |
|--------|------|
| STEEL-BEAM-100 | OK |
| ELEC-COMP-A | OK |
| CONCRETE-50KG | OK |
| ALUM-SHEET-2MM | OK |
| SMART-SENSOR-01 | OK |
| WOOD-PANEL-1224 | OK |
| LED-FIXTURE-01 | OK |
| SS-PIPE-50MM | OK |
| PVC-CABLE-2.5SQ | OK |
| SERVICE-INSTALL | OK |

#### Quotation (5/5 PASS)

| Record | Auto Name | 상태 |
|--------|-----------|------|
| Seoul Build Corp | SAL-QTN-2026-00001 | OK |
| Busan Tech Solutions | SAL-QTN-2026-00002 | OK |
| Incheon Manufacturing | SAL-QTN-2026-00003 | OK |
| Daejeon Smart Farm | SAL-QTN-2026-00004 | OK |
| Gwangju Design Studio | SAL-QTN-2026-00005 | OK |

#### Sales Order (5/5 PASS)

| Record | Auto Name | 상태 |
|--------|-----------|------|
| Seoul Build Corp | SAL-ORD-2026-00001 | OK |
| Busan Tech Solutions | SAL-ORD-2026-00002 | OK |
| Incheon Manufacturing | SAL-ORD-2026-00003 | OK |
| Daejeon Smart Farm | SAL-ORD-2026-00004 | OK |
| Gwangju Design Studio | SAL-ORD-2026-00005 | OK |

#### Purchase Order (3/3 PASS)

| Record | Auto Name | 상태 |
|--------|-----------|------|
| Korea Steel Distribution | PUR-ORD-2026-00001 | OK |
| Dae gu Electronics | PUR-ORD-2026-00002 | OK |
| Sejong Packaging Solutions | PUR-ORD-2026-00003 | OK |

#### Stock Entry (5/5 PASS)

| Record | Auto Name | 상태 |
|--------|-----------|------|
| SE-1 (Material Receipt) | MAT-STE-2026-00001 | OK |
| SE-2 (Material Issue) | MAT-STE-2026-00002 | OK |
| SE-3 (Material Receipt) | MAT-STE-2026-00003 | OK |
| SE-4 (Material Transfer) | MAT-STE-2026-00004 | OK |
| SE-5 (Material Receipt) | MAT-STE-2026-00005 | OK |

#### Delivery Note (3/3 PASS)

| Record | Auto Name | 상태 |
|--------|-----------|------|
| Seoul Build Corp | MAT-DN-2026-00001 | OK |
| Busan Tech Solutions | MAT-DN-2026-00002 | OK |
| Gwangju Design Studio | MAT-DN-2026-00003 | OK |

#### Sales Invoice (3/3 PASS)

| Record | Auto Name | 상태 |
|--------|-----------|------|
| Seoul Build Corp | ACC-SINV-2026-00001 | OK |
| Busan Tech Solutions | ACC-SINV-2026-00002 | OK |
| Gwangju Design Studio | ACC-SINV-2026-00003 | OK |

#### Payment Entry (2/2 PASS)

| Record | Auto Name | 상태 | 비고 |
|--------|-----------|------|------|
| Seoul Build Corp | ACC-PAY-2026-00001 | OK | "Bank Transfer" → "Wire Transfer" 수정, exchange rate 필드 추가 |
| Gwangju Design Studio | ACC-PAY-2026-00002 | OK | |

---

## 8. 발생한 오류와 해결

| 오류 | 원인 | 해결 |
|------|------|------|
| Customer Group "Services" 미존재 | CSV에서 사용한 그룹이 ERPNext에 없음 | API로 Customer Group "Services" 생성 |
| Mode of Payment "Bank Transfer" 미존재 | CSV에서 사용한 모드가 ERPNext에 없음 | CSV를 "Wire Transfer"로 수정 |
| Payment Entry "Target Exchange Rate is mandatory" | exchange rate 필드 누락 | CSV에 Source/Target Exchange Rate, Paid From/To 필드 추가 |
| UOM 생성 DuplicateEntryError | 이미 존재하는 UOM | 무시 (이전 테스트에서 이미 생성됨) |

---

## 9. CSV 수정 사항

| 파일 | 수정 내용 | 사유 |
|------|-----------|------|
| `11-payment-entries.csv` | "Bank Transfer" → "Wire Transfer" | ERPNext에 "Wire Transfer"만 존재 |
| `11-payment-entries.csv` | exchange rate 필드 추가 | Payment Entry 필수 필드 |

---

## 10. 최종 데이터 현황

| DocType | Demo Records | Test/Default Records | Total |
|---------|-------------|---------------------|-------|
| Warehouse | 2 | 6 (default) | 8 |
| Customer | 5 | 1 (test) | 6 |
| Supplier | 5 | 1 (test) | 6 |
| Item | 10 | 1 (test) | 11 |
| Quotation | 5 | 0 | 5 |
| Sales Order | 5 | 0 | 5 |
| Purchase Order | 3 | 0 | 3 |
| Stock Entry | 5 | 0 | 5 |
| Delivery Note | 3 | 0 | 3 |
| Sales Invoice | 3 | 0 | 3 |
| Payment Entry | 2 | 0 | 2 |

---

## 11. 제약 사항 확인

| 항목 | 상태 |
|------|------|
| Docker volume 삭제 | 없음 |
| credential 커밋 | 없음 |
| 실제 고객 데이터 | 없음 |
| backup 파일 커밋 | 없음 |
| ERPNext core 수정 | 없음 |
| 외부 AI API 호출 | 없음 |

---

## 12. #3 Close 판단

| 기준 | 상태 |
|------|------|
| 전체 demo dataset import | **48/48 PASS** |
| CSV column count 검증 | **PASS** |
| Desk 데이터 확인 | **PASS** |
| 오류 문서화 | **완료** |
| CSV 수정 | **완료** |

**판정**: #3 close 가능.

---

**문서 버전**: v1.0
**작성일**: 2026-05-18
**상태**: 전체 import 성공 — #3 close 대상
