# 14 - Demo Data Test Import Log

## Date: 2026-05-18

## Summary

Small-scale test import of 4 DocTypes (Warehouse, Customer, Supplier, Item) before full CSV import.
Test executed via Frappe REST API (`frappe.client.insert`).

---

## 1. Backup

### Backup Created

| Item | Value |
|------|-------|
| Status | SUCCESS |
| Timestamp | 2026-05-18 07:16:39 |
| Site | frontend |
| Config File | `20260518_071635-frontend-site_config_backup.json` (149B) |
| Database File | `20260518_071635-frontend-database.sql.gz` (904.6KB) |
| Backup Path | `/home/frappe/frappe-bench/sites/frontend/private/backups/` |

### Backup Command

```bash
docker exec frappe_docker-frontend-1 bench --site frontend backup --compress
```

### Notes

- Backup file contains sensitive data (passwords, secrets) — NOT committed to git
- Backup can be restored if import fails catastrophically

---

## 2. Test Import Results

### Test 1: Warehouse

| Item | Value |
|------|-------|
| DocType | Warehouse |
| Method | REST API (`frappe.client.insert`) |
| Status | SUCCESS (after fix) |
| Created Record | `Test Warehouse - PDC` |

#### Initial Attempt — FAILED

**Payload**:
```json
{
  "doc": {
    "doctype": "Warehouse",
    "warehouse_name": "Test Warehouse",
    "company": "Padiem Demo Company",
    "warehouse_type": "Goods",
    "is_group": 0
  }
}
```

**Error**:
```
frappe.exceptions.LinkValidationError: Could not find Warehouse Type: Goods
```

**Root Cause**: `warehouse_type` 필드에 "Goods" 값이 ERPNext에 존재하지 않음.
현재 시스템에 존재하는 Warehouse Type은 `Transit` 뿐.

#### Fix Applied

- `warehouse_type` 필드를 아예 제거 (null 허용)

**Revised Payload**:
```json
{
  "doc": {
    "doctype": "Warehouse",
    "warehouse_name": "Test Warehouse",
    "company": "Padiem Demo Company",
    "is_group": 0
  }
}
```

**Result**: SUCCESS
```json
{
  "name": "Test Warehouse - PDC",
  "warehouse_name": "Test Warehouse",
  "company": "Padiem Demo Company",
  "warehouse_type": null,
  "is_group": 0
}
```

#### CSV 수정 필요 사항

| 필드 | 문제 | 수정 방향 |
|------|------|-----------|
| `Warehouse Type` | "Goods" 값이 존재하지 않음 | 필드 제거 또는 null 처리 |

---

### Test 2: Customer

| Item | Value |
|------|-------|
| DocType | Customer |
| Method | REST API (`frappe.client.insert`) |
| Status | SUCCESS (after fix) |
| Created Record | `Test Customer Corp` |

#### Initial Attempt — FAILED

**Payload**:
```json
{
  "doc": {
    "doctype": "Customer",
    "customer_name": "Test Customer Corp",
    "customer_type": "Company",
    "territory": "Seoul",
    "customer_group": "Commercial"
  }
}
```

**Error**:
```
frappe.exceptions.LinkValidationError: Could not find Territory: Seoul
```

**Root Cause**: `territory` 필드에 "Seoul" 값이 존재하지 않음.
Setup Wizard에서 생성된 Territory:
- `All Territories`
- `Korea, Republic of`
- `Rest Of The World`

#### Fix Applied

- `territory` 값을 `"Seoul"` → `"Korea, Republic of"` 변경

**Revised Payload**:
```json
{
  "doc": {
    "doctype": "Customer",
    "customer_name": "Test Customer Corp",
    "customer_type": "Company",
    "territory": "Korea, Republic of",
    "customer_group": "Commercial"
  }
}
```

**Result**: SUCCESS
```json
{
  "name": "Test Customer Corp",
  "customer_type": "Company",
  "customer_group": "Commercial",
  "territory": "Korea, Republic of"
}
```

#### CSV 수정 필요 사항

| 필드 | 문제 | 수정 방향 |
|------|------|-----------|
| `Territory` | "Seoul", "Busan", "Incheon" 등 개별 도시가 없음 | 모두 `"Korea, Republic of"` 로 변경 |

---

### Test 3: Supplier

| Item | Value |
|------|-------|
| DocType | Supplier |
| Method | REST API |
| Status | NOT TESTED (Docker unavailable) |

#### Reason for Incompletion

- Docker Desktop became unavailable mid-test
- API connection refused (`localhost:8080`)
- Cannot verify `supplier_group` field values

#### Expected Issues (Based on Customer Test)

