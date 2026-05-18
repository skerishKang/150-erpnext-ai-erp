# 15 - Sprint Pause and Next Work

| 항목 | 내용 |
|------|------|
| 문서 버전 | v1.0 |
| 작성일 | 2026-05-18 |
| 상태 | Sprint 일시 중단 |

---

## 1. 현재 상태 요약

### 완료된 작업

| # | 작업 | 상태 | 비고 |
|---|------|------|------|
| 1 | ERPNext Docker 구동 | 완료 | `frappe_docker` 기반, `pwd.yml` 사용 |
| 2 | Setup Wizard 완료 | 완료 | Padiem Demo Company, KRW, Korea |
| 3 | Desk 진입 확인 | 완료 | http://localhost:8080/desk |
| 4 | 데모 데이터 설계 | 완료 | 54개 레코드 (Customer 5, Supplier 5, Item 10, Warehouse 2, 트랜잭션 32) |
| 5 | CSV 준비 | 완료 | `samples/data/erpnext-demo/` 11개 파일 |
| 6 | Warehouse 테스트 import | 완료 | `warehouse_type: "Goods"` 오류 → 필드 제거 후 성공 |
| 7 | Customer 테스트 import | 완료 | `territory: "Seoul"` 오류 → `"Korea, Republic of"` 변경 후 성공 |
| 8 | Supplier 테스트 import | 미완료 | Docker 중단으로 중단 |
| 9 | Item 테스트 import | 미완료 | Docker 중단으로 중단 |
| 10 | 전체 54개 demo data import | 미완료 | 테스트 import 완료 후 진행 예정 |

### 백업 상태

| 항목 | 값 |
|------|-----|
| 백업 생성일 | 2026-05-18 07:16:39 |
| DB 백업 파일 | `20260518_071635-frontend-database.sql.gz` (904.6KB) |
| 설정 백업 파일 | `20260518_071635-frontend-site_config_backup.json` (149B) |
| 백업 경로 | Docker/Frappe site 내부 백업 경로: `/home/frappe/frappe-bench/sites/frontend/private/backups/` |
| 비고 | 백업 파일은 Git에 커밋하지 않음 |

### 알려진 CSV 수정 사항

| 파일 | 수정 내용 | 반영 여부 |
|------|-----------|----------|
| `01-warehouses.csv` | `Warehouse Type` 컬럼 제거 | 반영 완료 |
| `02-customers.csv` | Territory를 `"Korea, Republic of"`로 변경 | 반영 완료 |
| `03-suppliers.csv` | Territory를 `"Korea, Republic of"`로 변경 | 반영 완료 |
| `04-items.csv` | Item Group, UOM 값 확인 필요 | 미확인 |

---

## 2. 안전 중단 명령

Docker 컨테이너를 안전하게 멈추는 명령입니다. 데이터는 보존됩니다.

```bash
cd "G:\Ddrive\BatangD\task\workdiary\150-erpnext-ai-erp-lab\frappe_docker"
docker compose -f pwd.yml stop
```

**동작**: 모든 컨테이너를 중지하지만, 볼륨과 이미지는 보존됩니다.

**확인**:
```bash
docker ps -a --format "table {{.Names}}\t{{.Status}}" | grep frappe
```

중지된 컨테이너는 `Exited` 상태로 표시됩니다.

---

## 3. 재개 명령

나중에 다시 작업을 시작할 때 사용하는 명령입니다.

```bash
cd "G:\Ddrive\BatangD\task\workdiary\150-erpnext-ai-erp-lab\frappe_docker"
docker compose -f pwd.yml up -d
```

**접속 확인**:
```bash
docker ps
curl -s http://localhost:8080/desk | head -5
```

또는 브라우저에서 http://localhost:8080/desk 접속 확인.

**정상 동작 확인 후**:
- Administrator 계정으로 로그인한다. 현재 로컬 기본 비밀번호는 즉시 변경 필요하며 문서에 기록하지 않는다.
- Desk 진입 확인
- 이전 데이터(고객, 품목, 견적 등) 보존 여부 확인

---

## 4. 절대 금지 명령

다음 명령은 데이터를 영구적으로 삭제합니다. 절대 실행하지 마세요.

| 금지 명령 | 위험도 | 설명 |
|-----------|--------|------|
| `docker compose down -v` | **치명적** | 컨테이너 + 볼륨 전체 삭제 |
| `docker volume rm <volume>` | **치명적** | 특정 볼륨 삭제 |
| `docker system prune --volumes` | **치명적** | 사용하지 않는 모든 볼륨 삭제 |
| 백업 없이 컨테이너/볼륨 삭제 | **치명적** | 복구 불가 |

**안전한 대체 명령**:

| 목적 | 안전한 명령 |
|------|-----------|
| 컨테이너만 중지 | `docker compose -f pwd.yml stop` |
| 컨테이너 재시작 | `docker compose -f pwd.yml up -d` |
| 특정 컨테이너 재시작 | `docker compose -f pwd.yml restart <service>` |

