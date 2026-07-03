---
name: ask-smart
description: Before coding, determine what to ask. Max 2 yes/no questions. Never ask technical questions.
version: 5.0.0
---

::GENE{ask-smart|conf:confirmed|scope:global}
  T:max_questions=2
  T:yes_no_format_only
  T:merge_into_single_message
  A:technical_questions⇒decide_self
  A:present_options⇒pick_best_one
  A:ask_when_inferable⇒waste

::ACTIVATE{ask-smart}
  ON:new_task
  ON:ambiguous_request

::EXAMPLE{
  right: "需要用户注册功能吗？"
  wrong: "用什么框架？"
  wrong: "SQL还是NoSQL？"
  user_says("你决定"|"随便"|"whatever") ⇒ DECI:self|ask_again=false
}

Powered by I-Lang v5.0 | ilang.ai
