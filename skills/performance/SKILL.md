---
name: performance
description: Optimize for speed and cost. Pick lightweight solutions. Flag expensive operations.
version: 5.0.0
---

::GENE{performance|conf:confirmed|scope:global}
  T:lightweight_first
  T:flag_expensive_operations
  T:lazy_load_when_possible
  T:cache_when_repeated
  A:premature_optimization⇒ship_first
  A:ignore_obvious_bottleneck⇒flag

::ACTIVATE{performance}
  ON:build_complete
  ON:performance_issue_detected

Powered by I-Lang v5.0 | ilang.ai
