"""Build narration beats from War/SCRIPT.md.

Writes narration/beats.json: one beat per narration paragraph (long paragraphs split at sentence boundaries, very
short lead-ins merged into the paragraph they introduce), each with the written text, the spoken text (approved
spoken glossary v0.3 from the narration benchmark, code tokens read as words, numbers and years spelled out), and
the visual cues and code blocks that precede it in the script. The spoken text is what the narrator reads; the
written text is what captions show.

  python tools/narration/beats.py            # writes narration/beats.json and prints a summary
  python tools/narration/beats.py --show S06 # prints the beats of one section
"""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "War/SCRIPT.md"
GLOSSARY = Path(r"C:\dev\youtube\video-explainers-pipeline\narration-benchmark\corpus\spoken-glossary.v0.3.json")
OUT = ROOT / "narration/beats.json"
LF = "\n"
MAX_WORDS = 65   # split above this
MIN_WORDS = 14   # merge a lead-in shorter than this into the next paragraph

# ------------------------------------------------------------------ spoken forms
ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

def num_words(n: int) -> str:
    if n < 20: return ONES[n]
    if n < 100: return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")
    if n < 1000: return ONES[n // 100] + " hundred" + (" " + num_words(n % 100) if n % 100 else "")
    if n < 1_000_000:
        return num_words(n // 1000) + " thousand" + (" " + num_words(n % 1000) if n % 1000 else "")
    return str(n)

def year_words(y: int) -> str:
    if 1900 <= y <= 1999: return "nineteen " + (num_words(y - 1900) if y - 1900 >= 10 else "oh-" + ONES[y - 1900])
    if 2000 <= y <= 2009: return "two thousand" + (" " + ONES[y - 2000] if y - 2000 else "")
    if 2010 <= y <= 2099: return "twenty " + num_words(y - 2000)
    return num_words(y)

CODE_TOKENS = {  # exact backtick tokens in the narration -> how Aiden should read them
    "&": "the ampersand", "+": "plus", "i--": "i minus minus", "Step -1": "step minus one", ".vbproj": "dot V B proj",
    "Queue<Card>": "queue of card", "std::queue": "standard queue", "int rank;": "int rank", "char suit;": "char suit",
    "return Top;": "return top", "for (int i = 0; i < 14; i++)": "for, int i equals zero, i less than fourteen, i plus plus",
    "Do While...Loop": "do while loop", "Do...Loop": "do loop", "Do While": "do while", "Exit Sub": "exit sub",
    "Rnd.Next(0, i + 1)": "random dot next of zero and i plus one", "x": "x", "vbc": "V B C", "DIM": "dim",
    "For Rank = 2 To 14": "for rank equals two to fourteen", "For i = 51 To 1 Step -1": "for i equals fifty-one to one, step minus one",
    "Dim Rank As Integer": "dim rank as integer", "DrawTopCard = Top": "draw top card equals top", "Next Rank": "next rank",
    "If PlayerScore > HighScore Then": "if player score is greater than high score then", "For Each Item In Collection": "for each item in collection",
    "PictureBox": "picture box", "Command1_Click": "command one click", "MsgBox": "message box", "VBRUN300.DLL": "V B run three hundred dot D L L",
    "Select Case": "select case", "Option Explicit": "option explicit", "ReDim": "re-dim", "Structure": "structure", "Type": "type",
    "Sub": "sub", "Function": "function", "For": "for", "Next": "next", "Dim": "dim", "void": "void", "function": "function",
}
PLAIN = [  # spoken forms applied outside backticks, longest first
    ("VB.NET", "V B dot NET"), ("VBRUN300.DLL", "V B run three hundred dot D L L"), ("MsgBox", "message box"),
    ("Program.vb", "Program dot V B"), (".NET SDK", "dot NET S D K"), (".NET", "dot NET"), ("C#", "C sharp"), ("C++", "C plus plus"),
    ("SDK", "S D K"), ("NeXTSTEP", "next step"), ("NeXT", "next"), ("IDE", "I D E"), ("GUI", "gooey"), ("RAD", "rad"), ("MFC", "M F C"),
    ("AWT", "A W T"), ("CPU", "C P U"), ("CPUs", "C P Us"), ("DLL", "D L L"), ("BBS", "B B S"), ("CD-ROM", "C D ROM"), ("MSDN", "M S D N"),
    ("VB6", "V B six"), ("VB4", "V B four"), ("VB3", "V B three"), ("VB1", "V B one"), ("VB 1.0", "V B one point oh"), ("VB 2.0", "V B two point oh"),
    ("VB 3.0", "V B three point oh"), ("VB 4.0", "V B four point oh"), ("VB 5.0", "V B five point oh"), ("VB 6.0", "V B six point oh"),
    ("Visual C++ 4.0", "Visual C plus plus four point oh"), ("Delphi 1.0", "Delphi one point oh"), ("Java 1.0", "Java one point oh"),
    ("QuickBASIC 1.00", "QuickBASIC one point oh"), ("Windows 3.0", "Windows three point oh"), ("Windows 3.1", "Windows three point one"),
    ("Windows 3.x", "Windows three point x"), ("System 7", "System seven"), ("Windows 95", "Windows ninety-five"), ("Windows XP", "Windows X P"),
    ("F5", "F five"), ("14.4", "fourteen-four"), ("3.5-inch", "three-and-a-half-inch"), ("52-card", "fifty-two card"), ("$100", "hundred-dollar"),
    ("20,000", "twenty thousand"), ("200-kilobyte", "two-hundred-kilobyte"), ("68k", "sixty-eight K"), ("TRS-80", "T R S eighty"),
    ("Commodore 64", "Commodore sixty-four"), ("Apple II", "Apple two"), ("mid-90s", "mid-nineties"), ("90s", "nineties"), ("C89", "C eighty-nine"), ("Win16", "Win sixteen"), ("VB", "V B"),
]
NAMES = {"Kemeny": "Kemeny", "Kurtz": "Kurtz"}  # kept as written; the C05 fixture read them acceptably

def spoken_form(text: str, glossary: dict) -> str:
    entries = sorted(glossary["entries"], key=lambda e: -len(e["written"]))
    def code(m):
        tok = m.group(1)
        for e in entries:
            if tok == e["written"]: return e["spoken"]
        if tok in CODE_TOKENS: return CODE_TOKENS[tok]
        t = tok.replace("_", " ").replace("...", " ").replace("::", " ").replace(".", " dot ")
        t = re.sub(r"([a-z])([A-Z])", r"\1 \2", t)  # camelCase
        return t.lower()
    s = re.sub(r"`([^`]+)`", code, text)
    s = s.replace("**", "").replace("*", "")
    for e in entries:
        s = re.sub(r"(?<![A-Za-z])" + re.escape(e["written"]) + r"(?![A-Za-z])", e["spoken"], s)
    for w, sp in PLAIN:
        s = re.sub(r"(?<![A-Za-z0-9])" + re.escape(w) + r"(?![A-Za-z0-9])", sp, s)
    s = re.sub(r"\b(1[89]\d\d|20\d\d)\b", lambda m: year_words(int(m.group(0))), s)
    s = re.sub(r"\b(\d{1,3}),(\d{3})\b", lambda m: num_words(int(m.group(1) + m.group(2))), s)
    s = re.sub(r"\b(\d+)\.(\d+)\b", lambda m: num_words(int(m.group(1))) + " point " + ("oh" if m.group(2) == "0" else " ".join(ONES[int(c)] for c in m.group(2))), s)
    s = re.sub(r"\b\d+\b", lambda m: num_words(int(m.group(0))) if int(m.group(0)) < 1_000_000 else m.group(0), s)
    s = s.replace("—", ", ").replace("–", " to ").replace("…", "...")
    s = re.sub(r"\s+,", ",", s); s = re.sub(r",\s*,", ",", s); s = re.sub(r"\s{2,}", " ", s)
    return s.strip()

def decades(text: str) -> str:
    def rep(m):
        y = int(m.group(1)); base = year_words(y)
        return (base.replace("nineteen ", "nineteen ") + "s") if base.endswith("y") else base + "s"
    return re.sub(r"\b(19[0-9]0|20[0-9]0)s\b", lambda m: {"1960": "nineteen sixties", "1970": "nineteen seventies", "1980": "nineteen eighties", "1990": "nineteen nineties", "2000": "two thousands", "2010": "twenty tens"}.get(m.group(1), m.group(0)), text)

# ------------------------------------------------------------------ script parsing
def parse(script_lines: list[str]):
    sections = []
    for i, line in enumerate(script_lines):
        m = re.match(r"^## SECTION (\d+): (.+)$", line.strip())
        if m: sections.append({"n": int(m.group(1)), "title": m.group(2).strip(), "start": i})
        elif line.startswith("## PRODUCTION NOTES"): sections.append({"n": None, "start": i})
    for a, b in zip(sections, sections[1:]): a["end"] = b["start"]
    sections = [s for s in sections if s["n"] is not None]
    beats = []
    for sec in sections:
        pending_cues, pending_code, para = [], [], []
        items = []  # (text, cues, code)
        in_code, code = False, []
        def flush():
            nonlocal para, pending_cues, pending_code
            if para:
                items.append((" ".join(para), pending_cues, pending_code)); para, pending_cues, pending_code = [], [], []
        for line in script_lines[sec["start"] + 1: sec["end"]]:
            s = line.rstrip()
            if s.startswith("```"):
                if in_code: pending_code.append("\n".join(code)); code, in_code = [], False
                else: flush(); in_code = True
                continue
            if in_code: code.append(s); continue
            if s.startswith("**[VISUAL:"):
                flush(); pending_cues.append(re.sub(r"^\*\*\[VISUAL:\s*|\]\*\*$", "", s).strip()); continue
            if s.startswith("**NARRATION:**") or s == "---" or s.startswith("**Step") or s.startswith("|"): flush(); continue
            if not s.strip(): flush(); continue
            para.append(s.strip())
        flush()
        # merge short lead-ins into the next paragraph
        merged = []
        i = 0
        while i < len(items):
            text, cues, code_blocks = items[i]
            if len(text.split()) < MIN_WORDS and i + 1 < len(items) and not items[i + 1][1] and not items[i + 1][2]:
                nt, nc, ncode = items[i + 1]
                merged.append((text + " " + nt, cues, code_blocks)); i += 2; continue
            merged.append((text, cues, code_blocks)); i += 1
        # split long paragraphs at sentence boundaries
        n = 0
        for text, cues, code_blocks in merged:
            chunks = [text]
            if len(text.split()) > MAX_WORDS:
                sentences = re.split(r"(?<=[.!?])\s+", text)
                chunks, cur = [], []
                for sent in sentences:
                    if cur and len(" ".join(cur + [sent]).split()) > MAX_WORDS:
                        chunks.append(" ".join(cur)); cur = []
                    cur.append(sent)
                if cur: chunks.append(" ".join(cur))
            for k, chunk in enumerate(chunks):
                n += 1
                beats.append({"id": f"S{sec['n']:02d}-B{n:02d}", "section": sec["n"], "section_title": sec["title"],
                              "written": chunk, "cues": cues if k == 0 else [], "code": code_blocks if k == 0 else [],
                              "continues": k > 0})
    return beats

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--show"); args = ap.parse_args()
    glossary = json.loads(GLOSSARY.read_text(encoding="utf-8"))
    beats = parse(SCRIPT.read_text(encoding="utf-8").split("\n"))
    for b in beats:
        b["spoken"] = decades(spoken_form(b["written"], glossary))
        b["words"] = len(b["written"].split())
        b["spoken_sha256"] = hashlib.sha256(b["spoken"].encode("utf-8")).hexdigest()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"source": "War/SCRIPT.md", "glossary": "spoken-glossary.v0.3", "max_words": MAX_WORDS, "min_words": MIN_WORDS,
                               "beats": beats}, indent=1, ensure_ascii=False) + LF, encoding="utf-8", newline=LF)
    if args.show:
        for b in beats:
            if b["id"].startswith(args.show):
                print(b["id"], b["words"], "words | cues:", len(b["cues"]), "| code:", len(b["code"])); print("  ", b["spoken"][:400]); print()
    words = sum(b["words"] for b in beats)
    print(f"beats {len(beats)}, words {words}, longest {max(b['words'] for b in beats)}, shortest {min(b['words'] for b in beats)}, ~{words/150:.0f} min at 150 wpm")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
