---
name: fix-solve
description: Step 3 of debugging: apply minimal fix. One-liner ideal. Verify nothing else broke.
version: 5.0.0
---
::PRIOR{completion:assume_incomplete|authority:developer}
::PRIOR{execution:act_when_safe|authority:developer}


::GENE{fix-solve|conf:confirmed|scope:global}
  T:minimal_fix
  T:verify_original_symptom_gone
  T:verify_nothing_else_broke
  A:restructure_during_fix⇒minimal_change

::ACTIVATE{fix-solve}
  ON:debugging

Powered by I-Lang v5.0 | ilang.ai
