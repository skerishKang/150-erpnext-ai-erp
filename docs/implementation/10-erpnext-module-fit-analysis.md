# 10 - ERPNext Module Fit Analysis for Padiem AI ERP MVP

## Date: 2026-05-18

## Summary

Analysis of ERPNext default modules to determine suitability for Padiem AI ERP MVP targeting Korean SMEs.

## ERPNext Default Module List (20 Modules)

Based on ERPNext Desk after Setup Wizard completion:

| # | Module | Icon | Description |
|---|--------|------|-------------|
| 1 | Organization | 🏢 | Company structure and management |
| 2 | Invoicing | 📄 | Invoice creation and management |
| 3 | Payments | 💳 | Payment processing and tracking |
| 4 | Financial Reports | 📊 | Balance Sheet, P&L, etc. |
| 5 | Accounts Setup | ⚙️ | Chart of Accounts configuration |
| 6 | Taxes | 🧾 | Tax templates and configuration |
| 7 | Banking | 🏦 | Bank reconciliation and management |
| 8 | Budget | 📈 | Budget planning and tracking |
| 9 | Share Management | 📉 | Shareholder and equity management |
| 10 | Subscription | 🔄 | Recurring billing management |
| 11 | Accounting | 📒 | Core accounting module |
| 12 | Assets | 🏗️ | Fixed asset management |
| 13 | Buying | 🛒 | Purchase management |
| 14 | Manufacturing | 🏭 | Production and BOM management |
| 15 | Projects | 📋 | Project and task management |
| 16 | Quality | ✅ | Quality inspection and control |
| 17 | Selling | 💰 | Sales management |
| 18 | Stock | 📦 | Inventory management |
| 19 | Subcontracting | 🔧 | Subcontracting workflows |
| 20 | ERPNext Settings | ⚙️ | Global configuration |

## Module Classification

### 1ST PRIORITY - Use for MVP (6 Modules)

#### 1. Selling Module ✅

**Status**: PRIMARY - Core MVP Module

**Why needed**:
- Customer management (Customer DocType)
- Quotation creation and tracking
- Sales Order processing
- Sales Invoice generation
- Delivery Note management
- Sales analytics and reporting

**Key DocTypes**:
- Customer
- Quotation
- Sales Order
- Sales Invoice
- Delivery Note
- Sales Partner

**Fit for Korean SME**: ★★★★★
- Essential for any business
- Supports Korean business practices
- Multi-currency support (KRW)

---

#### 2. Buying Module ✅

**Status**: PRIMARY - Core MVP Module

**Why needed**:
- Supplier management (Supplier DocType)
- Purchase Order creation
- Purchase Invoice processing
- Purchase Receipt tracking
- Supplier analytics

**Key DocTypes**:
- Supplier
- Purchase Order
- Purchase Invoice
- Purchase Receipt
- Request for Quotation

**Fit for Korean SME**: ★★★★★
- Essential for supply chain management
- Supports Korean supplier relationships
- Integration with Selling module

---

#### 3. Stock Module ✅

**Status**: PRIMARY - Core MVP Module

**Why needed**:
- Item/product management
- Warehouse management
- Stock Entry (in/out/transfer)
- Inventory tracking and valuation
- Stock balance reporting

**Key DocTypes**:
- Item
- Warehouse
- Stock Entry
- Stock Ledger Entry
- Stock Balance Report

**Fit for Korean SME**: ★★★★★
- Critical for inventory management
- Supports multiple warehouses
- Real-time stock tracking

---

#### 4. Invoicing Module ✅

**Status**: PRIMARY - Core MVP Module

**Why needed**:
- Unified invoice management
- Integration with Selling/Buying
- Payment tracking
- Invoice reporting

**Key DocTypes**:
- Sales Invoice (from Selling)
- Purchase Invoice (from Buying)
- Payment Entry

**Fit for Korean SME**: ★★★★★
- Central to business operations
- Supports Korean tax requirements
- Multi-currency invoicing

---

#### 5. Payments Module ✅

**Status**: PRIMARY - Core MVP Module

**Why needed**:
- Payment processing
- Payment reconciliation
- Payment analytics
- Bank integration preparation

**Key DocTypes**:
- Payment Entry
- Payment Order
- Payment Gateway Account

**Fit for Korean SME**: ★★★★☆
- Essential for cash flow management
- Supports multiple payment methods
- Integration with banking

---

#### 6. Accounts Setup Module ✅

**Status**: SUPPORTING - Configuration Module

