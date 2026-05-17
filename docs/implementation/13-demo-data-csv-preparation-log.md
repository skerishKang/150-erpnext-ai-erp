# 13 - Demo Data CSV Preparation Log

## Date: 2026-05-18

## Summary

Prepared CSV files for ERPNext Data Import Tool based on demo data plan. Files are ready for import but NOT yet imported.

## Important Notice

**Status**: CSV files prepared, NOT imported yet
**Next Step**: Small-scale test import (1-2 records per DocType)

---

## Generated CSV Files

### Location

```
samples/data/erpnext-demo/
```

### File List (11 Files)

| # | File Name | DocType | Purpose | Records |
|---|-----------|---------|---------|---------|
| 1 | 01-warehouses.csv | Warehouse | Storage locations | 2 |
| 2 | 02-customers.csv | Customer | Customer master data | 5 |
| 3 | 03-suppliers.csv | Supplier | Supplier master data | 5 |
| 4 | 04-items.csv | Item | Product/service catalog | 10 |
| 5 | 05-quotations.csv | Quotation | Price quotes to customers | 7 |
| 6 | 06-sales-orders.csv | Sales Order | Customer orders | 7 |
| 7 | 07-purchase-orders.csv | Purchase Order | Supplier orders | 3 |
| 8 | 08-stock-entries.csv | Stock Entry | Inventory movements | 5 |
| 9 | 09-delivery-notes.csv | Delivery Note | Shipment tracking | 4 |
| 10 | 10-sales-invoices.csv | Sales Invoice | Customer billing | 4 |
| 11 | 11-payment-entries.csv | Payment Entry | Payment recording | 2 |

**Total Records**: 54

---

## CSV File Details

### 1. 01-warehouses.csv

**Purpose**: Define storage locations for inventory management

**Fields**:
- Warehouse Name: Name of the warehouse
- Company: Padiem Demo Company
- Warehouse Type: Goods
- Is Group: No (not a group warehouse)

**Records**:
1. Main Warehouse (Seoul)
2. Busan Distribution Center (Busan)

**Import Order**: 1st (foundation for inventory)

---

### 2. 02-customers.csv

**Purpose**: Create customer master data for sales transactions

**Fields**:
- Customer Name: Company name
- Customer Type: Company
- Territory: Geographic region
- Customer Group: Business category

**Records**:
1. Seoul Build Corp (Construction)
2. Busan Tech Solutions (IT/Electronics)
3. Incheon Manufacturing (Automotive)
4. Daejeon Smart Farm (Agriculture)
5. Gwangju Design Studio (Services)

**Import Order**: 2nd (required for sales transactions)

---

### 3. 03-suppliers.csv

**Purpose**: Create supplier master data for purchase transactions

**Fields**:
- Supplier Name: Company name
- Supplier Type: Company
- Territory: Geographic region
- Supplier Group: Business category

**Records**:
1. Korea Steel Distribution (Steel)
2. Dae gu Electronics (Electronics)
3. Jeju Natural Materials (Natural Products)
4. Sejong Packaging Solutions (Packaging)
5. Gangwon Logistics (Logistics)

**Import Order**: 3rd (required for purchase transactions)

---

### 4. 04-items.csv

**Purpose**: Define products and services for sales and purchases

**Fields**:
- Item Code: Unique identifier
- Item Name: Product name
- Item Group: Category
- Stock UOM: Unit of measure
- Standard Rate: Default price
- Is Stock Item: Track inventory
- Is Sales Item: Can be sold
- Is Purchase Item: Can be purchased
- Description: Product details

**Records**:
1. STEEL-BEAM-100 (Steel Beam 100mm)
2. ELEC-COMP-A (Electronic Component Set A)
3. CONCRETE-50KG (Concrete Mix 50kg)
4. ALUM-SHEET-2MM (Aluminum Sheet 2mm)
5. SMART-SENSOR-01 (Smart Sensor Module)
6. WOOD-PANEL-1224 (Wood Panel 1200x2400)
7. LED-FIXTURE-01 (LED Light Fixture)
8. SS-PIPE-50MM (Stainless Steel Pipe 50mm)
9. PVC-CABLE-2.5SQ (PVC Cable 2.5sq)
10. SERVICE-INSTALL (Installation Service)

**Import Order**: 4th (required for all transactions)

---

### 5. 05-quotations.csv

**Purpose**: Create price quotes to customers

**Fields**:
- Quotation No: Unique identifier
- Customer: Customer name (reference)
- Transaction Date: Quote date
- Valid Till: Quote expiry date
- Item Code: Product code (reference)
- Qty: Quantity
- Rate: Unit price

**Records**:
1. QTN-2026-001 (Seoul Build Corp - Steel Beams)
2. QTN-2026-002 (Busan Tech Solutions - Electronic Components)
3. QTN-2026-003 (Incheon Manufacturing - Aluminum + Steel Pipe)
4. QTN-2026-004 (Daejeon Smart Farm - Sensors)
5. QTN-2026-005 (Gwangju Design Studio - Wood + LED)

