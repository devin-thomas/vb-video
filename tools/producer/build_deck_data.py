"""OPS-03 / OPS-04 data build.

Reads manifest.json, every state.json, delivery.json and evidence/claim-checks.json, plus War/SCRIPT.md and
docs/EDITORIAL_REGISTER.md, and writes:
  scratchpad/deck/deck-data.json            -> data the review deck renders from
  review/editorial-review.json              -> every review question in the project (OPS-03 ledger, question view)
  assets/ops/OPS-03/exports/decision-ledger.json -> per ticket: gates, status, approver, reason, questions
"""
from __future__ import annotations
import json, re, os
from pathlib import Path
from collections import OrderedDict

ROOT = Path(r"C:\dev\youtube\vb-video-checkout-2")
OUT = Path(__file__).parent
LF = "\n"

manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
rows = manifest["tickets"]

# ---- script sections and cue lines
script = (ROOT / "War/SCRIPT.md").read_text(encoding="utf-8").split("\n")
sections = {}
for i, line in enumerate(script, 1):
    m = re.match(r"^## SECTION (\d+): (.+)$", line.strip())
    if m:
        sections[int(m.group(1))] = {"n": int(m.group(1)), "title": m.group(2).strip().title().replace("Vb", "VB").replace("Basic", "BASIC").replace("Mac?", "Mac?"), "line": i}
sections[0] = {"n": 0, "title": "Whole video / shared", "line": 0}

def cue_text(line_no):
    if not line_no or line_no > len(script):
        return ""
    t = script[line_no - 1].strip()
    t = re.sub(r"^\*\*\[VISUAL:\s*", "", t); t = re.sub(r"\]\*\*$", "", t)
    return t[:260]

# ---- register gate titles
register = (ROOT / "docs/EDITORIAL_REGISTER.md").read_text(encoding="utf-8")
gate_titles = {}
for m in re.finditer(r"^#{2,4}\s*(R\d{2}a?)\b[\s:—–-]*(.*)$", register, re.M):
    gate_titles[m.group(1)] = m.group(2).strip().strip("*").strip()
for m in re.finditer(r"^\|\s*\*{0,2}(R\d{2}a?)\*{0,2}\s*\|\s*([^|]+)\|", register, re.M):
    gate_titles.setdefault(m.group(1), m.group(2).strip())
print("gate titles found:", len(gate_titles), sorted(gate_titles)[:20])

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def norm_q(q, tid, gate, n):
    if isinstance(q, str):
        return {"id": f"{tid}-Q{n}", "gate": gate, "status": "open", "for": None, "question": q}
    qid = q.get("id") or f"{tid}-Q{n}"
    if not qid.startswith(tid):
        qid = f"{tid}-{qid}"
    return {"id": qid, "gate": q.get("gate", gate), "status": q.get("status", "open"),
            "for": q.get("for") or q.get("owner") or q.get("type"),
            "question": q.get("question") or q.get("text") or json.dumps(q, ensure_ascii=False)[:400],
            "resolution": q.get("resolution")}

