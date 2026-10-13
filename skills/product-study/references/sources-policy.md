# Sources policy: what counts as public, and what each page is good for

The whole value of a blueprint is that every line can be traced to something
anyone could open. That is what lets the user build on it without worrying, and
what lets you defend it if asked. So the line is drawn by one question:
**could a stranger with a browser and no account read this page today?**
If yes, it is a source. If it took a login, a payment, a tool, or a trick, it is not.

## In scope (tier 1 public material)

| Page type | What to pull from it | Typical confidence |
|---|---|---|
| Official homepage, feature pages | positioning, headline features, platforms, audience | high for stated features |
| Pricing / plans | plan ladder, what each gates, seat vs usage, free limits, enterprise extras | high |
| Docs: concepts / data model / glossary | **object model and nesting** (the single best page for section 2 and 3), terminology | high for structure, medium for fields |
| Docs: getting started / guides | core flows, defaults, onboarding steps | high for flows |
| Changelog / release notes | velocity, what they consider important, recent directions, deprecated areas. One fetch of the changelog page is enough (it usually holds the last 3–6 months); read it by date headings, do not paginate past a second page | high for the facts, guess for direction |
| API / developer docs | API style (REST/GraphQL), auth model, webhooks, SDK languages, rate limits, object schemas | high |
| Integrations page | ecosystem, which systems they treat as first-class | high |
| Security / trust page | auth methods (SSO, SCIM), data residency, compliance claims | high |
| Careers / jobs pages | languages, frameworks, infrastructure named in postings | medium (postings describe teams, not the product) |
| Mobile / desktop pages, app-store listings | platform coverage, offline, notifications, store description | high |
| Customer stories, case studies | who uses it and for what, scale claims | medium |
| Public comparison pages ("X vs Y"), public review sites (G2, Capterra, Product Hunt), tech blogs | complaints, gaps, pricing perception, switching reasons → section 8 | medium for repeated complaints, guess for single voices |
| Public open-source repository: README, docs folder, LICENSE | architecture, modules, data model, stack | high for structure; note the license in section 10 |
| Public roadmap, public status page, terms/privacy | planned areas; data handling that shapes the architecture | medium |

A screenshot or description the **user** gives you of their own account is also
a source (tag it `{medium}` and cite it as what the user described): they are
allowed to look at their own account. It is a source of structure, never of
interface design or copy.

## Out of scope — the tool refuses these and so do you

- Anything behind a login, paywall or invite: account areas, dashboards, admin
  consoles, billing pages, "app." workspaces, private docs.
- Bypassing robots.txt, rate limits, anti-bot measures, or a site's terms; bulk
  scraping of user-generated content.
- Reading minified/obfuscated bundles to recover logic, source maps, network
  captures, API probing with made-up credentials, decompiling, unpacking apps.
  (That is the reverse-engineering path; AutoCode does not take it.)
- Leaked source code, internal documents, beta material, anything the user
  "found" that was not published — even if they paste it into the chat.
- Non-text files from the original (PDF brochures, videos) are not collected by
  the tool; if a PDF whitepaper is clearly public you may read it yourself and
  cite its URL, but prefer the HTML docs.

When a page you need is out of scope, you do not route around it. You note the
gap in the blueprint (lower confidence, a `{guess}` line, or simply a smaller
section) and move on. A thin honest blueprint beats a rich invented one.

## Open-source repositories: study, don't transplant

Reading a public repository is in scope. Copying its code into the user's
product is a separate question decided by the license:

- MIT, Apache-2.0, BSD: code could be reused with attribution, but the
  blueprint still describes structure; the build writes its own code so the
  user's product has one clear provenance.
- GPL, AGPL, SSPL, EUPL and other copyleft: **never** copy code into a product
  under a different license. The architecture may inform the blueprint; section
  10 must say so. The tool prints a NOTE when it detects these.
- No license file: treat as all-rights-reserved; study only.

## Citation format

Sources are numbered in the order they were fetched (`S1`, `S2`, …) and listed
by `blueprint.py sources` with title, URL, fetch date and content hash. In the
body, a bullet ends with `[S3]` or `[S3, S7]`; a table row has a `Sources`
cell with `S3, S7`. Cite the page that actually says it, not the homepage.

## Keeping the record honest

- Dates matter: pricing and features change. The fetch date is recorded next
  to each source; the blueprint header carries the study date.
- If two sources disagree (an old blog post vs. current pricing), prefer the
  official and newer one and say so in the line.
- Never fill a gap with memory of the product. If you "know" a feature but no
  fetched page shows it, either fetch the page that does or tag it `{guess}`.
