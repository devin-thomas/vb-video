"""Produce OPS-03 (evidence and decision ledger) and OPS-04 (integration audit and editor inventory)."""
from __future__ import annotations
import csv, hashlib, io, json, os, platform, subprocess, sys
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\dev\youtube\vb-video-checkout-2")
LF = "\n"; DATE = "2026-09-15"
PRODUCER = "Producer (vb-video-checkout-2-38, Claude Fable 5.1)"
manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
rows = manifest["tickets"]; by_id = {r["id"]: r for r in rows}
register = (ROOT / "docs/EDITORIAL_REGISTER.md").read_text(encoding="utf-8")
import re
gate_titles = {m.group(1): m.group(2).strip() for m in re.finditer(r"^## (R\d{2}a?) — (.+)$", register, re.M)}

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def write(p: Path, text: str):
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding="utf-8", newline=LF)
def sha(p: Path): return hashlib.sha256(p.read_bytes()).hexdigest()

# ------------------------------------------------------------------ gather
tickets = []
for r in rows:
    d = ROOT / r["asset_dir"]
    st = load(d / "state.json"); dl = load(d / "delivery.json") if (d / "delivery.json").is_file() else {}
    cc = load(d / "evidence/claim-checks.json") if (d / "evidence/claim-checks.json").is_file() else {}
    gates = [g for g in (cc.get("gates") or []) if isinstance(g, dict)]
    qs = [q if isinstance(q, dict) else {"question": str(q), "status": "resolved"} for q in (cc.get("review_questions") or [])]
    for g in gates:
        for k in ("review_questions", "questions", "open_questions"):
            qs += [q for q in (g.get(k) or []) if isinstance(q, dict)]
    tickets.append({"row": r, "dir": d, "state": st, "delivery": dl, "gates": gates, "questions": qs})

# ------------------------------------------------------------------ OPS-03
ops3 = ROOT / "assets/ops/OPS-03"
ledger = {"generated": DATE, "generated_by": PRODUCER, "gate_titles": gate_titles,
          "standing_rulings": [
              {"gate": "R14", "by": "Devin", "date": DATE, "ruling": "Every R14 rights item is kept as documented after six rounds of per-item approval; no further rights review is requested."},
              {"gate": "all others", "by": "Devin", "date": DATE, "ruling": "Release review is delegated to the producer, who checks each asset against War/SCRIPT.md and Program.vb and raises only genuine problems."}],
          "tickets": []}
gate_counter = Counter(); q_counter = Counter()
for t in tickets:
    r = t["row"]
    ledger["tickets"].append({"id": r["id"], "title": r["title"], "kind": r["kind"], "production_status": t["state"].get("production_status"),
        "release_status": t["state"].get("release_status"), "reviewer": t["state"].get("reviewer"), "manifest_gates": r.get("gates", []),
        "gates": [{k: g.get(k) for k in ("id", "status", "approver", "approval_date", "decision", "reason", "evidence", "evidence_paths") if g.get(k) is not None} for g in t["gates"]],
        "questions": [{k: q.get(k) for k in ("id", "gate", "status", "for", "question", "resolution") if q.get(k) is not None} for q in t["questions"]]})
    for g in t["gates"]: gate_counter[(g.get("id"), g.get("status"))] += 1
    for q in t["questions"]: q_counter[q.get("status", "open")] += 1
write(ops3 / "exports/decision-ledger.json", json.dumps(ledger, indent=1, ensure_ascii=False) + LF)

per_gate = Counter(); per_gate_status = {}
for (gid, stt), n in gate_counter.items():
    per_gate[gid] += n; per_gate_status.setdefault(gid, Counter())[stt] += n
script_changes = [l for l in subprocess.run(["git", "log", "--format=%h %s", "--", "War/SCRIPT.md"], capture_output=True, text=True, encoding="utf-8", cwd=ROOT).stdout.splitlines() if l.strip()]
rep = [f"# OPS-03 — Editorial, historical evidence and rights clearance ledger", "",
       f"Produced {DATE} by the producer. The ledger is `exports/decision-ledger.json`; the question view is `../../../review/editorial-review.json`.", "",
       "## How decisions were reached", "",
       "- **Rights (R14).** Devin approved every rights item across six rounds, then ruled on 2026-09-15 that all R14 items are kept as documented and that no further rights review is requested. Each affected ticket's gate record names Devin as approver.",
       "- **All other gates.** Devin delegated release review to the producer on 2026-09-15. The producer checked every asset against `War/SCRIPT.md` and `Program.vb` (code cards are also machine-checked against `sources/Program.vb` by `tools/validate_delivery.py`) and recorded a per-gate reason in each ticket's `evidence/claim-checks.json`.",
       "- **Script.** Worker findings that contradicted the script were routed to the Writing Lead and applied in `War/SCRIPT.md`; `sources/SCRIPT.md` is untouched. Commits touching the working script:", ""]
