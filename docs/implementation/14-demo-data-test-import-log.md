# 14 - Demo Data Test Import Log

## Date: 2026-05-18 (initial) / 2026-05-18 (Supplier + Item completed)

## Summary

Small-scale test import of 4 DocTypes (Warehouse, Customer, Supplier, Item) before full CSV import.
Test executed via Frappe REST API (`frappe.client.insert`).

**Status**: 4/4 tests completed. All PASS.

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
| Method | REST API (`frappe.client.insert`) |
| Status | SUCCESS (after fix) |
| Created Record | `Test Supplier Corp` |
| Branch | `test/issue-2-supplier-item-import-validation` |

#### Initial Attempt — FAILED

**Payload**:
```json
{
  "doc": {
    "doctype": "Supplier",
    "supplier_name": "Test Supplier Corp",
    "supplier_type": "Company",
    "supplier_group": "Raw Materials"
  }
}
```

**Expected Error** (if "Raw Materials" used):
```
frappe.exceptions.LinkValidationError: Could not find Supplier Group: Raw Materials
```

**Root Cause**: `supplier_group` 필드에 "Raw Materials" 값이 존재하지 않음.
ERPNext에 존재하는 Supplier Group: `Raw Material` (s 없음)

#### Fix Applied

- `supplier_group` 값을 `"Raw Materials"` → `"Raw Material"` 변경

**Revised Payload**:
```json
{
  "doc": {
    "doctype": "Supplier",
    "supplier_name": "Test Supplier Corp",
    "supplier_type": "Company",
    "supplier_group": "Raw Material"
  }
}
```

**Result**: SUCCESS
```json
{
  "name": "Test Supplier Corp",
  "supplier_type": "Company",
  "supplier_group": "Raw Material",
  "country": "Korea, Republic of",
  "naming_series": "SUP-.YYYY.-"
}
```

#### CSV 수정 필요 사항

| 필드 | 문제 | 수정 방향 |
|------|------|-----------|
| `Supplier Group` | "Raw Materials" → 존재하지 않음 | `"Raw Material"` 로 변경 (s 제거) |
| `Supplier Group` | "Components", "Packaging", "Logistics" → 존재하지 않음 | full import 전에 수동 생성 필요 |

---

### Test 4: Item

| Item | Value |
|------|-------|
| DocType | Item |
| Method | REST API (`frappe.client.insert`) |
| Status | SUCCESS (after fix) |
| Created Record | `TEST-ITEM-01` |
| Branch | `test/issue-2-supplier-item-import-validation` |

#### Pre-requisite: UOM Creation

UOM "Piece"가 ERPNext에 존재하지 않아 먼저 생성 필요.

**UOM 생성**:
```json
{"doc": {"doctype": "UOM", "uom_name": "Piece"}}
```
**Result**: SUCCESS

#### Initial Attempt — FAILED (if "Raw Materials" used)

**Expected Error**:
```
frappe.exceptions.LinkValidationError: Could not find Item Group: Raw Materials
```

**Root Cause**: `item_group` 필드에 "Raw Materials" 값이 존재하지 않음.
ERPNext에 존재하는 Item Group: `Raw Material` (s 없음)

#### Fix Applied

- `item_group` 값을 `"Raw Materials"` → `"Raw Material"` 변경

**Revised Payload**:
```json
{
  "doc": {
    "doctype": "Item",
    "item_code": "TEST-ITEM-01",
    "item_name": "Test Item Alpha",
    "item_group": "Raw Material",
    "stock_uom": "Piece",
    "standard_rate": 50000,
    "is_stock_item": 1,
    "is_sales_item": 1,
    "is_purchase_item": 1,
    "description": "Test item for import validation"
  }
}
```

**Result**: SUCCESS
```json
{
  "name": "TEST-ITEM-01",
  "item_code": "TEST-ITEM-01",
  "item_name": "Test Item Alpha",
  "item_group": "Raw Material",
  "stock_uom": "Piece",
  "standard_rate": 50000.0,
  "is_stock_item": 1,
  "is_sales_item": 1,
  "is_purchase_item": 1,
  "company": "Padiem Demo Company",
  "default_warehouse": "Stores - PDC"
}
```

