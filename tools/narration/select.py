"""Choose the take for each beat from narration/qa.json and write narration/selection.json.

Scoring: a take with dropped content words or clipping loses; among the rest, the pace closest to 160 wpm wins;
ties keep the earlier attempt. Prints every beat where attempt 02 replaced 01 so the choice is visible.

  python tools/narration/select.py
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / "narration/qa.json"
OUT = ROOT / "narration/selection.json"
TARGET = 160.0

def score(r: dict) -> tuple:
    bad = any(f.startswith("content words") or f == "clipping" or f.startswith("extra content") for f in r["flags"])
    return (1 if bad else 0, abs(r["wpm"] - TARGET), r["attempt"])

def main() -> int:
    qa = json.loads(QA.read_text(encoding="utf-8"))
    by_beat: dict[str, list[dict]] = {}
    for key, r in qa.items(): by_beat.setdefault(r["beat"], []).append(r)
    sel, changed = {}, []
    for beat, takes in sorted(by_beat.items()):
        best = min(takes, key=score)
        sel[beat] = {"attempt": best["attempt"], "wpm": best["wpm"], "flags": best["flags"], "candidates": [(t["attempt"], t["wpm"], "; ".join(t["flags"])) for t in sorted(takes, key=lambda t: t["attempt"])]}
        if best["attempt"] != 1: changed.append((beat, best["attempt"], best["wpm"], [t["wpm"] for t in takes if t["attempt"] == 1]))
    OUT.write_text(json.dumps(sel, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(sel)} beats selected; {len(changed)} use a later attempt")
    for c in changed: print("  ", c)
    still = {b: s["flags"] for b, s in sel.items() if s["flags"]}
    print(f"{len(still)} selected takes still carry flags"); [print("  ", b, "|", "; ".join(f)) for b, f in list(still.items())[:20]]
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
