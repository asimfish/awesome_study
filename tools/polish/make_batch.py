#!/usr/bin/env python3
"""Generate a codex prompt for a batch of paper dirs. Usage: make_batch.py <batch_name> <dir1> <dir2> ..."""
import sys
from pathlib import Path
root = Path(__file__).resolve().parents[2]
name, dirs = sys.argv[1], sys.argv[2:]
tmpl = (root / 'tools/polish/PROMPT_TEMPLATE.md').read_text(encoding='utf-8')
files = '\n'.join(f'- papers/{d}/README.md  （原文 PDF: papers/{d}/{d.split("_",1)[0]}.pdf）' for d in dirs)
log = f'reports/polish_log_{name}.md'
out = root / f'tools/polish/prompt_{name}.md'
out.write_text(tmpl.replace('{FILES}', files).replace('{LOG}', log), encoding='utf-8')
(root / log).write_text(f'# 打磨日志 · batch {name}\n\n', encoding='utf-8')
print(out)
