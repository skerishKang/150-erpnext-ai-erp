# 12 - ERPNext Demo Data Import Strategy

## Date: 2026-05-18

## Summary

Analysis of data import methods for ERPNext demo data, with recommended approach for Padiem AI ERP MVP.

## Current Environment Status

### ERPNext Container Status

| Container | Status | Uptime |
|-----------|--------|--------|
| frappe_docker-frontend-1 | Running | 5 hours |
| frappe_docker-backend-1 | Running | 5 hours |
| frappe_docker-db-1 | Healthy | 5 hours |
| frappe_docker-websocket-1 | Running | 5 hours |
| frappe_docker-scheduler-1 | Running | 5 hours |
| frappe_docker-redis-cache-1 | Running | 5 hours |
| frappe_docker-redis-queue-1 | Running | 5 hours |
| frappe_docker-queue-long-1 | Running | 5 hours |
| frappe_docker-queue-short-1 | Running | 5 hours |

### Command Execution Test

- **bench command**: ✅ Working (`bench --site frontend list-sites`)
- **docker exec**: ✅ Working
- **REST API**: ⚠️ Requires authentication (PermissionError)
- **Python script**: ⚠️ Requires proper environment setup

---

## Data Import Methods Comparison

### Method 1: ERPNext UI Manual Input

**Description**: Enter data directly through ERPNext web interface

**Pros**:
- Simplest approach, no technical skills required
- Immediate validation and error messages
- Visual feedback on data entry
- Built-in help and documentation
- No risk of data corruption

**Cons**:
- Very time-consuming for 40+ records
- Manual data entry errors possible
- Difficult to reproduce or automate
- Not scalable for larger datasets
- Tedious for repetitive data

**Time Estimate**: 4-6 hours for all demo data

**Risk Level**: Low

**Best For**: Small datasets, initial testing, one-time setup

---

### Method 2: Data Import Tool (Built-in)

**Description**: Use ERPNext's built-in Data Import Tool with CSV/Excel files

**Pros**:
- Built-in ERPNext feature
- Supports CSV and Excel formats
- Bulk import capability
- Template generation available
- Progress tracking and error reporting
- Rollback capability on failure

**Cons**:
- Requires CSV file preparation
- Column mapping can be tricky
- Some fields may not import correctly
- Requires understanding of DocType structure
- May need multiple import passes

**Time Estimate**: 2-3 hours (including file preparation)

**Risk Level**: Medium

**Best For**: Medium datasets, structured data, repeatable imports

---

### Method 3: Frappe REST API

**Description**: Use Frappe's REST API endpoints to create records programmatically

**Pros**:
- Full programmatic control
- Can automate entire process
- Supports complex data relationships
- Can handle validation logic
- Repeatable and scriptable

**Cons**:
- Requires authentication setup
- API endpoints may be restricted
- Need to handle API errors
- Requires programming knowledge
- Rate limiting may apply

**Time Estimate**: 3-4 hours (including script development)

**Risk Level**: Medium

**Best For**: Automated workflows, CI/CD integration, complex data

---

### Method 4: bench console / Python Script

**Description**: Use Frappe's Python API directly through bench console or scripts

**Pros**:
- Direct access to Frappe framework
- Full control over data creation
- Can handle complex business logic
- Best performance for large datasets
- Can use Frappe's built-in methods

**Cons**:
- Requires Python knowledge
- Risk of data corruption if errors occur
- Need to handle transactions properly
- May bypass validation checks
- Requires careful error handling

**Time Estimate**: 2-4 hours (including script development)

**Risk Level**: High

**Best For**: Complex data, large datasets, custom logic

---

## Recommended Approach

### Primary Recommendation: Data Import Tool (Method 2)

**Why Recommended**:
1. **Safety**: Built-in validation and error handling
2. **Efficiency**: Bulk import capability
3. **Traceability**: Progress tracking and logging
4. **Rollback**: Can undo failed imports
5. **Balance**: Good balance of speed and safety

