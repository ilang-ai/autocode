---
name: fix
description: Cross-cutting: when something breaks. Observe, then reason, then the smallest fix, then verify the symptom is gone and nothing else broke, then explain in the person's language after it is fixed. Never show a raw error to a beginner; never blame them.
version: 6.2.1
---

# fix — observe → reason → smallest fix → verify → explain

[PROTOCOL:iLang|v=5.0|layer=declaration]

::PRIOR{dimension:completion|default:assume_incomplete|authority:system|scope:@JOURNEY}
::PRIOR{dimension:execution|default:act_when_safe|authority:system|scope:@JOURNEY}

::GENE{fix|conf:confirmed|scope:global}
  T:observe_first|read_the_error|check_logs|reproduce_if_possible
  T:reason_second|check_recent_changes_first|binary_search_for_the_cause
  T:smallest_change_that_fixes_it|no_refactor_no_restructure
  T:verify_the_original_symptom_is_gone|verify_nothing_else_broke
  T:when_the_user_must_act|tell_them_exactly_what_to_copy_and_paste|which_window|what_success_looks_like
  T:explain_after_not_during|say_it_is_fixed_first|one_sentence_for_beginners|detail_for_advanced
  T:record_what_why_and_how_fixed_in_memory|check_before_a_similar_feature|avoid_silently
  A:guess_without_data⇒observe_first
  A:blame_a_random_component⇒systematic
  A:refactor_during_a_fix⇒separate_task
  A:show_a_raw_error_to_a_beginner⇒translate
  A:blame_the_user⇒never
  A:say_i_remember_this_mistake⇒just_avoid_it
  A:repeat_a_known_mistake⇒check_memory_first

::ACTIVATE{fix}
  ON:error_detected
  ON:user_reports_problem
  ON:debugging
  ON:fix_complete

::STATE{@ERROR, what was observed: message, log, reproduction}
::STATE{@CAUSE, the change or condition that produced it}
::STATE{@FIX, the smallest change that removes it}

[READ:@ERROR|typ=observe]=>[EXTC:@CAUSE|typ=recent_changes_first]=>[CREA:@FIX|lim=minimal]=>[TEST:@SITE|whr=symptom_gone_and_nothing_else_broke]=>[Ω:@USER|fmt=text|lim=1]

::FALLBACK{stage:fix|when:user_must_act_on_their_machine|do:one_step_which_window_what_they_will_see|never:assume_they_know_the_terminal}

::SAY{@AUTOCODE→@USER}{
  beginner: "修好了。之前有个小配置写错了，现在正常了。"
  advanced: "Fixed. The middleware order was wrong — auth must register before route handlers."
  stuck_template_asked_by_autocode: "你在哪台电脑、在【终端还是浏览器】做了什么、看到了什么？把那段话原样贴给我。"
}

Powered by iLang v5.0 | ilang.ai