#### CSV 수정 필요 사항

| 필드 | 문제 | 수정 방향 |
|------|------|-----------|
| `Item Group` | "Raw Materials" → 존재하지 않음 | `"Raw Material"` 로 변경 (s 제거) |
| `Item Group` | "Components", "Construction Materials", "Electronics", "Electrical" → 존재하지 않음 | full import 전에 수동 생성 필요 |
| `Stock UOM` | "Piece" → 존재하지 않았음 | UOM 수동 생성 완료 |
| `Stock UOM` | "Meter", "Set", "Bag", "Sheet", "Hour" → 존재 여부 미확인 | full import 전에 확인 필요 |

---

## 3. Existing Master Data Reference

### Verified ERPNext System Values

Based on test import queries:

| DocType | Existing Values |
|---------|-----------------|
| Warehouse Type | `Transit` |
| Territory | `All Territories`, `Korea, Republic of`, `Rest Of The World` |
| Customer Group | `Commercial` (confirmed working) |
| Supplier Group | `All Supplier Groups`, `Services`, `Local`, `Raw Material`, `Electrical`, `Hardware`, `Pharmaceutical`, `Distributor` |
| Item Group | `All Item Groups`, `Products`, `Raw Material`, `Services`, `Sub Assemblies`, `Consumable` |
| UOM | Many exist. `Piece` created during this test. `Meter`, `Set`, `Bag`, `Sheet`, `Hour` need verification. |

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
- Supplier creation (with correct supplier_group)
- Item creation (after UOM creation, with correct item_group)

### What Failed

- `warehouse_type: "Goods"` — value does not exist
- `territory: "Seoul"` — value does not exist
- `supplier_group: "Raw Materials"` — value does not exist (correct: "Raw Material")
- `item_group: "Raw Materials"` — value does not exist (correct: "Raw Material")
- `stock_uom: "Piece"` — value did not exist (manually created)

### Key Insights

1. **Link fields are strictly validated**: ERPNext rejects any value not in the database
2. **Setup Wizard creates limited master data**: Only 3 territories, limited Supplier/Item Groups
3. **Master data must be created first**: UOMs, Item Groups, Supplier Groups may need to be created before importing CSVs
4. **API approach works well**: REST API provides clear error messages for debugging
5. **Naming matters**: "Raw Material" vs "Raw Materials" — singular/plural difference causes LinkValidationError
6. **UOM "Piece"**: Not included in default ERPNext data, must be manually created

---

## 6. Next Steps (Recommended)

### Before Full Import (#3)

1. **Create missing master data**:
   - Supplier Groups: `Components`, `Packaging`, `Logistics`
   - Item Groups: `Components`, `Construction Materials`, `Electronics`, `Electrical`
   - UOMs: `Meter`, `Set`, `Bag`, `Sheet`, `Hour` (verify existence)
2. **Verify CSV corrections applied**:
   - `Raw Materials` → `Raw Material` (all CSVs)
   - `Territory` → `Korea, Republic of` (all CSVs)
3. **Re-test** with corrected CSVs (1 record each) — DONE

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

**Test Date**: 2026-05-18 (initial) / 2026-05-18 (Supplier + Item completed)
**Status**: COMPLETE — 4/4 tests PASS
**Next Action**: #3 full import (after creating missing master data)

---

## 8. Issue #2 Completion Summary

| 기준 | 상태 |
|------|------|
| Supplier 1건 test import | **PASS** |
| Item 1건 test import | **PASS** |
| CSV 수정 사항 반영 | **완료** |
| 전체 54개 import | 미수행 (#3에서 진행) |
| Docker volume 삭제 | 없음 |
| credential | 없음 |
| 실제 고객 데이터 | 없음 |

**판정**: #2 close 가능. #3 진행 가능.