**Why needed**:
- Chart of Accounts setup
- Account configuration for Korean accounting
- Fiscal year management
- Account groups and categories

**Key DocTypes**:
- Account
- Account Group
- Fiscal Year
- Company

**Fit for Korean SME**: ★★★★☆
- Required for basic accounting setup
- Supports Korean chart of accounts
- Foundation for financial reporting

---

### 2ND PRIORITY - Hold for Later (6 Modules)

#### 7. Financial Reports Module ⏸️

**Status**: HOLD - Phase 2 Candidate

**Why hold**:
- Advanced reporting not needed for MVP
- Requires complete accounting setup
- Can use basic reports initially

**Future use**:
- Balance Sheet
- Profit & Loss Statement
- Cash Flow Statement
- Trial Balance

**When to activate**: After basic accounting is stable

---

#### 8. Accounting Module ⏸️

**Status**: HOLD - Phase 2 Candidate

**Why hold**:
- Full accounting is complex
- MVP can use simplified invoicing
- Requires Chart of Accounts customization

**Future use**:
- Journal Entries
- General Ledger
- Account reconciliation
- Advanced financial reporting

**When to activate**: When SME needs full double-entry accounting

---

#### 9. Banking Module ⏸️

**Status**: HOLD - Phase 2 Candidate

**Why hold**:
- Bank reconciliation is advanced
- MVP can track payments manually
- Requires bank integration setup

**Future use**:
- Bank Account management
- Bank Statement import
- Bank Reconciliation
- Payment matching

**When to activate**: When bank integration is required

---

#### 10. Projects Module ⏸️

**Status**: HOLD - Phase 2 Candidate

**Why hold**:
- Not core to basic SME operations
- Adds complexity to MVP
- Can be added later for service businesses

**Future use**:
- Project management
- Task tracking
- Time tracking
- Project costing

**When to activate**: For service-based SMEs

---

#### 11. Budget Module ⏸️

**Status**: HOLD - Phase 3 Candidate

**Why hold**:
- Advanced financial planning
- Not essential for MVP
- Requires complete accounting

**Future use**:
- Budget planning
- Budget vs actual analysis
- Cost center management

**When to activate**: When financial planning is needed

---

#### 12. Manufacturing Module ⏸️

**Status**: HOLD - Phase 2 Candidate

**Why hold**:
- Complex manufacturing workflows
- Not all SMEs need manufacturing
- Can be added for production businesses

**Future use**:
- Bill of Materials (BOM)
- Production planning
- Work order management
- Manufacturing analytics

**When to activate**: For manufacturing SMEs

---

### 3RD PRIORITY - Exclude from MVP (8 Modules)

#### 13. Taxes Module ❌

**Status**: EXCLUDE - Too Complex for MVP

**Why exclude**:
- Korean tax system is specific
- Requires professional tax knowledge
- MVP can use simple tax handling

**Alternative**:
- Use basic tax fields in invoices
- Manual tax calculation initially
- Add tax module when compliance is needed

---

#### 14. Share Management Module ❌

**Status**: EXCLUDE - Not Relevant for SMEs

**Why exclude**:
- Shareholder management is corporate-level
- Most SMEs don't need this
- Adds unnecessary complexity

**Alternative**:
- Use Company settings for basic ownership
- Add only if business requires

---

#### 15. Subscription Module ❌

**Status**: EXCLUDE - Niche Use Case

**Why exclude**:
- Recurring billing is specialized
- Not all SMEs need subscriptions
- Can be added later if needed

**Alternative**:
- Manual invoice creation initially
- Add subscription module for SaaS businesses

---

#### 16. Assets Module ❌

**Status**: EXCLUDE - Advanced Feature

**Why exclude**:
- Fixed asset management is advanced
- Requires depreciation calculations
- Not essential for MVP

**Alternative**:
- Track assets as items initially
- Add asset module for proper asset management

---

#### 17. Quality Module ❌

**Status**: EXCLUDE - Specialized Use Case

**Why exclude**:
- Quality inspection is manufacturing-focused
- Not relevant for most SMEs
- Adds unnecessary workflows

**Alternative**:
- Manual quality checks initially
- Add for manufacturing businesses

---

#### 18. Subcontracting Module ❌

**Status**: EXCLUDE - Specialized Workflow

**Why exclude**:
- Subcontracting is specific to certain industries
- Not core SME functionality
- Adds complexity

**Alternative**:
- Use purchase orders for subcontractors
- Add only if subcontracting is core business

