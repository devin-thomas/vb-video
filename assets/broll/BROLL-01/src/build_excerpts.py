"""Write BROLL-01 evidence/source-excerpts.md from exact source line ranges.

Usage (from the repository root): python assets/broll/BROLL-01/src/build_excerpts.py .
"""
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
out = root / "assets/broll/BROLL-01/evidence/source-excerpts.md"
out.parent.mkdir(parents=True, exist_ok=True)


def lines(rel, lo, hi):
    text = (root / rel).read_text(encoding="utf-8").splitlines()
    return "\n".join(text[lo - 1:hi])


def sha(rel):
    return hashlib.sha256((root / rel).read_bytes()).hexdigest()


ranges = [
    ("sources/ASSET_PLAN.md", 109, 122, "ticket anchor; line 117 is the BROLL-01 row"),
    ("sources/SCRIPT.md", 799, 805, "ticket anchor"),
    ("sources/ASSET_PLAN.md", 81, 107, "R14 register anchor"),
    ("sources/SCRIPT.md", 749, 763, "R14 register anchor"),
    ("docs/EDITORIAL_REGISTER.md", 145, 153, "R14 register entry"),
]

parts = [
    "# BROLL-01 source excerpts",
    "",
    "Exact, unmodified line ranges copied programmatically from the repository files below "
    "(script recorded in qa.md). Nothing inside the fenced blocks is authored by this ticket. "
    "External web evidence (asset pages, license pages) is recorded separately in "
    "evidence/candidates.json and exports/candidates.md.",
    "",
]
for rel in sorted({r[0] for r in ranges}):
    parts.append(f"- `{rel}` sha256 `{sha(rel)}`")
parts.append("")
for rel, lo, hi, why in ranges:
    parts += [f"## {rel}:{lo}-{hi} ({why})", "", "~~~~text", lines(rel, lo, hi), "~~~~", ""]

out.write_text("\n".join(parts), encoding="utf-8", newline="\n")
print(out, out.stat().st_size)
