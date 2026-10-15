#!/bin/bash
# AutoCode v5.0: I-Lang v5.0 + memory

# I-Lang v5.0 Protocol (one line, not 31 verbs)
echo "## [AutoCode] I-Lang v5.0 Active"
echo "88 verbs. 13 Greek aliases. Spec: ilang.ai"
echo ""

# Global user preferences
GLOBAL_PREFS="$HOME/.autocode/user.md"
if [ -f "$GLOBAL_PREFS" ]; then
  echo "## [AutoCode] User Preferences Loaded"
  cat "$GLOBAL_PREFS"
  echo ""
fi

# Project memory
MEMORY_FILE=".autocode/memory.md"
if [ -f "$MEMORY_FILE" ]; then
  echo "## [AutoCode] Project Memory Loaded"
  cat "$MEMORY_FILE"
  echo "---"
  echo "Continue where you left off."
else
  cat << 'WELCOME'
## [AutoCode] Welcome

AutoCode active. 11 skills, 7 stages. iLang v5.0 judgment.

Tell the user in THEIR language:
1. "I'm AutoCode. Tell me what you want to build. I handle everything — code, deploy, domain. You just say yes or no."
2. "When we're done, you'll get a real URL anyone can visit."
3. Ask: "What computer are you using? Mac or other?"
WELCOME
fi
