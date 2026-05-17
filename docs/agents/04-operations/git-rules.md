# Git Rules

## Test Phase Policy

During the test phase, **commit everything useful**.

- Documentation changes? Commit.
- Sample data? Commit.
- Configuration updates? Commit.
- Research notes? Commit.

The goal is to capture all work and make it available to the team.

## What NOT to Commit

See [data-security-rules.md](../03-technical/data-security-rules.md) for the full list.

**Quick reference — never commit:**
- `.env` files
- API keys or passwords
- Real customer data
- Server credentials
- Large binary files (use Git LFS if needed)

## Commit Style

Use small, clear commits. One logical change per commit.

**Good:**
```
docs: add customer target description
feat: add quotation API endpoint
fix: correct inventory query filter
```

**Bad:**
```
update everything
WIP
asdfasdf
fix stuff
```

## Branch Strategy (Test Phase)

- `main` — primary branch, always deployable
- Feature branches optional during test phase
- Direct commits to `main` acceptable during test phase

## Remote

- GitHub: `https://github.com/skerishKang/150-erpnext-ai-erp.git`
- Always pull before pushing
- Use `git push -u origin main` for first push