**Import Order**: 5th (foundation for sales orders)

---

### 6. 06-sales-orders.csv

**Purpose**: Record confirmed customer orders

**Fields**:
- Sales Order No: Unique identifier
- Customer: Customer name (reference)
- Transaction Date: Order date
- Delivery Date: Expected delivery
- Item Code: Product code (reference)
- Qty: Quantity
- Rate: Unit price

**Records**:
1. SO-2026-001 (Seoul Build Corp - Steel Beams)
2. SO-2026-002 (Busan Tech Solutions - Electronic Components)
3. SO-2026-003 (Incheon Manufacturing - Aluminum + Steel Pipe)
4. SO-2026-004 (Daejeon Smart Farm - Sensors)
5. SO-2026-005 (Gwangju Design Studio - Wood + LED)

**Import Order**: 6th (required for delivery and invoicing)

---

### 7. 07-purchase-orders.csv

**Purpose**: Record orders to suppliers

**Fields**:
- Purchase Order No: Unique identifier
- Supplier: Supplier name (reference)
- Transaction Date: Order date
- Schedule Date: Expected receipt
- Item Code: Product code (reference)
- Qty: Quantity
- Rate: Unit price

**Records**:
1. PO-2026-001 (Korea Steel Distribution - Steel Beams)
2. PO-2026-002 (Dae gu Electronics - Electronic Components)
3. PO-2026-003 (Sejong Packaging Solutions - Concrete)

**Import Order**: 7th (required for stock receipts)

---

### 8. 08-stock-entries.csv

**Purpose**: Record inventory movements (receipts, issues, transfers)

**Fields**:
- Stock Entry No: Unique identifier
- Stock Entry Type: Material Receipt/Issue/Transfer
- Posting Date: Movement date
- Item Code: Product code (reference)
- Qty: Quantity
- Source Warehouse: Where from (for issues/transfers)
- Target Warehouse: Where to (for receipts/transfers)

**Records**:
1. STE-2026-001 (Steel Beam receipt)
2. STE-2026-002 (Steel Beam issue)
3. STE-2026-003 (Electronic Components receipt)
4. STE-2026-004 (Electronic Components transfer)
5. STE-2026-005 (Wood Panel receipt)

**Import Order**: 8th (updates inventory levels)

---

### 9. 09-delivery-notes.csv

**Purpose**: Record shipments to customers

**Fields**:
- Delivery Note No: Unique identifier
- Customer: Customer name (reference)
- Posting Date: Shipment date
- Item Code: Product code (reference)
- Qty: Quantity
- Warehouse: Source warehouse (reference)

**Records**:
1. DN-2026-001 (Seoul Build Corp - Steel Beams)
2. DN-2026-002 (Busan Tech Solutions - Electronic Components)
3. DN-2026-003 (Gwangju Design Studio - Wood + LED)

**Import Order**: 9th (required for invoicing)

---

### 10. 10-sales-invoices.csv

**Purpose**: Create customer invoices

**Fields**:
- Sales Invoice No: Unique identifier
- Customer: Customer name (reference)
- Posting Date: Invoice date
- Due Date: Payment due date
- Item Code: Product code (reference)
- Qty: Quantity
- Rate: Unit price

**Records**:
1. SINV-2026-001 (Seoul Build Corp - Steel Beams)
2. SINV-2026-002 (Busan Tech Solutions - Electronic Components)
3. SINV-2026-003 (Gwangju Design Studio - Wood + LED)

**Import Order**: 10th (required for payment tracking)

---

### 11. 11-payment-entries.csv

**Purpose**: Record payments received from customers

**Fields**:
- Payment Entry No: Unique identifier
- Payment Type: Receive/Pay
- Party Type: Customer/Supplier
- Party: Customer/Supplier name (reference)
- Posting Date: Payment date
- Paid Amount: Payment amount
- Mode of Payment: Payment method

**Records**:
1. PE-2026-001 (Seoul Build Corp - Partial payment 30M KRW)
2. PE-2026-002 (Gwangju Design Studio - Full payment 8.8M KRW)

**Import Order**: 11th (final step in sales cycle)

---

## Import Order (Revised)

### Recommended Sequence

Based on ERPNext Data Import Tool requirements and data dependencies:

**Phase 1: Master Data (Foundation)**
1. **Warehouse** → Storage locations
2. **Customer** → Customer master
3. **Supplier** → Supplier master
4. **Item** → Product catalog

**Phase 2: Transaction Data (References Phase 1)**
5. **Quotation** → Price quotes
6. **Sales Order** → Customer orders
7. **Purchase Order** → Supplier orders

**Phase 3: Operational Data (References Phase 2)**
8. **Stock Entry** → Inventory movements
9. **Delivery Note** → Shipments
10. **Sales Invoice** → Billing
11. **Payment Entry** → Payments

### Why This Order?