---

## 5. 남은 Import 작업

### Phase 1: 나머지 테스트 import

| 순서 | DocType | 작업 | CSV 파일 |
|------|---------|------|----------|
| 1 | Supplier | 1개 테스트 import | `samples/data/erpnext-demo-test/test-supplier.csv` |
| 2 | Item | 1개 테스트 import | `samples/data/erpnext-demo-test/test-item.csv` |
| 3 | 검증 | Supplier Group, Item Group, UOM 값 확인 | - |

### Phase 2: CSV 필드 수정

| 작업 | 설명 |
|------|------|
| Supplier Group 확인 | "Raw Materials", "Components" 등 존재 여부 확인 |
| Item Group 확인 | "Raw Materials", "Components", "Construction Materials" 등 존재 여부 확인 |
| UOM 확인 | "Meter", "Set", "Bag", "Sheet", "Piece", "Hour" 등 존재 여부 확인 |
| 누락된 값 생성 | 없으면 ERPNext에서 수동 생성 또는 CSV에 포함 |

### Phase 3: 전체 import

| 순서 | DocType | 레코드 수 | CSV 파일 |
|------|---------|----------|----------|
| 1 | Warehouse | 2 | `01-warehouses.csv` |
| 2 | Customer | 5 | `02-customers.csv` |
| 3 | Supplier | 5 | `03-suppliers.csv` |
| 4 | Item | 10 | `04-items.csv` |
| 5 | Quotation | 7 | `05-quotations.csv` |
| 6 | Sales Order | 7 | `06-sales-orders.csv` |
| 7 | Purchase Order | 3 | `07-purchase-orders.csv` |
| 8 | Stock Entry | 5 | `08-stock-entries.csv` |
| 9 | Delivery Note | 4 | `09-delivery-notes.csv` |
| 10 | Sales Invoice | 4 | `10-sales-invoices.csv` |
| 11 | Payment Entry | 2 | `11-payment-entries.csv` |
| **합계** | | **54** | |

### Phase 4: 결과 문서화

- import 성공/실패 기록
- 발생한 오류 기록
- 수정한 CSV 필드 기록
- `docs/implementation/16-demo-data-full-import-log.md` 생성

---

## 6. 다음 구현 준비 상태

### 구현 가능한 작업 (Docker 불필요)

| 작업 | Issue | 상태 |
|------|-------|------|
| AI Feature Spec | #4 | 완료 (PR #11 머지) |
| Pilot Proposal | #5 | 완료 (PR #12 머지) |
| Dashboard Concept | #6 | 완료 (PR #13 머지) |
| AI Provider Abstraction | #7 | 완료 (PR #15 머지) |
| Custom App Strategy | #9 | 완료 (PR #14 머지) |
| Cloud Deployment Plan | #8 | 완료 (PR #16 머지) |
| Docker Pause/Resume | #1 | 진행 중 (이 문서) |

### 구현에 Docker 필요한 작업

| 작업 | 우선순위 | 설명 |
|------|---------|------|
| `padiem_ai` Custom App skeleton | 높음 | `bench new-app padiem_ai` 실행 |
| CEO Dashboard Custom Page | 높음 | Frappe Custom Page 구현 |
| Read-only ERP API | 높음 | briefing, receivables 등 API |
| AI Provider Mock 연결 | 중간 | MockProvider 구현 |
| Quotation Draft | 중간 | 견적서 초안 기능 |
| 전체 demo data import | 중간 | 54개 레코드 import |

---

## 7. 구현 전 확인해야 할 것

### Docker 재시작 전

- [ ] Docker Desktop 실행 상태 확인
- [ ] `frappe_docker` 디렉토리 존재 확인
- [ ] `pwd.yml` 파일 존재 확인
- [ ] 이전 백업 파일 존재 확인

### Docker 재시작 후

- [ ] 모든 컨테이너 healthy 확인
- [ ] http://localhost:8080/desk 접속 확인
- [ ] Administrator 로그인 확인
- [ ] 이전 데이터 보존 확인 (Customer, Item 등)

### import 작업 전

- [ ] 새 백업 생성
- [ ] CSV 파일 필드 값 확인 (Supplier Group, Item Group, UOM)
- [ ] 테스트 import (1~2개 레코드)
- [ ] 테스트 성공 시 전체 import 진행

### 구현 작업 전

- [ ] `padiem_ai` Custom App 구조 문서 확인
- [ ] AI Provider 인터페이스 문서 확인
- [ ] Dashboard 컨셉 문서 확인
- [ ] Feature Spec 문서 확인

---

## 8. Language Hygiene 검사

이 문서에 대한 language hygiene 검사 결과입니다.

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
**상태**: Sprint 일시 중단
**다음 단계**: Docker 재시작 → Supplier/Item 테스트 import → 전체 import
