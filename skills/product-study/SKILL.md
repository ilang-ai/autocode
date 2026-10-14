---
name: product-study
description: Study an existing product from its public pages and turn it into an evidence-backed blueprint plus an MVP cut that AutoCode can build and ship. Use this whenever the user wants something "like X", "similar to X", "my own version of X", "a clone of X", names a competitor they admire, or pastes a product URL and asks to build it — even when they never say "research" or "analyze". Public sources only (official site, docs, pricing, changelog, public repos, app-store listings, public reviews); no logins, captures, decompiling, or copying of code, copy, images or brand.
version: 6.1.0
---

::GENE{product-study|conf:confirmed|scope:global}
  T:learn_structure_not_skin
  T:public_pages_only
  T:every_claim_has_source_and_confidence
  T:end_with_an_mvp_the_agent_can_build_in_one_session
  T:classify_target_first|saas_with_public_pages|open_source_project|app_with_store_listing|undocumented
  T:acceptance_line=user_does+should_see+machine_checks
  T:mvp_names_learned_rules_vs_own_decisions
  T:verify_runs_before_go_live_and_again_on_the_live_url|tool:scripts/acceptance_run.py
  A:reverse_engineer_or_capture⇒refuse_and_continue_with_public_pages
  A:report_tests_passed⇒show_expected_vs_actual_table
  A:copy_ui_copy_images_brand_code⇒describe_structure_instead
  A:present_blueprint_as_the_product⇒it_is_a_map_the_build_comes_next

::ACTIVATE{product-study}
  ON:user_names_a_product_to_imitate
  ON:user_pastes_product_url_with_build_intent

# Product study

The user saw a product and wants their own. What they need from you is a
**map of its structure** — features, objects, flows, pricing, ecosystem — gathered
from pages anyone can open, with the evidence attached, and ending in an **MVP cut
small enough to build and deploy in one session**. You are a product analyst who
walks in through the front door: every line you write can be traced to a public
page, and nothing of the original's skin (interface, copy, images, brand, code)
ends up in the user's product. That is what makes the result safe to ship and
the user's own.

## Step 0 — Frame it in one sentence

Before any fetching, tell the user what will happen, in their language:

> I'll study *X* from its public pages, give you a blueprint of how it's built,
> and cut an MVP we can ship today. We learn the structure and design our own look.

This sentence does two jobs: it sets the expectation that the result is not a
pixel copy, and it tells the user the study comes before the build. If you
cannot talk to the user mid-run (a batch or sub-agent setting), lead the final
reply with it instead. Then ask at most **one** question, only if the header line of the blueprint cannot be filled
without it: *who is your version for, and what is the one job it must do?* If
the user already said it, do not ask.

## Step 1 — Collect public pages

Scripts live in this skill's `scripts/` folder; both are Python 3.8+ standard
library and refuse out-of-scope URLs on their own. They write under
`.autocode/study/<slug>/` **relative to the directory you run them from**, so run
them from the user's project root and call them by their absolute path (or pass
`--root <dir>`). `$SKILL` below stands for this skill's folder.

```bash
python3 $SKILL/scripts/fetch_public.py discover https://example.com          # candidate pages, nothing saved
python3 $SKILL/scripts/fetch_public.py fetch <slug> <url> [<url> ...]        # save text + outline as S1.txt, S2.txt ...
python3 $SKILL/scripts/fetch_public.py links <slug> S3 [--grep docs]       # same-site links seen on S3, no network
python3 $SKILL/scripts/fetch_public.py github <slug> owner/repo             # public repo README + license (if open source)
python3 $SKILL/scripts/fetch_public.py list <slug>
```

Decide first which kind of thing the user pointed at; the sources differ:

- **SaaS with public pages** (Linear, Notion…): pricing, docs, changelog, help center, reviews. The live app itself is usually a login wall; the docs are the map.
- **Open-source project** (a small game, a CLI, a template): the public repo *is* the map. `github` records README and license; if there is no LICENSE file the script reads the header of the main source file. Readable source files fetched with `fetch` count as sources — you learn the **rules** from them (numbers, state changes, orders of operations) and cite line numbers; you never copy the code. Copyleft (GPL/AGPL): architecture only.
- **App with a store listing**: the store page and help center; no binaries.
- **Undocumented**: say so, write a thin blueprint with low confidence, and let the MVP carry more `{guess}`.