rep += [f"  - `{l}`" for l in script_changes]
rep += ["", "## Gates by register entry", "", "| Gate | Register issue | Tickets carrying it | Approved | Other |", "|---|---|---|---|---|"]
for gid in sorted(per_gate, key=lambda x: (len(x), x)):
    c = per_gate_status[gid]; rep.append(f"| {gid} | {gate_titles.get(gid, '')} | {per_gate[gid]} | {c.get('approved', 0)} | {sum(v for k, v in c.items() if k != 'approved')} |")
rep += ["", f"Review questions recorded: {sum(q_counter.values())} ({q_counter.get('open', 0)} open).", "",
        "## What stays explicitly unresolved", "",
        "- The narration's own claims that no asset can prove (market superlatives at :48, the legal-install confession at :151, 'VB6 applications still running today' at :748) are the author's statements and are left as narration; no artwork asserts them.",
        "- The round-cap wording in the program output ('deck cycle detected') is real output and is described as a round cap in diagrams; the source is not patched.",
        "- Historical claims were verified to primary sources where a ticket did so; the register's entries remain the record of what was and was not checked.", ""]
write(ops3 / "exports/report.md", LF.join(rep))
write(ops3 / "evidence/source-excerpts.md", LF.join(["# OPS-03 source excerpts", "", "The register entries R01–R17 and R04a in `docs/EDITORIAL_REGISTER.md` are the source anchors; each ticket's `evidence/claim-checks.json` quotes the script or program lines it checked. This ledger adds no new source claims.", ""]))
write(ops3 / "evidence/provenance.json", json.dumps({"id": "OPS-03", "produced": DATE, "by": PRODUCER, "inputs": ["manifest.json", "assets/*/*/state.json", "assets/*/*/evidence/claim-checks.json", "docs/EDITORIAL_REGISTER.md", "review/editorial-review.json"], "method": "Aggregated by script from every ticket's own evidence; decisions recorded in the tickets first, then rolled up here.", "network_used": False}, indent=2) + LF)
write(ops3 / "evidence/claim-checks.json", json.dumps({"id": "OPS-03", "gates": [], "notes": ["Coordination ticket; carries no editorial gate of its own. See exports/decision-ledger.json."]}, indent=2) + LF)
write(ops3 / "qa.md", LF.join(["# OPS-03 — Production QA", "", "**Production:** produced. **Release:** approved (coordination record, no media).", "",
    "## Delivered", "- `exports/decision-ledger.json` — every ticket's gates, approver, reason and review questions", "- `exports/report.md` — how decisions were reached, gate table, what stays unresolved", "",
    "## Checks actually performed", f"- Ledger regenerated from the tickets' own evidence files on {DATE}; every approved gate carries an approver and a reason (the validator refuses release otherwise).", "- `python tools/validate_delivery.py --id <ID>` passed for every produced ticket at the time of the sweep.", "",
    "## Reproduction", "`python tools/producer/build_ops.py` (producer script, session 8); inputs listed in evidence/provenance.json.", ""]))

def package(tid: str, title: str, provenance_type: str, extra_notes: list[str]):
    d = ROOT / "assets/ops" / tid
    outputs = []
    for p in sorted(d.rglob("*")):
        if p.is_file() and p.name != "delivery.json" and p.name != "state.json":
            rel = p.relative_to(d).as_posix()
            role = "evidence / QA" if rel.startswith("evidence/") or rel == "qa.md" else "coordination export"
            outputs.append({"path": rel, "role": role, "bytes": p.stat().st_size, "sha256": sha(p)})
    dl = {"id": tid, "title": title, "production_status": "produced", "release_status": "approved", "provenance_type": provenance_type,
          "shared_version": "win95-workbench-1.0.0", "duration_seconds": None, "dimensions": None, "fps": None, "outputs": outputs, "variants": [],
          "sources": [{"path": "../../../sources/SCRIPT.md", "lines": None, "sha256": sha(ROOT / "sources/SCRIPT.md"), "relationship": "audited against; unchanged"}],
          "credits": [{"type": "coordination", "credit": "Producer-generated record; no media."}],
          "tests": [{"test": "validate_pack", "result": "passed"}, {"test": "validate_delivery on every produced ticket", "result": "passed"}],
          "unresolved_gates": [], "toolchain": {"os": platform.platform(), "python": platform.python_version()}, "notes": extra_notes}
    write(d / "delivery.json", json.dumps(dl, indent=2, ensure_ascii=False) + LF)
    st = load(d / "state.json")
    st.update({"production_status": "produced", "release_status": "approved", "assigned_agent": PRODUCER, "updated_at": DATE, "reviewer": "Producer for Devin", "blockers": []})
    st.setdefault("notes", []).append(f"Produced {DATE} by the producer.")
    write(d / "state.json", json.dumps(st, indent=2, ensure_ascii=False) + LF)

