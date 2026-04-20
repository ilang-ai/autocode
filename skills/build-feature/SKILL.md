---
name: build-feature
description: "Builds one feature at a time sequentially, running quality checks and verification after each. Use when implementing features from a development plan to ensure each is complete before starting the next."
---

# Build Feature

Implements features one at a time. Each feature goes through a complete build-check-verify cycle before the next begins.

## Workflow

1. **Write code** for a single feature
2. **Run auto-quality** checks silently (activates auto-quality skill)
3. **Verify** the feature works — run the relevant test or manual check
4. **Report** to the user: state what was built and what it does
5. **Show progress**: "Step 3 done, 2 remaining"
6. **Move** to the next feature in the plan

## Rules

- One feature at a time — never work on two simultaneously
- Each feature must function independently before integrating
- If a feature would take more than one build cycle, decompose it first (activates plan-breakdown skill)
- Always tell the user what was completed and what remains

## Example

Building a login system from a 3-step plan:

```
Step 1: Build registration
  -> write code -> run auto-quality -> verify signup works
  -> "Registration is done. Users can create accounts."
  -> "Step 1 complete, 2 remaining."

Step 2: Build login
  -> write code -> run auto-quality -> verify credentials work
  -> "Login is done. Users can sign in."
  -> "Step 2 complete, 1 remaining."

Step 3: Build logout
  -> write code -> run auto-quality -> verify session ends
  -> "Logout is done. All 3 steps complete."
```