---

#### 19. Organization Module ❌

**Status**: EXCLUDE - Configuration Only

**Why exclude**:
- Used for initial setup only
- Not a functional module
- Company settings in ERPNext Settings

**Alternative**:
- Use Company DocType directly
- No separate module needed

---

#### 20. ERPNext Settings Module ❌

**Status**: EXCLUDE - Configuration Only

**Why exclude**:
- Configuration module, not functional
- Used for system setup
- Not user-facing

**Alternative**:
- Access settings as needed
- No separate module activation

---

## Recommended DocType Priority for MVP

### Tier 1 - Essential DocTypes (Must Have)

| DocType | Module | Purpose | Priority |
|---------|--------|---------|----------|
| Customer | Selling | Customer master data | ★★★★★ |
| Supplier | Buying | Supplier master data | ★★★★★ |
| Item | Stock | Product/service catalog | ★★★★★ |
| Quotation | Selling | Price quotes to customers | ★★★★★ |
| Sales Order | Selling | Customer orders | ★★★★★ |
| Purchase Order | Buying | Supplier orders | ★★★★★ |
| Sales Invoice | Selling/Invoicing | Customer billing | ★★★★★ |
| Purchase Invoice | Buying/Invoicing | Supplier billing | ★★★★★ |
| Delivery Note | Stock/Selling | Shipment tracking | ★★★★☆ |
| Stock Entry | Stock | Inventory movements | ★★★★☆ |
| Payment Entry | Payments | Payment recording | ★★★★☆ |

### Tier 2 - Important DocTypes (Should Have)

| DocType | Module | Purpose | Priority |
|---------|--------|---------|----------|
| Warehouse | Stock | Storage locations | ★★★★☆ |
| UOM | Stock | Units of measure | ★★★☆☆ |
| Price List | Selling/Buying | Pricing management | ★★★☆☆ |
| Currency | Setup | Multi-currency support | ★★★☆☆ |
| Company | Setup | Company information | ★★★☆☆ |
| Fiscal Year | Setup | Accounting periods | ★★★☆☆ |

### Tier 3 - Optional DocTypes (Nice to Have)

| DocType | Module | Purpose | Priority |
|---------|--------|---------|----------|
| Sales Partner | Selling | Partner/referral tracking | ★★☆☆☆ |
| Request for Quotation | Buying | RFQ management | ★★☆☆☆ |
| Material Request | Stock | Internal requests | ★★☆☆☆ |
| Batch | Stock | Batch tracking | ★★☆☆☆ |
| Serial No | Stock | Serial number tracking | ★★☆☆☆ |

## Korean SME Specific Considerations

### Language Support

- ERPNext supports Korean language
- Korean translations available
- UI can be switched to Korean

### Currency

- KRW (Korean Won) supported
- Multi-currency for international trade
- Exchange rate management

### Accounting

- Korean Chart of Accounts can be configured
- Tax handling needs customization
- Fiscal year alignment (calendar year)

### Business Practices

- Korean business relationship management
- Multi-level approval workflows
- Korean address format support

## Next Steps for Implementation

### Phase 1 - Core Setup (Week 1-2)

1. Configure Company with Korean settings
2. Set up Chart of Accounts for Korean SME
3. Create Item groups and categories
4. Configure UOM (Units of Measure)
5. Set up Price Lists (KRW)

### Phase 2 - Master Data (Week 2-3)

1. Create sample Customer records
2. Create sample Supplier records
3. Create sample Item records
4. Configure Warehouse structure

### Phase 3 - Transaction Testing (Week 3-4)

1. Test Quotation workflow
2. Test Sales Order workflow
3. Test Purchase Order workflow
4. Test Invoice generation
5. Test Payment recording

### Phase 4 - AI Integration Prep (Week 4+)

1. Identify AI integration points
2. Design natural language interface
3. Plan AI-assisted data entry
4. Design smart reporting

## Conclusion

Padiem AI ERP MVP should focus on 6 core modules:
1. **Selling** - Customer and sales management
2. **Buying** - Supplier and purchase management
3. **Stock** - Inventory management
4. **Invoicing** - Billing management
5. **Payments** - Payment processing
6. **Accounts Setup** - Basic accounting configuration

This provides a solid foundation for Korean SMEs while avoiding complexity. Advanced modules can be added in later phases based on specific business needs.

---

**Analysis Date**: 2026-05-18
**Next Review**: After Phase 1 implementation