| 필드 | 예상 문제 | 확인 필요 |
|------|-----------|-----------|
| `Territory` | "Ulsan", "Daegu" 등 개별 도시 없음 | `"Korea, Republic of"` 로 변경 필요 |
| `Supplier Group` | "Raw Materials", "Components" 등 존재 여부 미확인 | 확인 필요 |

---

### Test 4: Item

| Item | Value |
|------|-------|
| DocType | Item |
| Method | REST API |
| Status | NOT TESTED (Docker unavailable) |

#### Reason for Incompletion

- Docker Desktop became unavailable mid-test

#### Expected Issues

| 필드 | 예상 문제 | 확인 필요 |
|------|-----------|-----------|
| `Item Group` | "Raw Materials", "Components" 등 존재 여부 미확인 | 확인 필요 |
| `Stock UOM` | "Meter", "Set", "Bag" 등 존재 여부 미확인 | 확인 필요 |

---

## 3. Existing Master Data Reference

### Verified ERPNext System Values

Based on test import queries:

| DocType | Existing Values |
|---------|-----------------|
| Warehouse Type | `Transit` |
| Territory | `All Territories`, `Korea, Republic of`, `Rest Of The World` |
| Customer Group | `Commercial` (confirmed working) |
| Supplier Group | Not checked |
| Item Group | Not checked |
| UOM | Not checked |

---

## 4. Required CSV Field Corrections

### 01-warehouses.csv

| Column | Current Value | Required Change |
|--------|---------------|-----------------|
| `Warehouse Type` | `Goods` | Remove column entirely (leave blank) |

### 02-customers.csv

| Column | Current Value | Required Change |
|--------|---------------|-----------------|
| `Territory` | `Seoul`, `Busan`, `Incheon`, `Daejeon`, `Gwangju` | All → `Korea, Republic of` |

### 03-suppliers.csv

| Column | Current Value | Required Change |
|--------|---------------|-----------------|
| `Territory` | `Ulsan`, `Daegu`, `Jeju`, `Sejong`, `Gangwon` | All → `Korea, Republic of` |
| `Supplier Group` | `Raw Materials`, `Components`, etc. | Verify existence first |

### 04-items.csv

| Column | Current Value | Required Change |
|--------|---------------|-----------------|
| `Item Group` | `Raw Materials`, `Components`, etc. | Verify existence first |
| `Stock UOM` | `Meter`, `Set`, `Bag`, `Sheet`, `Piece`, `Hour` | Verify existence first |

### 05-11 Transaction CSVs

- May need field name adjustments based on ERPNext version
- Reference fields (Customer, Supplier, Item) must match exact names from master data
- Date format must be `YYYY-MM-DD`

---

## 5. Summary of Findings

### What Worked

- REST API authentication via `POST /api/method/login`
- `frappe.client.insert` endpoint for creating records
- Warehouse creation (without warehouse_type)
- Customer creation (with correct territory)

### What Failed

- `warehouse_type: "Goods"` — value does not exist
- `territory: "Seoul"` — value does not exist
- Docker connection mid-test — containers stopped

### Key Insights

1. **Link fields are strictly validated**: ERPNext rejects any value not in the database
2. **Setup Wizard creates limited master data**: Only 3 territories, 1 warehouse type
3. **Master data must be created first**: Territories, UOMs, Item Groups may need to be created before importing CSVs
4. **API approach works well**: REST API provides clear error messages for debugging

---

## 6. Next Steps (Recommended)

### Before Full Import

1. **Re-start Docker Desktop** and verify ERPNext containers are running
2. **Check remaining master data values**:
   - Supplier Group
   - Item Group
   - UOM (Units of Measure)
3. **Create missing master data** if needed (Territory, UOM, Item Group, etc.)
4. **Update all CSV files** with correct field values
5. **Re-test** Supplier and Item imports

### CSV Update Priority

1. **01-warehouses.csv**: Remove `Warehouse Type` column
2. **02-customers.csv**: Fix all Territory values to `"Korea, Republic of"`
3. **03-suppliers.csv**: Fix Territory values, verify Supplier Group
4. **04-items.csv**: Verify Item Group and UOM values

### Full Import (After Fixes)

1. Re-test with corrected CSVs (1 record each)
2. If all 4 tests pass → proceed to full import
3. Follow import order from `12-demo-data-import-strategy.md`

---

## 7. Rollback Plan

If full import causes issues:

```bash
# Restore from backup taken at 2026-05-18 07:16:39
docker exec frappe_docker-frontend-1 bench --site frontend restore \
  /home/frappe/frappe-bench/sites/frontend/private/backups/20260518_071635-frontend-database.sql.gz
```

---

**Test Date**: 2026-05-18
**Status**: PARTIAL — 2/4 tests completed before Docker stopped
**Next Action**: Fix CSVs, restart Docker, complete remaining tests
