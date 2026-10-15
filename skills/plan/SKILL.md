---
name: plan
description: S3 of see-it-ship-it: cut the work into steps that each end in something the person can click, with minutes not hours, core before polish, risks and costs flagged, free alternatives first. Internal planning is written in iLang; the person never sees it.
version: 6.2.0
---

# plan — S3: cut it into steps they can see

[PROTOCOL:iLang|v=5.0|layer=declaration]

::PRIOR{dimension:completion|default:assume_incomplete|authority:system|scope:@JOURNEY}
::PRIOR{dimension:execution|default:act_when_safe|authority:system|scope:@JOURNEY}
::PRIOR{dimension:v1_scope|default:core_tier_only_one_session|authority:system|scope:@MVP}

::GENE{plan|conf:confirmed|scope:global}
  T:steps=5-15|each=2-5min|dependency_order_first
  T:each_step_ends_in_something_clickable_or_testable
  T:estimate_in_minutes|total_at_end|buffer=+20%
  T:core_function_first|revenue_before_aesthetics|mvp_then_iterate
  T:flag_third_party_dependencies_rate_limits_and_cost_traps|free_alternatives_first
  T:large_task⇒phases_with_milestones_and_a_shipping_date
  T:compare_with_a_mid_level_programmer_only_at_milestones|time_and_money|realistic
  T:internal_plans_in_ilang|user_never_sees_compressed_form
  T:mvp_from_product_study_is_the_plan|when:S2_ran
  A:step_over_5_minutes⇒split_further
  A:monolithic_spec⇒reject
  A:say_it_depends⇒give_a_concrete_number
  A:all_features_at_once⇒sequential
  A:polish_before_core⇒reject
  A:roadmap_without_a_shipping_date⇒add_one
  A:exaggerate_the_comparison⇒realistic
  A:filler_words_in_internal_notes⇒remove
  A:meaning_loss_in_compression⇒reject

::ACTIVATE{plan}
  ON:task_scope>30min
  ON:plan_created
  ON:multiple_features_requested
  ON:external_api_detected
  ON:S2-study.gate_passed

::STATE{@STEPS, ordered steps, each with minutes and what the person will see}

[PLAN:@STEPS|whr=dependency_order|lim=15]=>[CHEK:@STEPS|whr=each_clickable]=>[Ω:@USER|fmt=text|lim=5]

::EVIDENCE{id:plan1|deliverable:steps|kind:text|ref:the_plan_shown|verified_by:@USER|result:they_said_go}

::SAY{@AUTOCODE→@USER}{
  output: "1. 搭框架（2分钟）2. 注册页面（5分钟）3. 登录功能（5分钟）4. 上线（5分钟）… 大概 20 分钟搞定。"
  risk: "这个功能要用 X 的接口，免费额度每天 100 次，够我们用；超了我会先说。"
}

Powered by iLang v5.0 | ilang.ai
