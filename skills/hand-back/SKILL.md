---
name: hand-back
description: S7 of see-it-ship-it: what the person hears. Progress lines while building (percentage, fraction, three lines max), one-line celebration of real milestones credited to them, a session summary of done / fixed / next, and the fixed hand-back at the end: URL, table result, what to try by hand, what was learned versus decided.
version: 6.2.1
---

# hand-back — S7: what the person hears, from the first step to the URL

[PROTOCOL:iLang|v=5.0|layer=declaration]

::GENE{hand-back|conf:confirmed|scope:global}
  T:progress_line_per_step|percentage_plus_fraction|just_done_now_remaining|max_3_lines
  T:focus_on_done_not_missing
  T:real_milestones_only|one_line_one_emoji|credit_to_the_user|save_milestone_to_memory
  T:session_summary=done|fixed|next|delta|positive_tone
  T:final_shape=url+machine_table_result+actions_to_try_by_hand+learned_vs_own
  T:one_line_invitation|change_anything_by_saying_it|url_stays
  T:always_in_the_user's_language
  A:verbose_report⇒concise
  A:over_celebrate⇒never
  A:say_i_did_this⇒say_your_product
  A:treat_a_minor_step_as_a_milestone⇒only_significant
  A:end_a_session_without_a_summary⇒always_summarize
  A:end_with_a_file_path⇒end_with_the_url
  A:list_what_was_not_built⇒only_if_asked

::ACTIVATE{hand-back}
  ON:build_step_complete
  ON:milestone_reached
  ON:session_end
  ON:S6-ship.live_verified

::EVIDENCE{id:h1|deliverable:hand_back|kind:text|ref:final_message|verified_by:@USER|result:they_opened_the_url}
::STATUS{@MVP|state:committed|evidence:h1|by:@USER|authority:user}

::SAY{@AUTOCODE→@USER}{
  progress: "✅ 40% (5/12) — 登录做好了，下一步是支付。"
  milestone: "🎉 你的网站第一次上线了。"
  summary: "今天：做了 5 个功能，修了 1 个问题。明天：支付和上线。进度 60%。"
  final: "上线了：https://… 机器验收 8/8 一致。请你亲手点：开始、空格跳、拖滑块、撞了重开。学来的：起始速度 6、每次 +0.001、上限 13；画面和滑块是我们自己设计的。想改什么直接说，网址不变。"
}

Powered by iLang v5.0 | ilang.ai
