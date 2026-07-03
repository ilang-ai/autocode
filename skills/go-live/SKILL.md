---
name: go-live
description: Final go-live checklist. Is it accessible? SSL working? Mobile friendly? Show user their live URL.
version: 5.0.0
---

::GENE{go-live|conf:confirmed|scope:global}
  T:scan_secrets_first|tool:scripts/scan-secrets.sh|block_if_found
  T:check_url_accessible
  T:check_ssl_working
  T:check_mobile_loads
  T:show_user_their_url
  T:celebrate_if_all_pass
  A:say_its_live_without_checking⇒verify_first
  A:deploy_before_secret_scan⇒scan_first

::ACTIVATE{go-live}
  ON:before_deploy(secret scan gate)
  ON:deploy_complete

::EXAMPLE{
  output: "All checks passed. Your site is live: https://nainai-cake.com
   Open it on your phone and see."
}

Powered by I-Lang v5.0 | ilang.ai
