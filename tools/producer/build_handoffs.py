"""Package the human handoffs (producer step 8): narration script, recording plan, audio brief, assembly plan, upload package.

Writes docs/handoffs/H06-narration-script.md, H01-recording-plan.md, H03-H04-audio-brief.md, H05-assembly-plan.md,
H07-upload-package.md and refreshes docs/handoffs/README.md. Everything is derived from War/SCRIPT.md, manifest.json and
assets/ops/OPS-04/exports/; nothing here records, licenses, assembles or uploads anything.
"""
from __future__ import annotations
import csv, json, re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LF = "\n"; DATE = "2026-09-15"
script = (ROOT / "War/SCRIPT.md").read_text(encoding="utf-8").split("\n")
orig = (ROOT / "sources/SCRIPT.md").read_text(encoding="utf-8").split("\n")
manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8")); rows = manifest["tickets"]
inv = {r["id"]: r for r in csv.DictReader((ROOT / "assets/ops/OPS-04/exports/editor-inventory.csv").open(encoding="utf-8"))}

def norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[`*_\[\]]", "", s)).strip().lower()

# ---------------------------------------------------------------- parse sections of the working script
sections = []  # {n, title, start, end}
for i, line in enumerate(script):
    m = re.match(r"^## SECTION (\d+): (.+)$", line.strip())
    if m:
        sections.append({"n": int(m.group(1)), "title": m.group(2).strip(), "start": i})
    elif line.startswith("## PRODUCTION NOTES"):
        sections.append({"n": None, "title": None, "start": i})
for a, b in zip(sections, sections[1:]):
    a["end"] = b["start"]
sections = [s for s in sections if s["n"] is not None]
chapter_titles = {}
for line in script[:40]:
    m = re.match(r"^- (\d+:\d\d) — (.+)$", line.strip())
    if m:
        chapter_titles[len(chapter_titles) + 1] = (m.group(1), m.group(2))

def blocks(sec):
    """Yield ('narration', text) / ('visual', text) / ('code', text) in order for one section."""
    out = []; in_code = False; code = []
    para = []
    def flush():
        nonlocal para
        if para:
            out.append(("narration", " ".join(para))); para = []
    for line in script[sec["start"] + 1: sec["end"]]:
        s = line.rstrip()
        if s.startswith("```"):
            if in_code:
                out.append(("code", "\n".join(code))); code = []; in_code = False
            else:
                flush(); in_code = True
            continue
        if in_code:
            code.append(s); continue
        if s.startswith("**[VISUAL:"):
            flush(); out.append(("visual", re.sub(r"^\*\*\[VISUAL:\s*|\]\*\*$", "", s).strip())); continue
        if s.startswith("**NARRATION:**") or s == "---":
            flush(); continue
        if s.startswith("**Step") or s.startswith("|"):
            flush(); continue  # sub-bullets and table rows belong to the cue above them
        if not s.strip():
            flush(); continue
        para.append(s.strip())
    flush()
    return out

# ---------------------------------------------------------------- cue -> ticket mapping via the original cue text
cue_text_to_ids = defaultdict(list)
for r in rows:
    for ln in r.get("cues") or []:
        if 0 < ln <= len(orig):
            cue_text_to_ids[norm(orig[ln - 1])].append(r["id"])
sec_assets = defaultdict(list)
for r in rows:
    for n in r.get("sections") or []:
        sec_assets[n].append(r["id"])

ID_RE = re.compile(r"(?:TERM|CODE|DIA|HIST|XTRA|BROLL|CH|CARD|CMP|FACT|MOCK|REF|OPS)-\d{2}")
def ids_for_visual(text):
    named = sorted(set(ID_RE.findall(text)))
    if named:
        return named
    key = norm("**[VISUAL: " + text + "]**")
    ids = cue_text_to_ids.get(key)
    if ids:
        return sorted(set(ids))
    # fuzzy: original cue whose normalized text shares the first 40 chars
    head = norm(text)[:40]
    hits = [ids for k, ids in cue_text_to_ids.items() if head and head in k]
    return sorted({i for h in hits for i in h}) if hits else []

# ---------------------------------------------------------------- H06 narration script
PRON = [
    ("Dim", "say the word: 'dim'"), ("ByRef / ByVal", "'by ref', 'by val'"), ("MsgBox", "'message box' or 'msg box' (either, be consistent)"),
    ("vbc", "letters: 'v b c'"), ("Kemeny and Kurtz", "KEM-uh-nee, KURTS"), ("CompUSA", "'Comp U S A'"), ("Egghead, Babbage's", "as written; BAB-ij-iz"),
    ("Metrowerks CodeWarrior", "MET-ro-works"), ("ResEdit", "'rez edit'"), ("NeXT / NeXTSTEP", "'next', 'next step'"), ("Applesoft", "as written"),
    ("VBRUN300.DLL", "'v b run three hundred dot d l l'"), ("Fisher–Yates", "FISH-er YATES"), ("Sybase", "SY-base"), ("PowerBuilder", "as written"),
    ("QuickBASIC", "'quick basic'"), ("Jet engine", "as written"), ("MFC", "letters"), ("AWT", "letters"), ("Rnd.Next(0, i + 1)", "'random dot next of zero and i plus one' (or skip the code aloud; it is on screen)"),
    ("Exit Sub / Do...Loop / Next Rank", "read the keywords as words: 'exit sub', 'do loop', 'next rank'"),
]
h6 = ["# H06 — Narration script (recording copy)", "", f"Prepared {DATE} from `War/SCRIPT.md` at its current revision. Only spoken text is here; visual cues and code blocks are removed. Code the narration refers to is on screen in the corresponding CODE card, so read the words, not the listings, unless a sentence quotes a token (those are kept inline).", "",
      "**How to use:** record one file per section, named `H06-<section number>.wav`, into `assets/handoffs/H06/` (create it; it is not tracked yet). Keep a clean start and end on each file. Return the real durations; the chapter timestamps in the script metadata are estimates and will be replaced.", "",
      "## Pronunciation and reading notes", ""]
h6 += [f"- **{a}** — {b}" for a, b in PRON]
h6 += ["", "## Estimated running time", ""]
total_words = 0; rows_rt = []
sec_blocks = {}
for sec in sections:
    b = blocks(sec); sec_blocks[sec["n"]] = b
    words = sum(len(t.split()) for k, t in b if k == "narration"); total_words += words
    rows_rt.append((sec["n"], sec["title"], words, words / 150))
h6 += ["| Section | Title | Words | ~min at 150 wpm |", "|---|---|---|---|"]
h6 += [f"| {n} | {t} | {w} | {m:.1f} |" for n, t, w, m in rows_rt]
h6 += [f"| | **Total** | **{total_words}** | **{total_words/150:.0f}** |", "", "The script metadata estimates 45 minutes of chapters; narration alone at a relaxed pace is about the same, so allow for holds on code and captures.", ""]
for sec in sections:
    h6 += [f"## Section {sec['n']}: {sec['title']}", ""]
    for kind, text in sec_blocks[sec["n"]]:
        if kind == "narration":
            h6 += [text, ""]
(ROOT / "docs/handoffs/H06-narration-script.md").write_text(LF.join(h6), encoding="utf-8", newline=LF)

# ---------------------------------------------------------------- H05 assembly plan
h5 = ["# H05 — Assembly plan (script order, cue by cue)", "", f"Prepared {DATE}. Each section lists its visual cues in script order with the ticket that fulfils it and the file to drop on the timeline. `assets/ops/OPS-04/exports/editor-inventory.csv` has the full row for every ticket (duration, variants, credits); `exceptions.md` has the labels and cuts that must survive the edit.", "",
      "**Conventions:** every export is 1920×1080. Stills are PNG posters; motion assets have `exports/preview.mp4` (H.264, 30 fps) plus keyframes; captures are framed PNGs; B-roll is the original file under `source/` with the cut noted. Chapter cards (CH-01…16) open each section; CARD-01 opens the video and CARD-02 closes it.", ""]
unmatched = 0
for sec in sections:
    ch = chapter_titles.get(sec["n"])
    h5 += [f"## Section {sec['n']}: {sec['title']}", "", f"Open with **CH-{sec['n']:02d}** ({inv['CH-%02d' % sec['n']]['primary_file'] if 'CH-%02d' % sec['n'] in inv else ''}). Script chapter estimate: {ch[0] if ch else '?'}.", ""]
    h5 += ["| # | Cue (from the script) | Ticket(s) | File |", "|---|---|---|---|"]
    k = 0
    for kind, text in sec_blocks[sec["n"]]:
        if kind != "visual":
            continue
        k += 1; ids = ids_for_visual(text)
        if not ids: unmatched += 1
        files = "<br>".join(f"`{inv[i]['primary_file']}`" for i in ids if i in inv and inv[i]["primary_file"]) or "—"
        h5.append(f"| {k} | {text[:170]}{'…' if len(text) > 170 else ''} | {', '.join(ids) if ids else '(section assets below)'} | {files} |")
    others = sorted(set(sec_assets.get(sec["n"], [])) - {i for kind, text in sec_blocks[sec["n"]] if kind == "visual" for i in ids_for_visual(text)} - {f"CH-{sec['n']:02d}"})
    if others:
        h5 += ["", "Also assigned to this section: " + ", ".join(f"**{i}** ({inv[i]['kind']}, `{inv[i]['primary_file']}`)" for i in others if i in inv), ""]
    else:
        h5.append("")
h5 += ["## Notes", "", f"- {unmatched} cue lines could not be matched to a ticket by text (the cue was reworded during production); their assets are listed under 'also assigned to this section'.",
       "- The 62 MP4 previews are deterministic renders; play them at speed or scrub, both are frame-accurate.",
       "- Credits: the list in `exceptions.md` goes in the end credits and the description; XTRA-14 carries its own on-screen credit line and it must stay.", ""]
(ROOT / "docs/handoffs/H05-assembly-plan.md").write_text(LF.join(h5), encoding="utf-8", newline=LF)

# ---------------------------------------------------------------- H01 recording plan
h1 = ["# H01 — Screen recording plan", "", f"Prepared {DATE}. The TERM captures are stills of real runs; these recordings replace or supplement them with motion. Record at 1920×1080, 30 fps, cursor visible, no system audio. Use a fresh window; hide notifications and other windows first.", "",
      "## Set-up (once)", "", "```", "cd C:\\dev\\youtube\\vb-video-checkout-2", "python tools/war-harness/tools/capture_assets.py --help", "```",
      "The harness copies `tools/war-harness/War/` (byte-identical `Program.vb`, derived `War.vbproj`) into a work folder; never build inside `tools/war-harness/` itself. For a recording you can simply copy `tools/war-harness/War/` to a scratch folder and run `dotnet run` there.", "",
      "## Takes", "", "| Take | What | Command | Serves |", "|---|---|---|---|",
      "| R1 | Project creation | `dotnet new console -lang VB` in an empty folder, then `dotnet --version` | Section 4 (TERM-01 beat) |",
      "| R2 | Full game, run 1 | `dotnet run` in the copied War folder; let it scroll to the summary | Sections 1 (cold open, fast) and 11 |",
      "| R3 | Two more full runs | `dotnet run` twice more, different outcomes | Section 11, 'run it a few more times' |",
      "| R4 | War-heavy moment | keep running until a `** WAR! **` chain appears; TERM-04 found a double war on run 1 of 30 | Sections 1 and 10 |",
      "| R5 | Code scroll-through | `vim Program.vb` (or any editor at a readable size), scroll top to bottom slowly | Section 6 onward, whenever code is discussed; TERM-03 has the 12 viewports as stills |",
      "| R6 | Project file | open `War.vbproj`, show `OptionExplicit` and `OptionStrict` | Section 4 (XTRA-06 beat) |", "",
      "## Rules that still apply", "", "- Output is never edited or re-run to get a preferred result (R4 may be searched, as TERM-04 did, but say so in the take log).",
      "- Save raw files under `assets/handoffs/H01/` with a take log (command, time, outcome). A replay of a saved log must be labelled replay.",
      "- If you skip this handoff entirely, the edit uses the TERM stills with pan and scan; that is allowed.", ""]
(ROOT / "docs/handoffs/H01-recording-plan.md").write_text(LF.join(h1), encoding="utf-8", newline=LF)

# ---------------------------------------------------------------- H03/H04 audio brief
h34 = ["# H03 / H04 — Music and sound brief", "", f"Prepared {DATE}. The script asks for one bed and three effects (`War/SCRIPT.md`, Audio notes). Nothing has been chosen or licensed; record the source and terms for each file under `assets/handoffs/H03/` and `H04/`.", "",
       "## H03 — Background bed", "", "- Direction from the script: vaguely 90s, chiptune or lo-fi electronic, never distracting under narration.",
       "- Length: the cut will run about 45 minutes; a loopable 2–4 minute bed or a small set of beds (history sections, code sections, outro) is enough.",
       "- Keep it under the voice: the narration is dense, so a bed with a narrow mid-range and no vocals.",
       "- Record title, creator, source, licence and attribution wording; if the terms need a credit, add it to the credits list in `assets/ops/OPS-04/exports/exceptions.md`.", "",
       "## H04 — Effects", "", "| Effect | Where it lands | Assets it plays against |", "|---|---|---|",
       "| Card shuffle | Section 5 rules and Section 7 shuffle animation; also the cold-open B-roll | DIA-02, DIA-06, BROLL-01 |",
       "| Card slap | Each war flip and the pot award | DIA-08, DIA-09, the `** WAR! **` moments in Section 10 and 11 |",
       "| Windows 95 startup | Once, briefly, at the Windows 95 launch beat in Section 2 | HIST-08, BROLL-04 |", "",
       "The startup sound is Microsoft's; the script wants it once for comedy. Record the source and the basis you are using it on, as you did for the images.", ""]
(ROOT / "docs/handoffs/H03-H04-audio-brief.md").write_text(LF.join(h34), encoding="utf-8", newline=LF)

# ---------------------------------------------------------------- H07 upload package
meta_start = next(i for i, l in enumerate(script) if l.startswith("## Video Metadata"))
meta_end = next(i for i, l in enumerate(script) if l.startswith("## SECTION 1"))
meta = script[meta_start:meta_end]
desc = []; tags = ""; titles = []
mode = None
for l in meta:
    if l.startswith("**Title Options"): mode = "t"; continue
    if l.startswith("**Description"): mode = "d"; continue
    if l.startswith("**Tags"): mode = "g"; continue
    if l.startswith("**Chapters"): mode = "c"; continue
    if mode == "t" and re.match(r"^\d+\. ", l.strip()): titles.append(re.sub(r"^\d+\. ", "", l.strip()))
    elif mode == "d" and l.strip(): desc.append(l.strip())
    elif mode == "g" and l.strip(): tags = l.strip()
exc = (ROOT / "assets/ops/OPS-04/exports/exceptions.md").read_text(encoding="utf-8")
credits = exc.split("## Credits to carry")[1].strip().split("\n") if "## Credits to carry" in exc else []
h7 = ["# H07 — Upload package (draft metadata)", "", f"Prepared {DATE} from the script's Video Metadata block. Nothing here is uploaded; fill in the real chapter times from the locked cut, then publish from your own account.", "",
      "## Title", "", f"Use option 1, which is the title card (CARD-01): **{titles[0] if titles else ''}**", "", "Alternatives kept from the script:"] + [f"- {t}" for t in titles[1:]] + ["",
      "## Description", ""] + desc + ["", "Append the credits block below and, if you used H03/H04 sources that require it, their attribution lines.", "",
      "## Tags", "", tags, "", "## Chapters", "", "Replace the times with the real ones from the cut; the titles are the chapter cards."] + [f"- {t} — {ttl}" for n, (t, ttl) in sorted(chapter_titles.items())] + ["",
      "## Credits (from OPS-04 exceptions.md)", ""] + credits + ["",
      "## End screen", "", "CARD-02 leaves the platform's end-screen zones clear (see `assets/cards/CARD-02/src/` layer map); place subscribe and one next-video element there. No next video is chosen yet.", "",
      "## Checklist before you press publish", "", "- Chapter times replaced with real timings.", "- Credits present in the description.", "- Visibility, audience and any disclosure settings chosen deliberately.", "- Thumbnail chosen (none was produced; CARD-01's poster is a usable base).", ""]
(ROOT / "docs/handoffs/H07-upload-package.md").write_text(LF.join(h7), encoding="utf-8", newline=LF)

# ---------------------------------------------------------------- README
readme = ["# Human and capability handoffs", "",
          f"Asset production finished on {DATE} (134/134 produced and release-approved). What remains is the work only Devin can do. Each handoff below has its original boundary note (H0x.md) and, from session 8, a prepared package that lays out inputs, exact steps and where results go.", "",
          "| Handoff | What you do | Package |", "|---|---|---|",
          "| H06 | Record the narration | [H06-narration-script.md](H06-narration-script.md) — spoken text only, per section, with pronunciation notes and timings |",
          "| H01 | Screen recordings (optional; stills exist) | [H01-recording-plan.md](H01-recording-plan.md) — six takes with commands |",
          "| H03, H04 | Music bed and three effects | [H03-H04-audio-brief.md](H03-H04-audio-brief.md) |",
          "| H05 | Assemble the video | [H05-assembly-plan.md](H05-assembly-plan.md) — cue-by-cue with files; plus `assets/ops/OPS-04/exports/editor-inventory.csv` and `exceptions.md` |",
          "| H07 | Upload | [H07-upload-package.md](H07-upload-package.md) — title, description, tags, chapters, credits |",
          "| H02 | Gated stock footage | Not needed: all six B-roll clips came from free sources. [H02.md](H02.md) stays as the record. |", "",
          "Original boundary notes: [H01](H01.md) · [H02](H02.md) · [H03](H03.md) · [H04](H04.md) · [H05](H05.md) · [H06](H06.md) · [H07](H07.md).", ""]
(ROOT / "docs/handoffs/README.md").write_text(LF.join(readme), encoding="utf-8", newline=LF)
print(f"handoffs written; narration words {total_words}; unmatched cues {unmatched}")
