---
name: security
description: Auto-apply security basics and block deploys that would leak secrets. Never ask the user about security choices — just do it, and run a real secret scan before going live.
version: 5.0.0
---
::PRIOR{completion:assume_incomplete|authority:developer}
::PRIOR{execution:act_when_safe|authority:developer}

::GENE{security|conf:confirmed|scope:global}
  T:auto_apply_no_ask
  T:no_hardcoded_secrets
  T:scan_before_deploy|tool:scripts/scan-secrets.sh
  T:input_validation
  T:parameterized_queries
  T:xss_escape
  T:https_only
  T:rate_limit_login_and_api
  T:error_messages_no_internal_details
  A:ask_user_about_security⇒decide_self
  A:skip_security⇒never
  A:deploy_with_hardcoded_secret⇒block_and_fix

::ACTIVATE{security}
  ON:always
  ON:before_deploy(run scan-secrets.sh; if blocked, fix then re-scan)

# Declaring "no hardcoded secrets" is not enough — it does not catch a real leak.
# Before any deploy, run the scanner. If it returns AUTOCODE_DEPLOY_BLOCKED, do NOT
# deploy: relay the plain-language warning, move the value to an env var, re-scan,
# then ship. This turns security from a promise into an actual gate.

::EXAMPLE{
  user_asks: "安全吗?"
  output: "我做了防攻击处理（防注入、防跨站、密码加密），上线前也扫了一遍确认没有把密钥写死在代码里。正常使用不用担心。"
}

Powered by I-Lang v5.0 | ilang.ai
