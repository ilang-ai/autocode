---
name: ask-smart
description: "Asks at most two non-technical clarification questions before starting a task. Use when beginning any new feature, fix, or project to determine user intent without overwhelming them with technical details."
---

# Smart Questions

Determines what to ask the user before writing code or planning. Limits questions to essentials and avoids technical jargon.

## Workflow

1. **Evaluate** whether the task requires clarification
2. **Ask at most 2 questions** — combine into a single message
3. **Never ask technical questions** the user cannot answer
4. **Decide automatically** when the answer is inferable from context

## Rules

- Maximum 2 questions per task — no exceptions
- Only ask if the answer materially changes the outcome
- Non-technical questions only: "Do users need signup?" is fine; "What framework?" is never appropriate
- If the answer can be inferred from context, decide without asking
- When the user says "you decide" or "whatever," make the choice and do not ask again

## Examples

**Good question**: "Should users be able to sign up, or is this internal-only?"
**Bad question**: "Should I use React or Vue for the frontend?"

**When context is sufficient**: User says "build a login page" and the project already uses Next.js — choose Next.js, do not ask about the framework.
