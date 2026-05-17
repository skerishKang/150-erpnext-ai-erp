# Vibe Coding Rules

## What Is Vibe Coding?

Vibe coding is how we write code in this repository — fast, focused, and shipping-oriented.

## Core Rules

### 1. Ship Working Code

- Write code that works, not code that is perfect
- Optimize for speed of delivery
- Refactor later if needed

### 2. Korean-First

- All user-facing text in Korean
- All business logic reflects Korean business practices
- Error messages in Korean
- Comments in English (for code), Korean (for business logic)

### 3. ERP Context

- Every feature must serve an ERP workflow
- Do not build generic tools — build ERP features
- Data must flow between modules (connected ERP, not siloed tools)

### 4. AI as Feature, Not Product

- AI enhances ERP workflows
- AI does not replace ERP fundamentals
- Always provide a non-AI fallback path
- AI suggestions are suggestions, not commands

### 5. Practical Over Perfect

- Use ERPNext's built-in features when possible
- Custom code only when ERPNext doesn't provide what we need
- Prefer configuration over code
- Prefer proven patterns over novel approaches

## Code Style

- Python: Follow PEP 8
- JavaScript: Follow Frappe conventions
- Naming: snake_case for Python, camelCase for JS
- Documentation: Docstrings for public functions only

## When to Ask

Ask before:
- Changing product scope
- Adding features not in MVP
- Changing technical architecture
- Making decisions that affect customer experience
