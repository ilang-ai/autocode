---
name: plan-estimate
description: Give realistic time and cost estimates for each step. Explain in human terms.
version: 5.0.0
---

::GENE{plan-estimate|conf:confirmed|scope:global}
  T:estimate_in_minutes_not_hours
  T:include_total_at_end
  T:explain_cost_in_human_currency
  A:underestimate⇒add_20_percent_buffer
  A:say_depends⇒give_concrete_number

::ACTIVATE{plan-estimate}
  ON:plan_created

Powered by I-Lang v5.0 | ilang.ai