1. **Warehouse first**: Required for Item default warehouse
2. **Customer/Supplier next**: Required for all transactions
3. **Item after**: References Warehouse for default location
4. **Quotation before Sales Order**: Sales Order can reference Quotation
5. **Sales Order before Delivery Note**: Delivery Note references Sales Order
6. **Delivery Note before Sales Invoice**: Invoice can reference Delivery Note
7. **Sales Invoice before Payment Entry**: Payment references Invoice
8. **Stock Entry independent**: Can be created anytime after Item/Warehouse

### Differences from Previous Strategy

**Previous Order** (12-demo-data-import-strategy.md):
1. Company
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

**Revised Order**:
1. Warehouse (moved earlier)
2. Customer
3. Supplier
4. Item (moved after Warehouse)
5. Quotation
6. Sales Order
7. Purchase Order
8. Stock Entry (moved earlier)
9. Delivery Note
10. Sales Invoice
11. Payment Entry

**Key Changes**:
- **Warehouse moved to position 1**: Required for Item default warehouse
- **Item moved to position 4**: After Warehouse, before transactions
- **Stock Entry moved to position 8**: After Purchase Order, before Delivery Note
- **UOM removed**: System defaults are sufficient for demo
- **Company removed**: Already exists from Setup Wizard

---

## Data Validation Checklist

### Pre-Import Validation

- [ ] All CSV files have correct headers
- [ ] No empty required fields
- [ ] Customer names match Customer master
- [ ] Supplier names match Supplier master
- [ ] Item codes match Item master
- [ ] Warehouse names match Warehouse master
- [ ] Dates are in YYYY-MM-DD format
- [ ] Quantities are positive numbers
- [ ] Rates are positive numbers

### Reference Integrity Check

- [ ] Quotation customers exist in Customer master
- [ ] Quotation items exist in Item master
- [ ] Sales Order customers exist in Customer master
- [ ] Sales Order items exist in Item master
- [ ] Purchase Order suppliers exist in Supplier master
- [ ] Purchase Order items exist in Item master
- [ ] Stock Entry items exist in Item master
- [ ] Stock Entry warehouses exist in Warehouse master
- [ ] Delivery Note customers exist in Customer master
- [ ] Delivery Note items exist in Item master
- [ ] Delivery Note warehouses exist in Warehouse master
- [ ] Sales Invoice customers exist in Customer master
- [ ] Sales Invoice items exist in Item master
- [ ] Payment Entry parties exist in Customer master

---

## Import Execution Plan

### Step 1: Backup Database

```bash
docker exec frappe_docker-frontend-1 bench --site frontend backup --compress
```

### Step 2: Test Import (Small Scale)

**Test with 1-2 records per DocType**:
1. Import 1 Warehouse
2. Import 1 Customer
3. Import 1 Supplier
4. Import 1 Item
5. Verify all records created correctly

### Step 3: Full Import (If Test Succeeds)

**Import in order**:
1. All Warehouses (2 records)
2. All Customers (5 records)
3. All Suppliers (5 records)
4. All Items (10 records)
5. All Quotations (7 records)
6. All Sales Orders (7 records)
7. All Purchase Orders (3 records)
8. All Stock Entries (5 records)
9. All Delivery Notes (4 records)
10. All Sales Invoices (4 records)
11. All Payment Entries (2 records)

### Step 4: Verification

**Check each DocType**:
1. Count records match expected
2. Spot-check random records
3. Verify linked documents
4. Test basic reports

---

## Known Limitations

### CSV Simplifications

1. **No multi-currency**: All amounts in KRW
2. **No tax handling**: Tax fields omitted for simplicity
3. **No payment terms**: Payment terms omitted
4. **No address details**: Addresses omitted
5. **No contact information**: Contact details omitted

### Data Gaps

1. **No UOM conversion**: Using default UOMs only
2. **No price lists**: Using standard rates
3. **No batch/serial tracking**: Not applicable for demo
4. **No warehouse zones**: Single-level warehouse structure

### ERPNext Version Differences

- CSV format may vary by ERPNext version
- Field names may differ in older/newer versions
- Some fields may be required in specific versions

---

## Next Steps

### Immediate Actions

1. **Review CSV files**: Verify data accuracy
2. **Test import**: Import 1-2 records per DocType
3. **Document issues**: Record any import errors
4. **Adjust CSV**: Fix issues found during testing

### After Successful Test

1. **Full import**: Import all records
2. **Verification**: Check all records imported correctly
3. **AI testing**: Test demo questions with data
4. **Documentation**: Update import log

### If Issues Occur

1. **Check error messages**: Understand failure原因
2. **Adjust CSV format**: Fix field names or values
3. **Check dependencies**: Ensure master data imported first
4. **Consult ERPNext docs**: Verify correct CSV format

---

## Conclusion

**Status**: CSV files prepared, ready for import

**Total Files**: 11
**Total Records**: 54
**Import Order**: Revised and documented
**Next Action**: Small-scale test import

**Key Success Factors**:
- Follow revised import order
- Test with small batch first
- Verify after each step
- Document any issues

---

**Preparation Date**: 2026-05-18
**Status**: Ready for Testing
**Next Step**: Test import with 1-2 records per DocType
