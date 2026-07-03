#!/usr/bin/env bash
# AutoCode pre-deploy secret guard.
# Runs before pushing a beginner's project live. If it finds passwords or keys
# written directly into the code, it BLOCKS the deploy and prints a plain-language
# explanation the AI relays to the user. Zero external deps (bash + python3).
#
# Usage (called by the deploy skills, or manually):
#   bash scripts/scan-secrets.sh [path]     # default path: current dir
# Exit 0 = safe to deploy, 1 = secrets found (block deploy).

set -euo pipefail
TARGET="${1:-.}"
cd "$TARGET"

# Only scan the user's own source. Skip deps, build output, and env files
# (env files are where secrets are SUPPOSED to live, and are gitignored).
scan_files() {
  git ls-files 2>/dev/null | grep -vE '\.(example|template|md)$|node_modules/|\.next/|/dist/|/build/|\.env' \
    || find . -type f \( -name '*.js' -o -name '*.ts' -o -name '*.py' -o -name '*.go' \
         -o -name '*.php' -o -name '*.rb' -o -name '*.env*' -o -name '*.yml' -o -name '*.yaml' \) \
         -not -path '*/node_modules/*' -not -path '*/.next/*' -not -path '*/dist/*' 2>/dev/null
}

check() {
  local f="$1"
  [ -f "$f" ] || return 0
  python3 - "$f" <<'PY'
import sys, re
path = sys.argv[1]
try:
    text = open(path, errors='replace').read()
except Exception:
    sys.exit(0)

ALLOW = ('process.env', 'os.getenv', 'os.environ', 'getEnv(', '${', 'your-', 'your_',
         'example', 'placeholder', 'REPLACE', 'changeme', 'dummy', '<YOUR', 'xxxxx',
         'REDACTED', 'FAKE', 'sample')
def allowed(line): return any(a in line for a in ALLOW)

PATTERNS = {
    'a login token / API key (JWT)':
        re.compile(r'eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}'),
    'a Google API key':      re.compile(r'AIza[0-9A-Za-z_-]{35}'),
    'a Google login secret': re.compile(r'GOCSPX-[0-9A-Za-z_-]{20,}'),
    'a GitHub access token': re.compile(r'\bghp_[A-Za-z0-9]{36}\b'),
    'an OpenAI key':         re.compile(r'\bsk-[A-Za-z0-9_-]{20,}'),
    'a private key file':    re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----'),
    'a database password':   re.compile(r'\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://[^\s:/@]+:[^\s@]{6,}@'),
}

hits = []
for i, line in enumerate(text.splitlines(), 1):
    if allowed(line):
        continue
    for name, rx in PATTERNS.items():
        if rx.search(line):
            if 'database password' in name and re.search(r':(password|pass|user|root|postgres|admin)@', line, re.I):
                continue
            hits.append((i, name))
            break
if hits:
    print(f'FILE::{path}')
    for ln, name in hits:
        print(f'HIT::{ln}::{name}')
    sys.exit(1)
sys.exit(0)
PY
}

FOUND=0
REPORT=""
while IFS= read -r f; do
  [ -z "$f" ] && continue
  if out=$(check "$f"); then :; else
    FOUND=1
    REPORT="${REPORT}${out}\n"
  fi
done < <(scan_files)

if [ "$FOUND" -ne 0 ]; then
  # Machine-readable block for the AI, followed by the plain-language script to relay.
  echo "AUTOCODE_DEPLOY_BLOCKED"
  echo -e "$REPORT"
  cat <<'MSG'
---
SAY THIS TO THE USER (in their language, do not show the technical lines above):

  "等一下，先别上线。我发现代码里直接写了一个密码/密钥。这样一旦上线，
   任何人都能在网上看到它、拿去用。我帮你改成安全的存法（放进一个不会被公开的
   配置里），几秒钟就好，然后我们再上线。"

  (English: "Hold on before we go live. I found a password/key written directly
   into the code. Once it's online, anyone could read and misuse it. Let me move
   it into a safe place that won't be exposed — takes a few seconds — then we ship.")

THEN: move the value to an environment variable / .env (gitignored), replace the
hardcoded value with a reference, and re-run this check before deploying.
---
MSG
  exit 1
fi

echo "AUTOCODE_DEPLOY_SAFE"
exit 0
