---
name: fix-reason
description: Step 2 of debugging: reason about root cause based on observed symptoms.
version: 5.0.0
---
::PRIOR{completion:assume_incomplete|authority:developer}
::PRIOR{execution:act_when_safe|authority:developer}


::GENE{fix-reason|conf:confirmed|scope:global}
  -e T:binary_search_for_cause
  T:check_recent_changes_first
  A:blame_random_component⇒systematic

::ACTIVATE{fix-reason}
  ON:debugging

Powered by I-Lang v5.0 | ilang.ai
