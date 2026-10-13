# Product blueprint: TODO product name

<!--
Write the body in the user's language. Keep the numbered headings exactly as
they are (the number is what `blueprint.py check` keys on; the words after it
may be translated). Delete every HTML comment and every TODO before `check`.

Claim lines: in sections 1-8 every bullet and every table row is a claim and
must end with a source tag and a confidence tag, for example
  - Issues can be grouped into cycles of fixed length [S12] {high}
  | Workspace -> Team -> Project -> Issue | S12, S13 | high |
Confidence: {high} = stated verbatim by an official page; {medium} = official
page implies it, or a credible third party states it; {guess} = your inference,
no page says it. {guess} lines may omit the source tag; the others may not.
Chinese tags {高} {中} {推测} are accepted too.
-->

Product: TODO name · Official site: TODO url · Studied on: TODO date · Goal: TODO one sentence on what the user wants to build and for whom

Reading guide: this blueprint describes **structure** (what the product does, how its objects relate, what its users go through), gathered only from public pages listed under Sources. It is a map for building your own product. It does not carry the original's interface, copy, images or brand, and nothing in it is copied from a non-public source.

## 0. Summary

<!-- one paragraph: what it is, who it is for, the one thing it does best, the pricing shape. Plain words, no claims that are not in a source. -->

TODO

## 1. Feature inventory

<!-- Every feature you can establish from the sources. Tier: core = the product is unusable without it; plus = valuable but separable; drop = you would not build it in your version. Group by area if there are more than ~15. -->

| Feature | What it does (one line) | Tier | Sources | Confidence |
|---|---|---|---|---|
| TODO | TODO | core | S1 | high |

## 2. Information architecture

<!-- The nesting of containers and navigation as the user sees it (Workspace > Team > Project > Issue; sidebar sections; top-level pages). Bullets or a short tree in a code block. -->

- TODO [S1] {high}

## 3. Core objects and data model (inferred)

<!-- Entities, their key fields, and relations. Most of this is inference from docs and screenshots, so expect {guess} and {medium}. Mark 1:N / N:M. -->

| Object | Key fields | Relations | Sources | Confidence |
|---|---|---|---|---|
| TODO | TODO | TODO | S1 | medium |

## 4. Key user flows

<!-- 3 to 6 flows that define the product (onboarding, the main create/edit loop, collaboration, reporting). Numbered steps; each flow is one bullet with sub-steps or a short list. -->

- Flow A: TODO -> TODO -> TODO [S1] {medium}

## 5. Technical stack clues

<!-- Only what public pages say: API style (REST/GraphQL), SDKs, webhooks, auth model, platforms, job postings naming languages/frameworks, open-source repo languages. No guessing from bundle names or network traffic: that is out of scope. -->

- TODO [S1] {high}

## 6. Pricing and business model

<!-- Plans, what gates each plan, free tier limits, per-seat vs usage, enterprise extras. -->

| Plan | Price | What it unlocks | Sources | Confidence |
|---|---|---|---|---|
| TODO | TODO | TODO | S1 | high |

## 7. Integrations and ecosystem

<!-- Native integrations, public API, import/export, marketplace, CLI, mobile/desktop apps. -->

- TODO [S1] {high}

## 8. Gaps and differentiation opportunities

<!-- Where public reviews, comparison pages, roadmap or the docs themselves show a hole, a complaint, a market the product does not serve. This is where your product gets its reason to exist. Inference is fine, tag it {guess}. -->

- TODO {guess}

## 9. MVP cut

<!--
The hand-off to the build phase. Only the core tier survives, sized for what an AI agent can build and deploy in one session:
  at most 5 core objects, at most 7 screens, no third-party integrations in v1, one auth method, one deployment target.
Each line is a decision, not a claim: no source tags needed. Keep the user's goal from the header in view; the MVP serves their users, not the original's.
Keep the bold labels starting with the English words Objects / Screens / Acceptance (add a translation after them if you write in another language):
the gate finds them by those words. List items separated by commas or 、; a comma inside parentheses does not split an item.
-->

**Users and the one job:** TODO who uses v1 and the single job it must do

**Objects (<= 5):** TODO

**Screens (<= 7):** TODO

**Dropped from v1 and why:** TODO

**Build order (each step ends in something the user can click):**
1. TODO
2. TODO
3. TODO

**Acceptance (v1 is done when):** TODO three to five checks a non-technical user can perform

## 10. What we will not copy

- Interface look, layout, colors, icons and typography of the original: we design our own.
- Copy, screenshots, images, logo, product and feature names that are trademarks.
- Any code from the original's repositories or bundles. (If a studied repository is copyleft, say so here: its architecture informed this blueprint; none of its code is used.)
- Anything that was not on a public page: no account areas, captures, decompilation or leaked material were used.

## Sources

<!-- Generated by `blueprint.py sources <slug>` from sources.json. Do not edit by hand. -->