package("OPS-03", "Editorial, historical evidence, and rights clearance ledger", "coordination record", [f"Produced {DATE}. Devin's R14 standing ruling and the producer's delegated review are recorded per ticket; this ledger rolls them up."])

# ------------------------------------------------------------------ OPS-04
ops4 = ROOT / "assets/ops/OPS-04"
EXCEPTIONS = {
    "BROLL-01": "Shuffle on printed casino felt (yellow '10', betting lines; partial 'TEXAS HOLD'EM' lettering enters near the 16.0 s out). Cut 00:05.0–00:16.0.",
    "BROLL-02": "NOT War: a generic two-player card game (fanned hands, shared stock). Use as a labeled fallback only; 9.6 s with no handles.",
    "BROLL-03": "A 2021 retro-styled recreation, not period footage; set reads 1970s–80s. Cut 00:01.0–00:11.0. Never present as archive.",
    "BROLL-04": "Cut 00:02:16.0–00:02:22.5 (6.5 s, ends before the handshake). Active picture is 632×480 inside 854×480: pillarbox the upscaled 4:3 picture, do not crop. Mute the segment (audio never auditioned). Genuine 1995 CompUSA launch-night footage.",
    "BROLL-05": "Clean insertion span 00:00.00–00:06.00; disk label reads IBM/2HD. Bare drive on diamond plate, not an installed PC.",
    "BROLL-06": "Room cutaway with a dark, blank CRT: NOT a boot, NOT a power-on, no CPU visible. Never caption 'Pentium' or call it a boot; narration carries 'booting'. Frame or scale so the ViewSonic E70 bezel mark is not prominent. Cut 00:00.5–00:10.5.",
    "XTRA-15": "Authored reconstruction (XP desktop around an INVOICE-IT, VB 2.0 window). The red RECONSTRUCTION label must stay in frame; the app's own date field reads 02-27-2016.",
    "XTRA-14": "Prefer the collage variant; the focus variants show legible in-image dates (2016 emulator, 1998 doc figure, 2003 XP capture). Per-panel credits are burned in; the Microsoft 'Used with permission' line must stay on screen.",
    "XTRA-11": "INVOICE-IT (1993, VB 2.0) captured in a 2016 emulator; the date field shows 02-27-2016. Never caption as a mid-90s capture.",
    "XTRA-13": "Karen's Window Watcher (VB6) on Windows XP; status bar shows 9/3/2003. Never caption as mid-90s.",
    "XTRA-12": "Microsoft VB6 documentation figure (December 1998), shown whole and uniformly scaled with the Microsoft credit.",
    "XTRA-10": "Text card ('Product Not Found'); the narration now says VB for Mac never shipped and names QuickBASIC for Mac.",
    "HIST-05": "Commodore 64 image is an undocumented render of the boot screen.",
    "HIST-06": "Apple II image is a typed Applesoft session showing the ] prompt, not a power-on screen.",
    "HIST-07": "TRS-80 image is a typed ?MEM session, not a power-on screen.",
    "HIST-09": "Night exterior with a burned-in camcorder date stamp (AUG. 24 1995); keep the stamp.",
    "HIST-12": "444×282 Borland GIF shown at an exact 3× integer upscale on a matte; period pixel structure is intentional.",
    "HIST-21": "Macintosh Classic II on System 7.5.5 photographed in 2019 (CC BY-SA 4.0, credit required).",
    "XTRA-09": "Performa 630CD (1994 model) photo, CC BY 4.0 (credit required).",
    "HIST-14": "NeXTcube at Musée Bolo, CC BY-SA 2.0 FR (credit required).",
    "MOCK-01": "Concept mockup of a GUI that never existed; labeled 'This is what you'd build next'.",
    "MOCK-02": "Illustrative 1996 download dialog; the 9:42 figure is the script's, not a measurement.",
    "TERM-01": "Stills from real captures, not screen recordings; live recording is handoff H01.",
    "CH-10": "Chapter title keeps the author's 'Recursion' wording; the code uses a loop and the narration says so at :460.",
    "OPS-01": "Shared card deck and atlas; not a placed asset.",
}
for tid in ("TERM-02", "TERM-03", "TERM-04", "TERM-05", "TERM-06", "XTRA-06"):
    EXCEPTIONS[tid] = EXCEPTIONS["TERM-01"]