deck = []
ledger_questions = []
decision_ledger = []
for r in rows:
    tid = r["id"]; d = ROOT / r["asset_dir"]
    state = load(d / "state.json")
    delivery = load(d / "delivery.json") if (d / "delivery.json").is_file() else {}
    cc = load(d / "evidence/claim-checks.json") if (d / "evidence/claim-checks.json").is_file() else {}
    gates = []
    seen_ids = set()
    qn = 0
    questions = []
    for q in cc.get("review_questions", []) or []:
        qn += 1; nq = norm_q(q, tid, None, qn); questions.append(nq)
    gl = cc.get("gates", [])
    if isinstance(gl, dict):
        gl = [dict(v, id=k) if isinstance(v, dict) else {"id": k, "status": str(v)} for k, v in gl.items()]
    for g in gl or []:
        if not isinstance(g, dict):
            continue
        gid = g.get("id") or g.get("gate")
        gates.append({"id": gid, "title": g.get("title") or gate_titles.get(gid, ""), "status": g.get("status"),
                      "approver": g.get("approver") if g.get("approver") not in ("None", None) else None,
                      "decision": g.get("decision"), "reason": (g.get("reason") or "")[:600],
                      "evidence": g.get("evidence") or g.get("evidence_paths") or []})
        for key in ("review_questions", "questions", "open_questions"):
            for q in g.get(key, []) or []:
                qn += 1; nq = norm_q(q, tid, gid, qn)
                if isinstance(q, str) and q in {x["id"] for x in questions}:
                    continue  # gate-level pointer back to a top-level question
                questions.append(nq)
    # de-dup by id
    uniq = OrderedDict()
    for q in questions:
        uniq.setdefault(q["id"], q)
    questions = list(uniq.values())
    for q in questions:
        ledger_questions.append(dict(q, ticket=tid, evidence=f"{r['asset_dir']}/evidence/claim-checks.json"))
    secs = r.get("sections") or []
    primary = secs[0] if len(secs) == 1 else (0 if len(secs) > 3 else (secs[0] if secs else 0))
    cues = r.get("cues") or []
    deck.append({
        "id": tid, "title": r["title"], "kind": r["kind"], "family": r["asset_dir"].split("/")[1],
        "sections": secs, "section": primary, "cues": cues, "cue_text": cue_text(cues[0]) if cues else "",
        "brief": r.get("brief", ""), "copy": (r.get("copy") or "")[:300],
        "production": state.get("production_status"), "release": state.get("release_status"),
        "reviewer": state.get("reviewer"),
        "duration": delivery.get("duration_seconds"), "dimensions": delivery.get("dimensions"),
        "variants": delivery.get("variants") if isinstance(delivery.get("variants"), list) else [],
        "credits": delivery.get("credits") if isinstance(delivery.get("credits"), list) else ([delivery["credits"]] if delivery.get("credits") else []),
        "provenance": delivery.get("provenance_type", ""),
        "gates": gates, "questions": questions,
        "open_questions": sum(1 for q in questions if q["status"] == "open"),
        "thumb": f"thumbs/{tid}.jpg" if (OUT / "thumbs" / f"{tid}.jpg").is_file() else None,
        "issue": r.get("github_issue"), "asset_dir": r["asset_dir"],
    })
    decision_ledger.append({"id": tid, "title": r["title"], "production_status": state.get("production_status"),
                            "release_status": state.get("release_status"), "reviewer": state.get("reviewer"),
                            "manifest_gates": r.get("gates", []), "gates": gates, "questions": questions})

order = {s: i for i, s in enumerate(sorted(k for k in sections if k))}
deck.sort(key=lambda a: (a["section"] if a["section"] else 99, a["cues"][0] if a["cues"] else 10**6, a["id"]))
data = {"generated": "2026-09-15", "sections": [sections[k] for k in sorted(sections) if k] + [sections[0]], "assets": deck,
        "counts": {"tickets": len(deck), "approved": sum(a["release"] == "approved" for a in deck),
                   "blocked": sum(a["release"] == "blocked" for a in deck), "unreviewed": sum(a["release"] == "unreviewed" for a in deck),
                   "open_questions": sum(a["open_questions"] for a in deck)}}
(OUT / "deck-data.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8", newline=LF)
print("deck assets:", len(deck), data["counts"])
print("by section:", {k: sum(1 for a in deck if a["section"] == k) for k in sorted(set(a["section"] for a in deck))})

# ---- ledgers
prev = load(ROOT / "review/editorial-review.json")
prev_by = {q["id"]: q for q in prev["questions"]}
merged = []
for q in ledger_questions:
    old = prev_by.get(q["id"])
    if old:
        q = dict(q, **{k: old[k] for k in old if k in ("status", "resolution", "for", "branch", "commit", "merged_in")})
    merged.append(q)
for q in prev["questions"]:
    if q["id"] not in {m["id"] for m in merged}:
        merged.append(q)
prev["questions"] = merged; prev["count"] = len(merged); prev["generated_by"] = "producer, 2026-09-15 (OPS-03 full sweep)"
(ROOT / "review/editorial-review.json").write_text(json.dumps(prev, indent=2, ensure_ascii=False) + LF, encoding="utf-8", newline=LF)
print("ledger questions:", len(merged), "open:", sum(q["status"] == "open" for q in merged))
ops3 = ROOT / "assets/ops/OPS-03/exports"; ops3.mkdir(parents=True, exist_ok=True)
(ops3 / "decision-ledger.json").write_text(json.dumps({"generated": "2026-09-15", "gate_titles": gate_titles, "tickets": decision_ledger}, indent=1, ensure_ascii=False) + LF, encoding="utf-8", newline=LF)
print("wrote OPS-03 decision-ledger.json")
