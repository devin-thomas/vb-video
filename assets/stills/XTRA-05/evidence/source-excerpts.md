# XTRA-05 — Source excerpts

Access date for all external material: 2026-09-15 (UTC). Web quotes are kept short; each is attributed to its page. Nothing external was copied into the repository: URLs, short quotes and SHA-256 hashes of fetched pages only.

## 1. Pack input (verbatim, hash-locked `sources/`)

`sources/SCRIPT.md` (sha256 `3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb`), lines 130–134:

~~~~text
**[VISUAL: Side-by-side — the VB4 IDE with labeled callouts: Form Designer, Toolbox, Properties Window, Code Window, Project Explorer.]**

This IDE had a few key pieces. On the left, you had a toolbox — a vertical strip of icons for things like buttons, text boxes, labels, picture boxes, timers, scroll bars. In the center was your form — a blank gray window that you designed visually. On the right was the properties panel, where you could set things like the caption on a button or the font size of a label. And behind all of it was the code window, where you wrote your actual BASIC.

This was called "RAD" — Rapid Application Development. The whole point was speed. You weren't writing code to create a window. The IDE did that for you. You were writing code to respond to events — a button click, a timer tick, a key press.
~~~~

Ticket copy (manifest `copy`, the ticket's exact-copy payload). **Overridden for the fifth label** by the working script (§2), per Devin's 2026-09-15 ruling (writing change):

~~~~text
Form Designer
Toolbox
Properties Window
Code Window
Project Explorer
~~~~

## 2. Working script — label authority (read only, `War/SCRIPT.md` on main 9e6f14a), lines 133–137

~~~~text
**[VISUAL: Side-by-side — the VB4 IDE with labeled callouts: Form Designer, Toolbox, Properties Window, Code Window, Project Window.]**

This IDE had a few key pieces. On the left, you had a toolbox — a vertical strip of icons for things like buttons, text boxes, labels, picture boxes, timers, scroll bars. In the center was your form — a blank gray window that you designed visually. On the right was the properties panel, where you could set things like the caption on a button or the font size of a label. And behind all of it was the code window, where you wrote your actual BASIC.

This was called "RAD" — Rapid Application Development. The whole point was speed. You weren't writing code to create a window. The IDE did that for you. You were writing code to respond to events — a button click, a timer tick, a key press.
~~~~

Commit 9e6f14a ("Apply 6 HIST-sourced script corrections", Writing Lead batch) changed only the cue at line 133: "Project Explorer" became "Project Window". The narration is unchanged. `src/build.py` reads the five labels from this cue line at build time (the one line containing "VB4 IDE with labeled callouts"), asserts there are exactly five and that each still names its panel in cue order, and records the line, text and the file's SHA-256 in `src/layout.json`. Rendered labels: Form Designer, Toolbox, Properties Window, Code Window, Project Window.

## 3. Editorial register (`docs/EDITORIAL_REGISTER.md`)

- **R03 — Classic-inspired VB.NET versus actual VB4.** Required handling: "Verify version-specific syntax, platform capabilities, and UI panel names before historical claims."
- **R14 — Per-image licensing, archive capture, and public availability.** Required handling: record the rights holder, terms, access method and credit; unknown rights stay blocked.

## 4. Upstream original (HIST-02), text visible in the screenshot

Transcribed in HIST-02 `evidence/source-excerpts.md` §3 and re-read here at native size, at 1.5x and at 1.0x:

- Title bar: `Loan - Microsoft Visual Basic [design]`
- Untitled tool window at the left edge with control icons (pointer, PictureBox, Label "A", TextBox "ab|", Frame, CommandButton, CheckBox, OptionButton, ComboBox, ListBox, scroll bars, Timer, drive/dir/file lists, Shape, Line, Image, Data, OLE, Grid)
- Form window title `LoanSheet`, menu `Options  Down Payment  Loan Length`, frames `Years in Loan`, `Interest Rates`, buttons `Show Paymen…`, `Show Amortiza…` (cut off by the Code window), design grid dots, a selected grid control with sizing handles
- Project window title `Loan`, buttons `View Form`, `View Code`, entry `LOAN.FRM  LoanSheet`
- Properties window title `Properties - LoanSheet`, object `grdPayments Grid`
- Code window title `LoanSheet`, `Object: grdPayments`, `Proc: Click`, first line `Private Sub grdPayments_Click()`, `cmdCalcAmort.Enabled = True`

## 5. Rights record carried forward (HIST-02 `evidence/rights.json`, `evidence/source.json`)

- `rights_status`: `unresolved`; `credit_text`: `null`.
- `proposed_credit_text`: "Microsoft Visual Basic 4.0 (32-bit) screenshot via WinWorld, winworldpc.com. Used with permission from Microsoft."
- `proposed_credit_notes` (source.json): the Microsoft sentence is correct only if the rights review relies on Microsoft's screenshot permission and "must not be used before that decision".
- Microsoft screenshot conditions quoted upstream: "Do not alter the screenshot except to resize it." and "Do not use portions of screenshots."
- Devin, 2026-09-15: callout marks over the whole screenshot are allowed (XTRA-05-RQ1, carries RQ-HIST-02-3). The permission basis itself (RQ-HIST-02-1) is still undecided.

## 6. Panel-name evidence (Microsoft Knowledge Base, archived copies at jeffpar.github.io/kbarchive)

| Article | Applies to (as listed) | Last modified | Short quote |
|---|---|---|---|
| [Q140350](https://jeffpar.github.io/kbarchive/kb/140/Q140350/) "Deleting .frx File Causes Visual Basic to Exit Abnormally" | VB 4.0 Standard, Professional, Enterprise, 32-bit only | 11-JAN-2001 | "Open Form1, by double-clicking it in the Project window." |
| [Q136399](https://jeffpar.github.io/kbarchive/kb/136/Q136399/) "INFO: Visual Basic and Source Code Control Glyphs" | Visual SourceSafe 4.0, 5.0, 6.0 | 07-DEC-2001 | "In Visual Basic, the Project window displays a list of all the form modules" |
| [Q154885](https://jeffpar.github.io/kbarchive/kb/154/Q154885/) "PRB: Tabbing Problem When Sheridan SSTab Control Hosts OCXs" | VB 4.0 (16- and 32-bit editions), VB 5.0, 6.0 | 19-FEB-2002 | "If the SSTab control does not appear in the toolbox" |
| [Q169772](https://jeffpar.github.io/kbarchive/kb/169/Q169772/) | VB 4.0 32-bit editions, VB 5.0, 6.0 | 11-JAN-2001 | Title: "PRB: VB5 .OCX Property Missing from VB4 Properties Window" |
| [Q161344](https://jeffpar.github.io/kbarchive/kb/161/Q161344/) "INFO: Visual Basic 4.0 and Visual Basic 5.0 Compatibility" | VB 4.0 32-bit editions, VB 5.0 | 20-FEB-2002 | "The VB4 Properties window will only display control properties that are passed by value." |
| [Q216146](https://jeffpar.github.io/kbarchive/kb/216/Q216146/) "HOWTO: Get Number of Windows NT Event Log Records in Visual Basic" | VB 4.0 32-bit editions, VB 5.0, 6.0 | 11-JAN-2001 | "Add the following code to the Form1 code window:" |

Later-version terminology, Microsoft Visual Basic 6.0 documentation (archived on Microsoft Learn):

- [Integrated Development Environment Elements](https://learn.microsoft.com/en-us/previous-versions/visualstudio/visual-basic-6/aa242109(v=vs.60)) (ms.prod visual-basic-6): section headings include "Toolbox", "Project Explorer Window", "Properties Window", "Form Designer" and "Code Editor Window".
- [Using the Code Editor](https://learn.microsoft.com/en-us/previous-versions/visualstudio/visual-basic-6/aa231233(v=vs.60)) (visual-basic-6): refers readers to "Code Window Keyboard Shortcuts".

Not found: no VB 4.0-applicable Microsoft document using "Project Explorer" or "Form Designer" turned up in the searches. Q150423 (VB 4.0a fixes) and Q142823 (VB Programmer's Guide to Visual SourceSafe, VB 4.0) contain none of the panel names. A web search summary claimed Microsoft renamed the Project window to Project Explorer between versions 4 and 5; the thread it pointed to (microsoft.public.vb.general.discussion, "Project Window", narkive) contains no such statement, so the claim is not used.

## 7. Authorship of the "Loan" project (XTRA-05-RQ5, carries RQ-HIST-02-2)

**Conclusion: Microsoft sample.** The project in the capture is the Visual Basic 4.0 Grid sample (`\vb\samples\grid\loan.vbp`, `loan.frm`, `loan.frx`). Full record with hashes: `evidence/claim-checks.json` → `loan_project_research`.

| # | Source (accessed 2026-09-15) | Short quote / listing row | What it establishes |
|---|---|---|---|
| 1 | Microsoft KB [Q150726](https://jeffpar.github.io/kbarchive/kb/150/Q150726/) "INFO: Files Installed with All Editions of Visual Basic 4.0" (VB 4.0 Standard/Professional/Enterprise 32-bit; last modified 11-JAN-2001). Page sha256 `7de9ec92…6e5830`. | Section "F. Samples", "1. All Editions": `loan.frm*  \vb\samples\grid`, `loan.frx*  \vb\samples\grid`, `loan.vbp*  \vb\samples\grid`. Footnote: files "marked with an asterisk (*)" are also installed on a 16-bit platform. | Microsoft lists the Loan project as a sample installed into VB\SAMPLES\GRID by every VB 4.0 edition. Primary evidence. |
| 2 | archive.org [microsoft-visual-basic-4.0-enterprise](https://archive.org/details/microsoft-visual-basic-4.0-enterprise), disc contents listing page (not the ISO). Page sha256 `cf675658…f229bd`. | `VB/SAMPLES/GRID/LOAN.FRM 1996-01-12 31035`; `LOAN.FRX 2336`; `LOAN.VBP 382` | The files are on a VB 4.0 Enterprise CD beside `VB/SAMPLES/SAMPLES.HLP`. |
| 3 | archive.org [Microsoft_Visual_Basic_Enterprise_Edition_Version_4.0_Microsoft_1995](https://archive.org/details/Microsoft_Visual_Basic_Enterprise_Edition_Version_4.0_Microsoft_1995), disc contents listing page. Page sha256 `d3a3f80a…ca0040`. | `VB/SAMPLES/GRID/LOAN.FRM 1995-08-15 31035`; `LOAN.FRX 2336`; `LOAN.VBP 382` | An August 1995 pressing carries the same files at identical sizes. |
| 4 | archive.org [microsoft-visual-basic-4.0-professional-4.00.2422-english-cd](https://archive.org/details/microsoft-visual-basic-4.0-professional-4.00.2422-english-cd), `en_vb40A_pro.iso` contents listing page. Page sha256 `14b99b0c…3e3811`. | `vb/samples/grid/LOAN.FRM 1996-01-11 31035`; `LOAN.FRX 2336`; `LOAN.VBP 382` | The Professional edition (4.0a) has it too, not only Enterprise. |
| 5 | The capture (HIST-02 `source/original.png`) | `Loan - Microsoft Visual Basic [design]`; `LOAN.FRM  LoanSheet`; `grdPayments Grid` | Project named Loan, form file LOAN.FRM, a Grid control: matches the Grid sample. |
| 6 | KB [Q153838](https://jeffpar.github.io/kbarchive/kb/153/Q153838/) (page sha256 `4d40c375…3408c5`) | no "loan" text | Search false positive. |
| 7 | KB [Q173840](https://jeffpar.github.io/kbarchive/kb/173/Q173840/) (page sha256 `452e9c1c…db4d26`) | no "loan" text | Search false positive (no third-party book project named Loan). |
| 8 | 16 web searches (queries listed in claim-checks) for LOAN.VBP / LOAN.MAK / LOAN.FRM, grdPayments, cmdCalcAmort, LoanSheet, `samples\grid`, VB4 sample listings | — | Found sources 1–4; no attribution of a Loan / LoanSheet project to anyone but Microsoft. No VB3 LOAN.MAK listing found. |

Limit: the text of LOAN.FRM was not compared with the capture's form (LoanSheet, grdPayments, cmdCalcAmort, menus), because that would mean extracting a file from a disc image; that was not done. Effect: no third-party content concern remains, but release still depends on Microsoft's permission basis (RQ-HIST-02-1).

Method: read-only HTTPS GETs of HTML pages (KB articles, archive.org metadata and directory listings) with a generic browser User-Agent into the worker scratchpad; no accounts, no terms, no borrow-gated books, no installers, disc images or files from inside disc images.