### Secondary Recommendation: bench console (Method 4)

**When to Use**:
- If Data Import Tool fails
- For complex data relationships
- For custom validation logic
- For performance-critical imports

---

## DocType Import Order

### Phase 1: Foundation Data (Must Import First)

**Order**: 1 → 2 → 3 → 4

#### 1. Company

**Why First**:
- Foundation for all other data
- Required for Warehouse, Item, Customer, Supplier
- Sets currency, country, fiscal year

**Import Method**: UI or Data Import Tool

**Dependencies**: None

---

#### 2. Customer

**Why Second**:
- Required for Sales Orders, Quotations, Invoices
- Independent of other master data
- Can be created before Items

**Import Method**: Data Import Tool

**Dependencies**: Company

---

#### 3. Supplier

**Why Third**:
- Required for Purchase Orders
- Independent of Customer data
- Can be created before Items

**Import Method**: Data Import Tool

**Dependencies**: Company

---

#### 4. Item

**Why Fourth**:
- Required for Sales Orders, Purchase Orders, Stock Entries
- Depends on Company for default warehouse
- Can reference Customer/Supplier later

**Import Method**: Data Import Tool

**Dependencies**: Company, Warehouse (optional)

---

### Phase 2: Supporting Data (Import After Phase 1)

**Order**: 5 → 6

#### 5. Warehouse

**Why Fifth**:
- Required for Stock Entries
- Depends on Company
- Can be created after Items (Items can reference later)

**Import Method**: Data Import Tool

**Dependencies**: Company

---

#### 6. UOM (Units of Measure)

**Why Sixth**:
- Required for Item definitions
- System has defaults, but custom UOMs may be needed
- Can be created alongside Items

**Import Method**: Data Import Tool or UI

**Dependencies**: None

---

### Phase 3: Transaction Data (Import After Phase 2)

**Order**: 7 → 8 → 9 → 10 → 11

#### 7. Quotation

**Why After Master Data**:
- References Customer and Item
- Foundation for Sales Orders
- Can be created before Sales Orders

**Import Method**: Data Import Tool

**Dependencies**: Customer, Item

---

#### 8. Sales Order

**Why After Quotation**:
- Can reference Quotation
- References Customer and Item
- Foundation for Delivery Notes and Invoices

**Import Method**: Data Import Tool

**Dependencies**: Customer, Item, Quotation (optional)

---

#### 9. Purchase Order

**Why After Sales Order**:
- References Supplier and Item
- Can be created independently
- Foundation for Stock Entries

**Import Method**: Data Import Tool

**Dependencies**: Supplier, Item

---

#### 10. Delivery Note

**Why After Sales Order**:
- References Sales Order
- References Customer, Item, Warehouse
- Foundation for Sales Invoice

**Import Method**: Data Import Tool

**Dependencies**: Sales Order, Customer, Item, Warehouse

---

#### 11. Sales Invoice

**Why After Delivery Note**:
- References Delivery Note or Sales Order
- References Customer, Item
- Foundation for Payment Entry

**Import Method**: Data Import Tool

**Dependencies**: Sales Order or Delivery Note, Customer, Item

---

### Phase 4: Financial Data (Import Last)

**Order**: 12 → 13

#### 12. Payment Entry

**Why Last**:
- References Sales Invoice
- References Customer
- Final step in sales cycle

**Import Method**: Data Import Tool or UI

**Dependencies**: Sales Invoice, Customer

---

#### 13. Stock Entry

**Why Last**:
- References Item, Warehouse
- Can be created independently
- Tracks inventory movements

**Import Method**: Data Import Tool

**Dependencies**: Item, Warehouse

---

## Import Execution Plan

### Pre-Import Checklist

- [ ] Verify ERPNext is running
- [ ] Backup current database
- [ ] Prepare CSV files for each DocType
- [ ] Validate CSV data format
- [ ] Test import with 1-2 records first

