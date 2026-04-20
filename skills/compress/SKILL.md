---
name: compress
description: "Compresses internal planning into I-Lang shorthand notation, reducing token usage by 60%+ while preserving meaning. Use when the agent generates internal task plans, reasoning chains, or instruction sequences that the user does not see."
---

# Compress

Converts internal planning and task sequences into I-Lang compressed notation. External user-facing responses remain in natural language.

## I-Lang Syntax Reference

| Element | Format | Example |
|---------|--------|---------|
| Action | `[VERB:TARGET]` | `[BUILD:auth-page]` |
| Parameters | `\|key=value` | `[BUILD:auth-page\|type=login]` |
| Chaining | `=>` | `[BUILD]=>[TEST]=>[SAVE]` |
| Multiple params | comma-separated | `[BUILD:page\|stack=go,db=sqlite]` |

### Core Verbs

- `BUILD` — create a component or feature
- `TEST` — run tests (unit, integration, e2e)
- `CHECK` — validate (security, quality, types)
- `SAVE` — persist changes to disk
- `SPLIT` — decompose into smaller tasks

## Rules

- Internal only — never expose compressed syntax to the user
- Target 60%+ token reduction on internal operations
- Every filler word is removed; every meaning word is kept
- Chain multi-step operations with `=>`

## Example

**User says**: "Help me build a login page"

**Internal** (compressed):
```
[BUILD:auth-page|type=login,stack=go,db=sqlite]=>[TEST:unit]=>[CHECK:security]=>[SAVE]
```

**User sees**: "OK, I'll build the login page for you."
