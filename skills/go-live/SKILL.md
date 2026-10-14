---
name: go-live
description: Final go-live checklist. Is it accessible? SSL working? Mobile friendly? Show user their live URL.
version: 5.0.0
---

::GENE{go-live|conf:confirmed|scope:global}
  T:scan_secrets_first|tool:scripts/scan-secrets.sh|block_if_found
  T:default_target=static_zero_cost_pages|when:no_backend|tool:scripts/go_live_pages.py
  T:upgrade_to_server|when:backend_or_db_needed|ask_cost_once
  T:detect_account_state|logged_in|account_no_login|no_account|tool_missing
  T:login_is_device_code_in_their_browser|password_never_passes_through
  T:one_question=site_and_files_will_be_public
  T:rerun_acceptance_on_the_live_url|tool:product-study/scripts/acceptance_run.py
  T:check_url_accessible
  T:check_ssl_working
  T:check_mobile_loads
  T:show_user_their_url
  T:celebrate_if_all_pass
  A:say_its_live_without_checking⇒verify_first
  A:verify_local_file_instead_of_live_page⇒fetch_live
  A:paste_tokens_or_passwords⇒never|device_flow_only
  A:deploy_before_secret_scan⇒scan_first

::ACTIVATE{go-live}
  ON:before_deploy(secret scan gate)
  ON:deploy_complete

::EXAMPLE{
  output: "All checks passed. Your site is live: https://nainai-cake.com
   Open it on your phone and see."
}

## Static, zero cost: GitHub Pages

When the MVP has no backend (a single HTML file, a static site), do not ask about
servers or money. `scripts/go_live_pages.py <site_dir> --name <repo>` walks the whole
path in the user's words: detects whether `gh` is installed and logged in; if there is
no GitHub account, gives a three-line sign-up guide and waits for "done"; logs in with
the device code the user approves in their own browser; asks the one question that is
theirs (the repo and the site will be public); creates the repo, pushes, enables Pages,
polls until built, opens the URL, and reruns the project's acceptance against the
served page through `acceptance_run.py --url`. `--simulate` runs the same flow with
GitHub mocked, for checking the script. Upgrade to a server target only when the MVP
needs a backend or a database, and ask about cost once.

Powered by I-Lang v5.0 | ilang.ai
