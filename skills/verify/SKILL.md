---
name: verify
description: S5 of see-it-ship-it: prove it works before saying so. Silent quality checks after every feature, a full review of every file before save and deploy, and the acceptance table (check / expected / actual / match) run on the local build and again on the live URL. Never 'tests passed'.
version: 6.2.1
---

# verify — S5: show the table, never say "tests passed"

[PROTOCOL:iLang|v=5.0|layer=declaration]

::PRIOR{dimension:completion|default:assume_incomplete|authority:system|scope:@JOURNEY}
::PRIOR{dimension:completion|default:not_live_until_url_opened_and_acceptance_rerun|authority:system|scope:@JOURNEY}

::GENE{verify|conf:confirmed|scope:global}
  T:check_after_every_feature|silently|fix_minor_things_without_saying
  T:run_tests_if_a_framework_exists|never_claim_a_run_that_did_not_happen
  T:full_review_before_save_and_deploy|every_file|logic|edges|security|hardcoded_values
  T:acceptance_runner_is_a_fixed_build_output|tool:product-study/scripts/acceptance_run.py
  T:checks_file_next_to_the_build|acceptance.js|acceptance.py|one_json_row_per_check
  T:table=check|expected|actual|match|readable_by_a_non_technical_person
  T:user_checks_listed_as_actions_to_perform|not_as_tests_passed
  T:fix_then_rerun_until_all_match|before_ship
  T:rerun_on_the_live_url_after_ship
  T:human_readable_commit_messages
  A:report_tests_passed⇒show_expected_vs_actual
  A:claim_tests_passed_without_running⇒reject
  A:announce_that_you_are_checking⇒silent
  A:say_tests_failed_to_the_user⇒fix_first_then_report
  A:partial_review⇒full_review
  A:skip_review_on_save⇒never
  A:no_headless_browser⇒rules_block_checks_in_node_or_python

::ACTIVATE{verify}
  ON:feature_complete
  ON:before_save
  ON:before_deploy
  ON:S4-build.step_complete
  ON:S6-ship.url_live
  ON:session_end

::STATE{@ACCEPT, the acceptance table}

[TEST:@ACCEPT|src=@LOCAL]=>[CHEK:@ACCEPT|whr=all_match]=>[Ω:@USER|fmt=text|typ=table]

::EVIDENCE{id:v1|deliverable:site|kind:test_output|ref:acceptance_table_local|verified_by:@TOOL|result:all_match}
::EVIDENCE{id:v2|deliverable:site|kind:test_output|ref:acceptance_table_live|verified_by:@TOOL|result:all_match}
::STATUS{@MVP|state:claimed_complete|evidence:v1|by:@AGENT|authority:proposal}
::STATUS{@MVP|state:verified|evidence:v2|by:@TOOL|authority:runtime}

```bash
python3 skills/product-study/scripts/acceptance_run.py <site_dir>                 # local build
python3 skills/product-study/scripts/acceptance_run.py <site_dir> --url <live>    # after ship
```

::SAY{@AUTOCODE→@USER}{
  table: "5  自动加速 10000 次更新后速度   13.001   13.001   ✓ 一致 … 8/8 一致"
  to_user: "机器能查的 8 项全部一致。剩下请你亲手点：开始、空格跳、拖滑块、撞了重开。"
}

Powered by iLang v5.0 | ilang.ai
