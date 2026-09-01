#!/usr/bin/env python3
"""Download EN PDFs for all papers in data/papers.json into papers/<id>_<slug>/."""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
manifest = json.loads((ROOT / "data" / "papers.json").read_text())

failed = []
for p in manifest["papers"]:
    d = ROOT / "papers" / f"{p['id']}_{p['slug']}"
    d.mkdir(parents=True, exist_ok=True)
    out = d / f"{p['id']}.pdf"
    if out.exists() and out.stat().st_size > 50_000:
        print(f"skip  {p['slug']} (exists)")
        continue
    url = f"https://arxiv.org/pdf/{p['id']}"
    rc = subprocess.run(
        ["curl", "-sSL", "--retry", "3", "--retry-delay", "5", "-o", str(out), url],
        timeout=180).returncode
    ok = rc == 0 and out.exists() and out.stat().st_size > 50_000
    # arXiv returns tiny HTML error pages on failure; treat those as failures
    if ok and out.read_bytes()[:5] != b"%PDF-":
        ok = False
    print(f"{'ok    ' if ok else 'FAIL  '}{p['slug']:24s} {out.stat().st_size if out.exists() else 0:>9} bytes")
    if not ok:
        failed.append(p["id"])
        out.unlink(missing_ok=True)
    time.sleep(3)

print(f"\ndone: {len(manifest['papers']) - len(failed)}/{len(manifest['papers'])} ok; failed: {failed}")
sys.exit(1 if failed else 0)
