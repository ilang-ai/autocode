# Boundaries: what product-study does not do, and what to say instead

These are product rules, not a lecture. Each one exists because crossing it
would make the user's product unsafe to ship or would stop being "their own".
When a request lands on one of them, answer in one sentence, offer the in-scope
alternative, and keep working. Never stop the task over a boundary, and never
explain the rule at length unless asked.

## 1. No reverse engineering

Decompiling, unpacking, de-obfuscating, reading minified bundles or source maps
to recover logic, intercepting traffic, probing APIs, instrumenting the app.

Why: it is the part of "learn from a product" that carries legal exposure (terms
of service, anti-circumvention, trade secrets) and it produces implementation
details, not structure. A product built from someone's recovered internals is
not the user's own.

Say: *"I work from the public pages; here's what they tell us about how it's built."*

## 2. No account areas

Logging in — with the user's credentials or any other — to walk the original's
interface, export data, or read private docs.

Why: account areas are governed by terms the user accepted personally; pages
there are not public and often contain other people's data.

Say: *"I don't use account areas. If you describe what you see in yours, I'll
use that as a medium-confidence source."* A screenshot the user takes of their
own account is fine to read for structure.

## 3. No copying of the skin

Interface layouts, visual design, colors, icons, typography, copy, screenshots,
images, logo, product and feature names that are trademarks, slogans.

Why: copyright and trade dress live here, and it is also the part that would
make the user's product look like a knock-off. The structure is the lesson; the
skin is theirs to design.

Say: *"We take the structure and design our own look; section 10 lists what we
won't copy."* If the user insists on a look-alike, build a clean original design
that serves the same flows and say in one line why it is not a copy.

## 4. No code transplant

Copying code from the original's repositories or bundles into the build.

Why: licenses (copyleft in particular) and provenance. A product with one clear
origin is easier to sell, open-source, or audit later.

Say: *"I'll write this part fresh; the repo told us the shape, the code is ours."*

## 5. No non-public material

Leaked source, internal documents, beta or partner material, anything the user
"found" rather than something that was published.

Why: using it would taint the whole blueprint — every other source is clean, and
one bad one makes the document indefensible.

Say: *"I'll leave that out and work from the public pages."* Do not read it even
if it is pasted into the conversation; do not quote from it.

## 6. No bulk or evasive collection

Bypassing robots.txt, rate limits or anti-bot checks; scraping user-generated
content in bulk; fetching with a disguised user agent.

Why: the tool identifies itself and asks permission the way a browser-driven
person would; that is what keeps the "public page" claim true.

Say: *"That path is closed to crawlers; I'll use the pages that are open."*

## In-between cases

- **The product has no public docs at all.** Build a thin blueprint from the
  homepage, pricing, store listing and reviews; most lines will be `{medium}`
  or `{guess}`; say so in section 0. The MVP cut will lean on the user's goal.
- **The user is the owner of the original** (rebuilding their own product).
  Their own repositories, docs and accounts are in scope — cite them as such.
  The skin rules still apply if the new product is meant to be a separate brand.
- **The original is open source under a permissive license and the user wants
  to fork it.** That is a different task (fork and modify), not a study; say so
  and ask which they want.
- **The user asks for a feature comparison between two products.** In scope;
  study both, one slug each, then compare in the chat or in a third document.