### Step-by-Step Process

#### Step 1: Backup Database

```bash
docker exec frappe_docker-frontend-1 bench --site frontend backup --compress
```

**Purpose**: Create restore point before import

**Output**: Backup files in `/home/frappe/frappe-bench/sites/frontend/private/backups/`

---

#### Step 2: Import Company (if not already done)

**Method**: UI or bench console

**Note**: Company may already exist from Setup Wizard

---

#### Step 3: Import Customers

**Method**: Data Import Tool

**Process**:
1. Go to Data Import Tool in ERPNext
2. Select DocType: Customer
3. Download template
4. Fill in customer data from demo plan
5. Upload and import
6. Verify import results

**Expected Records**: 5

---

#### Step 4: Import Suppliers

**Method**: Data Import Tool

**Process**:
1. Go to Data Import Tool
2. Select DocType: Supplier
3. Download template
4. Fill in supplier data
5. Upload and import
6. Verify import results

**Expected Records**: 5

---

#### Step 5: Import Items

**Method**: Data Import Tool

**Process**:
1. Go to Data Import Tool
2. Select DocType: Item
3. Download template
4. Fill in item data
5. Upload and import
6. Verify import results

**Expected Records**: 10

---

#### Step 6: Import Warehouses

**Method**: Data Import Tool

**Process**:
1. Go to Data Import Tool
2. Select DocType: Warehouse
3. Download template
4. Fill in warehouse data
5. Upload and import
6. Verify import results

**Expected Records**: 2

---

#### Step 7: Import Quotations

**Method**: Data Import Tool

**Process**:
1. Go to Data Import Tool
2. Select DocType: Quotation
3. Download template
4. Fill in quotation data with Customer and Item references
5. Upload and import
6. Verify import results

**Expected Records**: 5

---

#### Step 8: Import Sales Orders

**Method**: Data Import Tool

**Process**:
1. Go to Data Import Tool
2. Select DocType: Sales Order
3. Download template
4. Fill in sales order data
5. Upload and import
6. Verify import results

**Expected Records**: 5

---

#### Step 9: Import Purchase Orders

**Method**: Data Import Tool

**Process**:
1. Go to Data Import Tool
2. Select DocType: Purchase Order
3. Download template
4. Fill in purchase order data
5. Upload and import
6. Verify import results

**Expected Records**: 3

---

#### Step 10: Import Delivery Notes

**Method**: Data Import Tool

**Process**:
1. Go to Data Import Tool
2. Select DocType: Delivery Note
3. Download template
4. Fill in delivery note data
5. Upload and import
6. Verify import results

**Expected Records**: 3

---

#### Step 11: Import Sales Invoices

**Method**: Data Import Tool

**Process**:
1. Go to Data Import Tool
2. Select DocType: Sales Invoice
3. Download template
4. Fill in sales invoice data
5. Upload and import
6. Verify import results

**Expected Records**: 3

---

#### Step 12: Import Payment Entries

**Method**: Data Import Tool or UI

**Process**:
1. Go to Data Import Tool
2. Select DocType: Payment Entry
3. Download template
4. Fill in payment entry data
5. Upload and import
6. Verify import results

**Expected Records**: 2

---

#### Step 13: Import Stock Entries

**Method**: Data Import Tool

**Process**:
1. Go to Data Import Tool
2. Select DocType: Stock Entry
3. Download template
4. Fill in stock entry data
5. Upload and import
6. Verify import results

**Expected Records**: 5

---

## Rollback Methods

### Method 1: Database Backup Restore (Recommended)

**When to Use**: Complete rollback needed

**Process**:
1. Stop ERPNext containers
2. Restore database from backup
3. Restart containers
4. Verify restoration

**Command**:
```bash
# Restore from backup
docker exec frappe_docker-frontend-1 bench --site frontend restore /path/to/backup.sql.gz
```

**Pros**: Complete restoration, clean state
**Cons**: Loses all changes after backup

