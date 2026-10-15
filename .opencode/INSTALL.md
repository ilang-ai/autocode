# Installing AutoCode for OpenCode

## Installation (recommended)

```bash
git clone https://github.com/ilang-ai/autocode.git ~/.config/opencode/autocode
python3 ~/.config/opencode/autocode/autocode.py setup --client opencode
```

`setup` shows what it will change, asks once, then copies the 11 skills into the
agent's skills folder and adds one managed block to its instructions file. Check
with `python3 ~/.config/opencode/autocode/autocode.py doctor`; remove with `uninstall`.

## Manual installation

```bash
git clone https://github.com/ilang-ai/autocode.git ~/.config/opencode/autocode
```

Add to your project `.opencode/AGENTS.md`:

```markdown
## AutoCode

Before writing any code, read all skill files in ~/.config/opencode/autocode/skills/ and follow their instructions automatically. Each skill activates based on context — never skip the see skill (intent, level, scope) before coding, and judge before anything that costs money or cannot be undone.
```

## Verify

```bash
ls ~/.config/opencode/autocode/skills/
```

11 skills loaded. Describe what you want to build.

## Update

```bash
cd ~/.config/opencode/autocode && git pull
```
