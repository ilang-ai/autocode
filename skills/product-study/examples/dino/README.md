# Example: dino runner — the first end-to-end run of see-it-ship-it

Target: the Chrome offline dinosaur game, studied from a public open-source copy
(`wayou/t-rex-runner`). The user's ask, in a non-technical person's words: "a dinosaur
game like that one, but I can set the speed myself."

What is here, in the order the methodology produces it (methodology/see-it-ship-it.md):

| Stage | File | Evidence |
|---|---|---|
| S2 study | `blueprint.md`, `sources.json` | 28/28 gate checks; every rule number cites S2 with a line number |
| S3 cut | `mvp.md` | 5 objects, 2 screens, 7 build steps, 5 three-part acceptance lines, learned-vs-own |
| S4 build | `site/index.html` | one file; rules in `<script id="rules">`, learned numbers tagged `[learned]`; look is our own |
| S5 verify | `site/acceptance.js` | `python3 ../../scripts/acceptance_run.py site` → 8/8 match, including the 13.001 boundary |
| S6 ship | `skills/go-live/scripts/go_live_pages.py site --name dino-runner --simulate` | GitHub Pages flow, verification rerun on the served page |

Learned from the target (rules only, no code): start speed 6, +0.001 per update while
below 13, gravity 0.6, jump velocity 12, wait for the first key, keep the best score on
restart. Everything else — look, shapes, slider 2–18, 60 updates/s, 1.5 s clear time,
spacing, copy — is our own design.

Reproduce the verification:

```bash
python3 skills/product-study/scripts/blueprint.py check dino --root skills/product-study/examples
python3 skills/product-study/scripts/acceptance_run.py skills/product-study/examples/dino/site
```
