---
applyTo: "**"
---

# Git Commit Conventions

## Format

```text
type(scope): subject
```

## Types

Allowed types: `build`, `ci`, `tools`, `docs`, `feat`, `feature`, `fix`, `perf`, `refactor`, `design`, `style`, `test`, `release`.

Prefer conventional `feat` for new features. `feature` remains an accepted fallback/alias. Never use `chore`; use `tools` or `build`.

## Scopes

Scopes match the normalized folder names in `__PROJECT_NAME__.code-workspace`:

`__SCOPES__`

Scope is required for code/package changes. `build`, `ci`, `docs`, `tools`, and `style` may omit it when a change is truly cross-cutting. An explicit scope must always be valid.

## Subject

Use lowercase imperative mood with no period at the end. Generic ticket prefixes are allowed when relevant: `ISSUE-123`, `TICKET-123`, or `#123`.

## Examples

```text
feat(__VALID_SCOPE__): add repository setup
fix(__VALID_SCOPE__): preserve request ordering
test(__VALID_SCOPE__): cover transaction rollback
docs: update local setup
ci: cache package-manager downloads
```
