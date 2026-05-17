# Test Policy

## Initial Phase

Initial testing is **broad and exploratory**.

- We are validating product-market fit, not production hardening
- Tests should cover happy paths first
- Edge cases can be addressed later

## Testing Priorities (In Order)

1. **Manual testing:** Does the feature work when a human uses it?
2. **API testing:** Do the API endpoints return correct data?
3. **Unit tests:** Do individual functions work correctly?
4. **Integration tests:** Do modules work together?

## Test Data

- Use sample/fake data only
- Never use real customer data in tests
- Sample data should reflect Korean business scenarios:
  - Korean company names (주식회사 한빛, 삼성전자, etc.)
  - Korean item names (CNC 부품, 전자부품, etc.)
  - Korean currency (KRW)
  - Korean address formats

## Test Commands (Future)

```bash
# Run all tests
pytest

# Run specific module tests
pytest tests/test_quotation.py

# Run with coverage
pytest --cov=app
```

## What We Test First

| Priority | Module | Why |
|----------|--------|-----|
| 1 | Customer management | Foundation for all other modules |
| 2 | Quotation management | Core AI feature (AI quotation draft) |
| 3 | Inventory status | High-frequency query use case |
| 4 | CEO daily briefing | Key AI differentiator |

## Quality Bar

- Features must work in Korean
- AI responses must be in Korean
- Error messages must be in Korean
- Performance: API responses under 2 seconds
- AI responses: under 5 seconds for queries, under 10 seconds for generation