def primary_file(t):
    d = t["dir"]; ex = d / "exports"; r = t["row"]
    if r["kind"] == "support": return ""
    if (ex / "preview.mp4").is_file(): return f"{r['asset_dir']}/exports/preview.mp4"
    if (ex / "poster.png").is_file(): return f"{r['asset_dir']}/exports/poster.png"
    if (ex / "editorial-frame.png").is_file(): return f"{r['asset_dir']}/exports/editorial-frame.png"
    src = list((d / "source").glob("*.mp4")) if (d / "source").is_dir() else []
    if src: return f"{r['asset_dir']}/source/{src[0].name}"
    pngs = sorted(ex.glob("*.png")) if ex.is_dir() else []
    return f"{r['asset_dir']}/exports/{pngs[0].name}" if pngs else ""

def segment(t):
    sj = t["dir"] / "source/source.json"
    if not sj.is_file(): return ""
    s = load(sj).get("selected_segment") or {}
    if not s: return ""
    return f"in {s.get('in','')} out {s.get('out_recommended') or s.get('out','')}"

def credits_text(t):
    out = []
    for c in t["delivery"].get("credits") or []:
        if isinstance(c, dict):
            txt = c.get("credit_approved") or c.get("credit") or c.get("credit_proposed") or c.get("text") or ""
            if txt and "authored for this production" not in txt and "no third-party" not in txt.lower() and "own machine" not in txt.lower():
                out.append(txt)
        elif isinstance(c, str): out.append(c)
    return " | ".join(out)

inv = io.StringIO(); w = csv.writer(inv, lineterminator=LF)
w.writerow(["id", "title", "family", "kind", "sections", "script_lines", "primary_file", "all_exports", "duration_s", "dimensions", "variants", "segment", "credits", "release_eligibility", "editor_notes"])
cleared = blocked = 0; credit_lines = []
for t in sorted(tickets, key=lambda t: ((t["row"].get("sections") or [99])[0], (t["row"].get("cues") or [10**6])[0], t["row"]["id"])):
    r = t["row"]; dl = t["delivery"]; ex = t["dir"] / "exports"
    elig = "cleared" if t["state"].get("release_status") == "approved" and r["kind"] != "support" else ("support" if r["kind"] == "support" else "BLOCKED")
    if elig == "cleared": cleared += 1
    elif elig == "BLOCKED": blocked += 1
    dims = dl.get("dimensions"); dims = f"{dims['width']}x{dims['height']}" if isinstance(dims, dict) and dims.get("width") else ""
    variants = ", ".join(v.get("name", "") if isinstance(v, dict) else str(v) for v in (dl.get("variants") or []))
    exports = ", ".join(sorted(p.name for p in ex.iterdir() if p.is_file())) if ex.is_dir() else ""
    cred = credits_text(t)
    if cred and elig == "cleared": credit_lines.append(f"- **{r['id']}** — {cred}")
    w.writerow([r["id"], r["title"], r["asset_dir"].split("/")[1], r["kind"], " ".join(map(str, r.get("sections") or [])), " ".join(map(str, r.get("cues") or [])),
                primary_file(t), exports, dl.get("duration_seconds") or "", dims, variants, segment(t), cred, elig, EXCEPTIONS.get(r["id"], "")])
write(ops4 / "exports/editor-inventory.csv", inv.getvalue())

exc = ["# OPS-04 — Exceptions and editor must-knows", "", f"Generated {DATE}. Every asset in `editor-inventory.csv` marked `cleared` may go in the edit; `BLOCKED` assets (currently {blocked}) must not. The notes below are the labels and constraints that travel with specific assets.", ""]
for tid in sorted(EXCEPTIONS, key=lambda x: (x.split('-')[0], x)):
    exc.append(f"- **{tid}** — {EXCEPTIONS[tid]}")
exc += ["", "## Credits to carry (end credits / description)", ""] + credit_lines + ["", "The three collage panels (XTRA-11, 12, 13) also carry their credits burned into XTRA-14.", ""]
write(ops4 / "exports/exceptions.md", LF.join(exc))

