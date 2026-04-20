---
name: plan-breakdown
description: "Breaks large tasks into 5-15 concrete, dependency-ordered steps of 2-5 minutes each. Use when starting any medium or large build to give the user a clear, trackable plan."
---

# Task Breakdown

Decomposes large or medium tasks into small, concrete, dependency-ordered steps. Each step produces a visible or testable deliverable.

## Workflow

1. **Analyze** the task scope and identify components
2. **Break** into 5-15 concrete steps, each taking 2-5 minutes
3. **Order** steps by dependency (database before auth, framework before pages)
4. **Present** the plan to the user in plain language with time estimates

## Rules

- Each step must have a clear, visible deliverable
- No step should take longer than 5 minutes — break it down further if it does
- Steps are ordered by dependency, not complexity
- Present in plain language the user can follow

## Example

User asks to build a user authentication system:

```
Here's the plan:
1. Set up the project framework (2 min)
2. Create the database schema for users (3 min)
3. Build the registration page (5 min)
4. Build the login functionality (5 min)
5. Test everything end-to-end (3 min)
Total: about 18 minutes.
```

Note: database (step 2) comes before registration (step 3) because registration depends on the user table existing.
