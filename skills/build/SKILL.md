---
name: build
description: S4 of see-it-ship-it: build one feature at a time, simplest stack that works, checkpoint before anything risky, rules kept apart from the look so they can be verified without a browser, learned numbers tagged. Includes first-session environment setup and running where you build.
version: 6.2.0
---

# build — S4: one feature at a time, rules apart from the look

[PROTOCOL:iLang|v=5.0|layer=declaration]

::PRIOR{dimension:completion|default:assume_incomplete|authority:system|scope:@JOURNEY}
::PRIOR{dimension:execution|default:act_when_safe|authority:system|scope:@JOURNEY}

::GENE{build|conf:confirmed|scope:global}
  T:ai_picks_the_stack|simplest_that_works|say_the_choice_in_one_sentence
  T:scaffold_all_files_at_once|then_one_feature_at_a_time|verify_before_next
  T:rules_in_one_pure_block|no_dom|loadable_headless|learned_numbers_tagged_[learned]
  T:single_deployable_unit_when_possible|one_file_static
  T:mobile_first|clean_and_functional|real_content_not_lorem_ipsum
  T:checkpoint_before_risky_change|git_commit_with_human_message|rollback_if_checks_fail
  T:lightweight_first|lazy_load|cache_when_repeated|flag_expensive_operations
  T:run_where_you_build|show_the_live_result_after_each_step
  T:environment_first|one_step_at_a_time|wait_for_each_step|recommend_one_provider_with_link|explain_every_cost
  T:git_as_sync_between_their_devices|guide_beginners
  T:no_secrets_in_source
  T:report_completion_in_the_user's_language
  A:ask_user_the_stack⇒decide_self
  A:over_engineer⇒simplest_solution
  A:parallel_features⇒sequential
  A:skip_verification_between_features⇒reject
  A:rules_tangled_with_rendering⇒separate_first
  A:over_design⇒ship_plain_first
  A:lorem_ipsum⇒real_content
  A:risky_change_without_checkpoint⇒save_first
  A:premature_optimization⇒ship_first
  A:ignore_an_obvious_bottleneck⇒flag
  A:suggest_local_dev_to_a_beginner⇒run_on_the_server
  A:assume_an_environment_exists⇒check_first
  A:several_setup_steps_at_once⇒one_at_a_time
  A:say_choose_a_provider⇒pick_one

::ACTIVATE{build}
  ON:project_start
  ON:plan_approved
  ON:S3-cut.user_said_go
  ON:ui_task_detected
  ON:build_step_complete
  ON:first_session
  ON:no_environment_detected
  ON:before_major_change

::STATE{@SITE, the built deployable unit}

[CREA:@SITE|typ=scaffold_all_files]=>[CREA:@SITE|typ=one_feature|whr=rules_block_separate]=>[TEST:@SITE|src=@LOCAL]=>[Ω:@USER|fmt=text|lim=1]

::EVIDENCE{id:build1|deliverable:site|kind:file|ref:the_build|verified_by:@TOOL|result:runs_and_rules_block_loads_headless}

## First session: environment

Ask what computer they use — the one question. Mac → work locally, push to a server
when ready. Other → a small server (about $6/month at vultr.com), SSH in, install the
agent, build there; one step at a time, wait for "done" after each. Domain ~$10/year
(namecheap.com), SSL free. Say every cost before it happens.

::FACT{key:vps|value:vultr_$6_per_month|conf:4/5}
::FACT{key:domain|value:namecheap_$10_per_year|conf:4/5}
::FACT{key:ssl|value:free_letsencrypt_or_cloudflare|conf:5/5}

::SAY{@AUTOCODE→@USER}{
  output: "我用 Go + SQLite 做，轻量、快、免费。开始搭框架了。"
  output: "登录功能做好了。用户可以注册、登录、登出。✅ 3/5 完成，还剩 2 步。"
}

Powered by iLang v5.0 | ilang.ai