Run `discover` on the homepage **and** on the docs root; docs navigation is
often rendered by JavaScript, so if no concepts / data-model page shows up, try
the usual slugs directly (`/docs/concepts`, `/docs/conceptual-model`,
`/docs/data-model`, `/docs/glossary`, `/docs/getting-started`): a 404 is refused
harmlessly and recorded. Once a docs page is fetched, `links <slug> S3` walks its
navigation without another round trip.

Pick 8–20 pages, in this order of value: pricing · docs "concepts" / data-model /
getting-started pages · feature pages · changelog (last 6–12 months) · API /
developer docs · integrations · security · careers (stack clues) · mobile/desktop ·
customer stories · comparison pages. App-store listings and public review sites
(G2, Capterra, Product Hunt) count as public pages too. Read
`references/sources-policy.md` for what each page type is good for and the exact
line between public and not.

What the tool refuses, you do not work around: login/account/billing paths,
robots-disallowed paths, pages that redirect to a sign-in, non-text files.
A page that comes back with almost no text was rendered by JavaScript — look for
the same content in the docs subdomain or a help center, or go without it. If
the product is genuinely undocumented in public, say so and build the blueprint
from what exists, with lower confidence tags; a thin honest blueprint beats a
rich invented one.

## Step 2 — Read before you write

Open each `sources/S*.txt`. The header gives the URL, title and an outline of
headings — the outline alone often reveals the information architecture. Keep
notes as `claim → S-id` while reading, because every line in the blueprint must
carry its sources and you will not want to hunt for them afterwards.

## Step 3 — Write the blueprint

```bash
python3 $SKILL/scripts/blueprint.py init <slug> --product "Name" --site https://... --goal "who it is for and the one job"
```

`examples/linear/` holds a finished blueprint and MVP hand-off produced with this
skill; skim it once to calibrate density and tone (about 200 lines, every claim
tagged, section 9 a real build order).

Fill `.autocode/study/<slug>/blueprint.md` section by section. The template's
HTML comments explain each section; delete them as you go. Rules that the gate
enforces, and why:

- **Every claim in sections 1–8 ends with `[S…]` and a confidence tag.**
  `{high}` = an official page states it; `{medium}` = an official page implies it
  or a credible third party states it; `{guess}` = your inference. `{guess}` may
  omit the source; the other two may not. The user will make decisions on this
  document — they must see which lines are facts and which are your reading.
- **Say it in your own words.** A sentence lifted from the original's site is a
  copyright problem and a signal that you did not understand it. The gate
  compares claim lines against the fetched text.
- **No images, logos, screenshots or code blocks longer than 15 lines.** Structure
  is text. If a repository was studied, name its license in section 10; copyleft
  code never moves into a differently licensed product.
- **Write in the user's language; keep the numbered headings and the bold labels
  in section 9.** The gate keys on the section number and on `**Objects`,
  `**Screens`, `**Acceptance` and `## Sources`; add a translation after the
  English word (`**Objects 对象 (<= 5):**`) rather than replacing it. Items in
  the Objects/Screens lines are separated by commas or 、; a comma inside
  parentheses is fine.
- A translated sentence is still a copy. When the blueprint and the sources are
  in different languages the gate says so and cannot catch it — the rule holds
  anyway.
- Keep it under ~250 lines. A blueprint is read before a build, not instead of one.

Section 8 (gaps) is where the user's product gets its reason to exist: what the
reviews complain about, what the pricing gates off, who the product ignores.
Section 9 (MVP cut) is a set of decisions, not claims: the core tier only, sized
to **≤ 5 objects, ≤ 7 screens, no third-party integrations in v1, one auth method,
one deployment target**, with a build order where every step ends in something
the user can click, and acceptance checks a non-technical user can perform.
Those limits are what let an AI agent finish and ship in one sitting; a bigger
v1 is where projects die.

Section 9 has two lines the gate reads strictly. **Acceptance** is three to five
lines, each in three parts separated by `->` (or `→`): *what the user does* -> *what
they should see* -> *what a machine can check* (write `manual` when nothing can). The
third part is what `acceptance_run.py` will verify, so write it as a number or a state,
not an adjective. **Learned vs own** names the rules and numbers taken from the target
(each with its `[S#]`) and says in one line that everything else — look, layout,
copy, defaults — is our own design. Both lines travel into `mvp.md` and into the code.

