# Installing AutoCode for Codex

## Installation (recommended)

```bash
git clone https://github.com/ilang-ai/autocode.git ~/.codex/autocode
python3 ~/.codex/autocode/autocode.py setup --client codex
```

`setup` shows what it will change, asks once, then copies the 49 skills into the
agent's skills folder and adds one managed block to its instructions file. Check
with `python3 ~/.codex/autocode/autocode.py doctor`; remove with `uninstall`.

## Manual installation

```bash
git clone https://github.com/ilang-ai/autocode.git ~/.codex/autocode
```

Add to `~/.codex/AGENTS.md`:

```markdown
## AutoCode

Before writing any code, read all skill files in ~/.codex/autocode/skills/ and follow their instructions automatically. Each skill activates based on context — never skip the clarify-scope skill before coding.
```

## Verify

```bash
ls ~/.codex/autocode/skills/
```

49 skills loaded. Describe what you want to build.

## Update

```bash
cd ~/.codex/autocode && git pull
```