---

### Method 2: Manual Deletion via UI

**When to Use**: Partial rollback, few records

**Process**:
1. Go to each DocType list
2. Select records to delete
3. Delete records
4. Verify deletion

**Pros**: Selective deletion
**Cons**: Time-consuming, risk of missing records

---

### Method 3: bench console Deletion

**When to Use**: Programmatic deletion needed

**Process**:
1. Access bench console
2. Use Frappe API to delete records
3. Commit changes
4. Verify deletion

**Example**:
```python
# Delete all demo customers
frappe.db.sql("DELETE FROM `tabCustomer` WHERE customer_name LIKE '%Demo%'")
frappe.db.commit()
```

**Pros**: Fast, programmatic
**Cons**: Risk of data corruption, bypasses validation

---

## Risk Mitigation

### Pre-Import Risks

| Risk | Mitigation |
|------|------------|
| Data format errors | Validate CSV files before import |
| Missing required fields | Check DocType requirements |
| Duplicate records | Use unique identifiers |
| Invalid references | Import in correct order |

### Import Risks

| Risk | Mitigation |
|------|------------|
| Import failure | Test with small batch first |
| Partial import | Use transactions, rollback on error |
| Performance issues | Import during off-peak hours |
| Timeout errors | Increase timeout settings |

### Post-Import Risks

| Risk | Mitigation |
|------|------------|
| Data inconsistency | Verify all references |
| Missing relationships | Check linked documents |
| Validation errors | Run data integrity checks |
| Performance degradation | Monitor system resources |

---

## Success Criteria

### Import Success Indicators

- [ ] All 5 Customers created successfully
- [ ] All 5 Suppliers created successfully
- [ ] All 10 Items created successfully
- [ ] All 2 Warehouses created successfully
- [ ] All 5 Quotations created successfully
- [ ] All 5 Sales Orders created successfully
- [ ] All 3 Purchase Orders created successfully
- [ ] All 3 Delivery Notes created successfully
- [ ] All 3 Sales Invoices created successfully
- [ ] All 2 Payment Entries created successfully
- [ ] All 5 Stock Entries created successfully
- [ ] All records linked correctly
- [ ] No validation errors
- [ ] System performance acceptable

### Verification Steps

1. **Count Verification**: Check record counts match expected
2. **Link Verification**: Verify all references are valid
3. **Data Verification**: Spot-check random records
4. **UI Verification**: View records in ERPNext interface
5. **Report Verification**: Run basic reports to confirm data

---

## Alternative Approaches

### If Data Import Tool Fails

**Fallback 1**: bench console with Python scripts
**Fallback 2**: Manual UI entry for critical records
**Fallback 3**: REST API with authentication

### If Performance Issues Occur

**Option 1**: Import during off-peak hours
**Option 2**: Increase container resources
**Option 3**: Batch imports with delays

---

## Next Steps

1. **Prepare CSV Files**: Create CSV files for each DocType
2. **Test Import**: Test with 1-2 records first
3. **Backup Database**: Create backup before full import
4. **Execute Import**: Follow import order
5. **Verify Results**: Check all records imported correctly
6. **Document Issues**: Record any problems encountered
7. **Update Plan**: Adjust strategy based on results

---

## Conclusion

**Recommended Approach**: Data Import Tool (Method 2)

**Import Order**:
1. Company (if needed)
2. Customer
3. Supplier
4. Item
5. Warehouse
6. UOM
7. Quotation
8. Sales Order
9. Purchase Order
10. Delivery Note
11. Sales Invoice
12. Payment Entry
13. Stock Entry

**Key Success Factors**:
- Follow correct import order
- Backup before import
- Test with small batches
- Verify after each step
- Document any issues

**Risk Level**: Medium (with proper precautions)

**Estimated Time**: 3-4 hours total

---

**Strategy Date**: 2026-05-18
**Status**: Ready for Implementation
**Next Step**: Prepare CSV files for import