## Step 4 — Gate it

```bash
python3 $SKILL/scripts/blueprint.py check <slug>      # one line per check; exit 1 on any FAIL
python3 $SKILL/scripts/blueprint.py sources <slug>    # refresh the Sources section after fetching more
```

`check` also prints notes that are not failures: sources fetched but never cited
(thin navigation-only pages — drop them from your reading or cite them), and a
language-mismatch note. Read the notes; they are the reviewer's eyes.

Fix every FAIL and run again. Do not hand the user a blueprint that fails the
gate, and do not edit the Sources section by hand.

## Step 5 — MVP hand-off

```bash
python3 $SKILL/scripts/blueprint.py mvp <slug>        # writes mvp.md from sections 9 + 10, plus a Verify note
```

Show the user, in their language: the one-paragraph summary (section 0), the
MVP cut, and one line inviting them to cross out or add. Two decisions are theirs:
the scope of v1 and anything that costs money. Everything else you decide.
When they say go, `mvp.md` is the input to the build (plan-breakdown →
build-scaffold → build-feature → Step 6 → go-live in AutoCode); the rest of the
blueprint is context, not scope.

While building, keep the rules (numbers, formulas, state changes) in one block that
loads without a browser — in a web build, `<script id="rules">` with no DOM access —
and tag the learned ones `[learned]` in the code. Everything else is rendering and is
yours. This is what makes Step 6 possible.

## Step 6 — Verify (before go-live, and again on the live URL)

Next to the build, write a checks file, `acceptance.js` (node) or `acceptance.py`,
that loads the rules block, performs the machine part of every acceptance line, and
prints one JSON row per check: `{"id","check","expected","actual","ok"}`. Then:

```bash
python3 $SKILL/scripts/acceptance_run.py <site_dir>                 # local build: table of check / expected / actual / match
python3 $SKILL/scripts/acceptance_run.py <site_dir> --url <live>    # after go-live: the same table against the served page
```

The runner exits non-zero on any mismatch; go-live refuses to continue on that. The
table is what the user sees — never "tests passed". The acceptance lines a machine
cannot check are handed to the user as actions to perform, in the hand-back. Worked
run: `examples/dino/` (8/8 match, including a floating-point boundary the original
has); the whole journey is written down in `methodology/see-it-ship-it.md`.

## Boundaries

If the user asks for any of these, say in one sentence what you will do instead
and keep going — no lecture, no stopping the task:

- decompiling, unpacking, de-obfuscating, reading minified bundles for logic,
  network capture, API probing → *"I work from the public pages; here is what
  they tell us."*
- logging in to their account of the original and walking the UI → *"I don't use
  account areas; if you describe what you see there, I can use that as a {medium}
  source."* (A screenshot they took of their own account is fine to read for
  structure; it is not a source of copy or design.)
- copying the interface, copy, images, logo, names, or code → *"We take the
  structure and design our own; here is the list of what we won't copy."*
- leaked source, internal docs, beta material → not used, even if pasted in.

`references/boundaries.md` has the full list with the reasoning, for the cases
in between.

## Output

```
.autocode/study/<slug>/
  sources.json        what was fetched, what was refused and why, hashes, dates
  sources/S1.txt …    text + outline of each public page
  blueprint.md        sections 0–10 + generated Sources
  mvp.md              hand-off to the build
```

## Example

User: *我想做一个像 Linear 那样的工单工具，给我们十个人的团队用。*

1. Reply in Chinese with the framing sentence; the goal is already stated, no question.
2. `discover https://linear.app` and `discover https://linear.app/docs` → fetch
   pricing, docs concepts, start guide, teams/projects/cycles/issues docs,
   changelog, developers, integrations, security, careers, mobile (≈15 pages;
   the finished run is in `examples/linear/`).
3. Read; init with `--goal "十人软件团队的轻量工单工具，键盘优先"`; fill sections 0–10
   in Chinese with `[S…] {高|中|推测}` tags; section 9 keeps Team / Project / Issue /
   Cycle / Comment, seven screens, no GitHub/Slack integration in v1.
4. `check` passes → `mvp` → show summary + MVP → user says go → build.

Powered by I-Lang v5.0 | ilang.ai
