# Commit Policy

## Message Format

```
<type>: <short description>
```

## Types

| Type | When to Use |
|------|-------------|
| `docs` | Documentation changes |
| `feat` | New features or modules |
| `fix` | Bug fixes |
| `refactor` | Code restructuring without behavior change |
| `test` | Test additions or changes |
| `chore` | Build, config, or tooling changes |
| `infra` | Infrastructure or deployment changes |
| `research` | Research notes or findings |

## Examples

```
docs: add AI provider strategy
feat: add customer management module
fix: correct quotation date format
refactor: simplify inventory query
test: add quotation API tests
chore: update .gitignore
infra: add Docker Compose config
research: compare Korean ERP solutions
```

## Rules

1. One logical change per commit
2. Keep description under 72 characters
3. Use imperative mood ("add", not "added")
4. No period at the end
5. Use English for commit messages (documentation can be in Korean)

## Multi-line Messages (When Needed)

```
feat: add AI quotation draft

- Accept natural language input in Korean
- Generate quotation with customer, items, pricing
- Support review and edit before submission
```
