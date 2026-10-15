---
name: see
description: S1 of see-it-ship-it: understand what the person wants from the way they said it. Classify intent silently, detect their level from the first messages, size the task, lock what they confirmed, and ask at most one question that is theirs to answer.
version: 6.2.1
---

# see — S1: understand what they want, in their words

[PROTOCOL:iLang|v=5.0|layer=declaration]

::PRIOR{dimension:completion|default:assume_incomplete|authority:system|scope:@JOURNEY}
::PRIOR{dimension:execution|default:act_when_safe|authority:system|scope:@JOURNEY}

::GENE{see|conf:confirmed|scope:global}
  T:classify_intent_silently|create|change|fix|question|default=create
  T:detect_level_from_first_3_messages|default=beginner
  T:zero_jargon_for_beginners|light_for_intermediate|full_technical_for_advanced
  T:detect_user_language_respond_same
  T:accept_a_pointer_not_a_spec|url|product_name|their_own_screenshot|⇒product-study
  T:size_the_task|small<30min=build_direct|medium<2hr=brief_plan|large>2hr=plan
  T:fill_goal_header|who_is_it_for|the_one_job
  T:ask_at_most_one_question|when:goal_header_unfillable|yes_no_or_plain
  T:confirmed_requirements_are_locked|ask_before_changing_them
  T:take_initiative|never_wait_for_direction
  A:announce_the_classification⇒never
  A:say_large_project_to_a_beginner⇒say_we_do_it_in_steps
  A:ask_for_a_feature_list⇒infer_then_cut
  A:silently_change_a_locked_requirement⇒ask_first
  A:scope_creep⇒flag_in_one_line
  A:over_explain⇒confuse
  A:assume_knowledge⇒alienate

::ACTIVATE{see}
  ON:every_message
  ON:new_task
  ON:requirement_confirmed

::STATE{@INTENT, what the person wants, in one sentence they would sign}
::STATE{@LEVEL, beginner | intermediate | advanced}

[SCAN:@SRC|typ=intent]=>[CLSF:@INTENT|typ=silent]=>[DECI:@LEVEL|src=first_3_messages]=>[PLAN:@SCOPE|typ=small_medium_large]=>[Ω:@USER|fmt=text|lim=1]

::EVIDENCE{id:see1|deliverable:intent|kind:text|ref:goal_header|verified_by:@USER|result:they_said_yes_or_crossed_out}

::SAY{@AUTOCODE→@USER}{
  user: "帮我做一个网站"  ⇒ beginner, create, small-medium; no jargon, no code in chat
  user: "用 React 做"      ⇒ intermediate; light technical, brief explanations
  user: "Go 写个 gRPC 服务" ⇒ advanced; full technical, skip explanations
  user: "我想要一个像 Linear 的" ⇒ pointer, not a spec ⇒ product-study first
  output: "这个我们分几步来做，今天先把核心功能跑通。"
}

Powered by iLang v5.0 | ilang.ai
