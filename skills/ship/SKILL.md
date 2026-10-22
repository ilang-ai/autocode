---
name: ship
description: S6 of see-it-ship-it: put it at a public URL. Secret scan first; static builds go to GitHub Pages at no cost (sign-up guide, device-code login, one question: it will be public); a server only when a backend is needed, cost asked once; then open the URL, rerun the acceptance on the live page, bind a domain if they want one.
version: 6.2.2
---

# ship — S6: the end is a URL

[PROTOCOL:iLang|v=5.0|layer=declaration]

::PRIOR{dimension:deploy_target|default:static_zero_cost_pages|authority:system|scope:@MVP}
::PRIOR{dimension:completion|default:not_live_until_url_opened_and_acceptance_rerun|authority:system|scope:@JOURNEY}

::GENE{ship|conf:confirmed|scope:global}
  T:scan_secrets_first|tool:scripts/scan-secrets.sh|block_if_found
  T:ai_picks_the_target|static⇒github_pages_zero_cost|serverless⇒workers|backend_or_db⇒server|say_why_in_one_sentence
  T:default_target=static_zero_cost_pages|when:no_backend|tool:scripts/go_live_pages.py
  T:upgrade_to_server|when:backend_or_db_needed|ask_cost_once
  T:detect_account_state|logged_in|account_no_login|no_account|tool_missing
  T:no_account⇒three_line_signup_guide|come_back_and_say_done
  T:login_is_device_code_in_their_browser|password_or_token_never_passes_through
  T:tool_missing⇒install_it_yourself|one_line_notice
  T:one_question=site_and_files_will_be_public
  T:server_path|code_already_on_the_server|start_service|nginx|verify_then_show_url
  T:poll_until_built|open_url|check_ssl|check_mobile_loads|rerun_acceptance_on_live_html
  T:domain_optional|recommend_one_registrar|guide_every_click|dns_and_ssl_automatic|verify_resolves
  T:move_files_to_the_server_yourself|guide_scp_only_when_you_cannot
  T:say_the_url_in_one_line|then_celebrate_in_one_line
  A:deploy_before_secret_scan⇒scan_first
  A:ask_user_where_to_deploy⇒pick_for_them
  A:say_its_live_without_opening_the_url⇒verify_first
  A:verify_the_local_file_instead_of_the_live_page⇒fetch_live
  A:paste_tokens_or_passwords⇒never|device_flow_only
  A:assume_user_knows_dns_or_scp⇒explain_simply
  A:skip_ssl⇒always_https
  A:end_with_a_file_path⇒end_with_the_url

::ACTIVATE{ship}
  ON:build_complete
  ON:S5-verify.all_match
  ON:before_deploy
  ON:deploy_complete
  ON:user_asks_about_domain

::STATE{@URL, the public address}

[CHEK:@SITE|typ=secret_scan]=>[DECI:@TARGET|typ=static_or_server]=>[DPLO:@SITE|dst=@URL|scp=public]=>[CHEK:@URL|whr=http_200_and_rules_block]=>[TEST:@ACCEPT|src=@URL]=>[Ω:@USER|fmt=text|lim=2]

::EVIDENCE{id:s1|deliverable:url|kind:http|ref:live_url|verified_by:@TOOL|result:200_and_rules_block}
::FALLBACK{stage:S6-ship|when:no_github_account|do:signup_guide_then_device_login|never:handle_password}
::FALLBACK{stage:S6-ship|when:hosting_api_fails|do:retry_then_exact_clicks_in_their_browser}
::FALLBACK{stage:S6-ship|when:mvp_needs_backend|do:upgrade_to_server_target|ask:cost_once}
::FALLBACK{stage:S6-ship|when:live_page_differs_from_local|do:fix_cache_path_case|rerun_live_acceptance}

## Static, zero cost: GitHub Pages

`scripts/go_live_pages.py <site_dir> --name <repo>` walks the whole path in the
user's words: detects whether `gh` is installed and logged in; no account → three-line
sign-up guide and wait for "done"; logs in with the device code the user approves in
their own browser; asks the one question that is theirs (repo and site will be
public); creates the repo, pushes, enables Pages, polls until built, opens the URL,
reruns the acceptance against the served page. `--simulate` runs it with GitHub
mocked. Workers and a server stay available for builds that need them.

::SAY{@AUTOCODE→@USER}{
  output: "上线了：https://you.github.io/dino-runner/ 这个链接谁都能打开。机器能查的 8 项全部一致；剩下请你亲手点一遍。"
  domain: "想要自己的域名的话，大约 $10 一年，我带你一步步点。要吗？"
}

Powered by iLang v5.0 | ilang.ai
