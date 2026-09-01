#!/bin/bash
# Translate all translate:true papers via SuperTranslate (layout-preserving EN->ZH).
# Usage: bash tools/translate_batch.sh [slug ...]   # no args = all pending
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ST_SKILL="$HOME/Code/super_translate/skills/paper-translate"
LOG="$ROOT/translate.log"

# key from local PDFMathTranslate config (never printed)
export DEEPSEEK_API_KEY="$(python3 -c "
import json
cfg = json.load(open('$HOME/.config/PDFMathTranslate/config.json'))
print([t['envs']['DEEPSEEK_API_KEY'] for t in cfg['translators'] if t['name']=='deepseek'][0])")"

TARGETS="$(python3 -c "
import json, sys
m = json.load(open('$ROOT/data/papers.json'))
want = set(sys.argv[1:])
for p in m['papers']:
    if p['translate'] and (not want or p['slug'] in want):
        print(p['id'] + '_' + p['slug'] + '/' + p['id'])
" "$@")"

echo "=== batch start $(date '+%F %T') ===" | tee -a "$LOG"
fail=0
for t in $TARGETS; do
  dir="$ROOT/papers/$(dirname "$t")"
  id="$(basename "$t")"
  src="$dir/$id.pdf"; dst="$dir/$id.zh.pdf"
  if [ -s "$dst" ]; then echo "[skip] $t (zh exists)" | tee -a "$LOG"; continue; fi
  echo "[start] $t $(date '+%T')" | tee -a "$LOG"
  if bash "$ST_SKILL/scripts/translate_one.sh" "$src" "$dst" >> "$LOG" 2>&1; then
    echo "[ok]   $t $(date '+%T')" | tee -a "$LOG"
  else
    echo "[FAIL] $t $(date '+%T')" | tee -a "$LOG"; fail=$((fail+1))
  fi
done
echo "=== batch done $(date '+%F %T'), failures: $fail ===" | tee -a "$LOG"
exit "$fail"