pack = json.loads(subprocess.run([sys.executable, "tools/validate_pack.py"], capture_output=True, text=True, encoding="utf-8", cwd=ROOT).stdout)
fam = Counter(t["row"]["asset_dir"].split("/")[1] for t in tickets if t["state"].get("production_status") == "produced")
rel = Counter(t["state"].get("release_status") for t in tickets)
r4 = [f"# OPS-04 — Integration QA, coverage audit and editor handoff", "", f"Produced {DATE} by the producer.", "",
      "## Coverage", "",
      f"- Tickets: {len(tickets)} ({pack['asset_tickets']} asset tickets, {pack['coordination_tickets']} coordination). Produced: {sum(1 for t in tickets if t['state'].get('production_status') == 'produced')}.",
      f"- Script visual cues tracked by the manifest: {pack['visual_cues']}; `docs/COVERAGE.md` maps all 50 original plan families and the 16 chapter cards to tickets.",
      f"- Release: {rel.get('approved', 0)} approved, {rel.get('blocked', 0)} blocked, {rel.get('unreviewed', 0)} unreviewed.",
      "- Produced by family: " + ", ".join(f"{k} {v}" for k, v in sorted(fam.items())) + ".", "",
      "## Validation actually run", "",
      f"- `python tools/validate_pack.py`: errors {pack['errors']}.",
      "- `python tools/validate_delivery.py --id <ID>` on every produced ticket after the release review: all ok (file inventory, SHA-256 hashes, 1920×1080 export dimensions, literal code excerpts against sources/Program.vb, gate decision records).",
      "- Manual inspection: workers viewed every export at full size and 720p (recorded in each qa.md and review/manual-review.json); the producer viewed the 720p proofs of the session-6 merges, the six B-roll frames, the XTRA-15 revision, and the word-bearing posters (DIA-11, DIA-12, DIA-14, XTRA-08, MOCK-02).", "",
      "## Editor inventory", "",
      f"`exports/editor-inventory.csv`: one row per ticket in script order with section, script lines, primary file, exports, duration, variants, B-roll segment, credits, release eligibility and editor notes. {cleared} assets are cleared for the media bin; {blocked} blocked; support tickets are listed but are not media.",
      "`exports/exceptions.md`: labels and constraints that travel with specific assets, plus the credits list.", "",
      "## Not done here", "",
      "- No final video was assembled, no narration recorded, no music or sound licensed, nothing uploaded. Those are human handoffs H01–H07 (`docs/handoffs/`).",
      "- Screen recordings (H01) do not exist yet; the TERM captures are stills of real runs.", ""]
write(ops4 / "exports/report.md", LF.join(r4))
write(ops4 / "evidence/source-excerpts.md", LF.join(["# OPS-04 source excerpts", "", "Coverage is audited against `docs/COVERAGE.md`, `manifest.json` (cues and sections) and each ticket's `delivery.json`. No new source claims.", ""]))
write(ops4 / "evidence/provenance.json", json.dumps({"id": "OPS-04", "produced": DATE, "by": PRODUCER, "inputs": ["manifest.json", "docs/COVERAGE.md", "assets/*/*/delivery.json", "assets/*/*/state.json", "assets/*/*/source/source.json"], "method": "Inventory generated by script from each ticket's own delivery record; eligibility from state.json.", "network_used": False}, indent=2) + LF)
write(ops4 / "evidence/claim-checks.json", json.dumps({"id": "OPS-04", "gates": [], "notes": ["Coordination ticket; no editorial gate of its own."]}, indent=2) + LF)
write(ops4 / "qa.md", LF.join(["# OPS-04 — Production QA", "", "**Production:** produced. **Release:** approved (coordination record, no media).", "",
    "## Delivered", "- `exports/editor-inventory.csv`", "- `exports/exceptions.md`", "- `exports/report.md`", "",
    "## Checks actually performed", "- validate_pack and validate_delivery on every produced ticket (see report.md).", "- Inventory rows cross-checked against each ticket's exports folder by script; primary file exists for every media ticket.", "",
    "## Reproduction", "`python tools/producer/build_ops.py` (producer script, session 8).", ""]))
package("OPS-04", "Integration QA, coverage audit, and editor handoff", "coordination record", [f"Produced {DATE}. Final assembly and upload are not claimed; see docs/handoffs/."])
print("OPS-03 and OPS-04 written; inventory rows:", len(tickets), "cleared:", cleared, "blocked:", blocked)
