# XTRA-05 — Source excerpts

Access date for all external material: 2026-09-15 (UTC). Web quotes are kept short; each is attributed to its page.

## 1. Pack input (verbatim, hash-locked `sources/`)

`sources/SCRIPT.md` (sha256 `3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb`), lines 130–134:

~~~~text
**[VISUAL: Side-by-side — the VB4 IDE with labeled callouts: Form Designer, Toolbox, Properties Window, Code Window, Project Explorer.]**

This IDE had a few key pieces. On the left, you had a toolbox — a vertical strip of icons for things like buttons, text boxes, labels, picture boxes, timers, scroll bars. In the center was your form — a blank gray window that you designed visually. On the right was the properties panel, where you could set things like the caption on a button or the font size of a label. And behind all of it was the code window, where you wrote your actual BASIC.

This was called "RAD" — Rapid Application Development. The whole point was speed. You weren't writing code to create a window. The IDE did that for you. You were writing code to respond to events — a button click, a timer tick, a key press.
~~~~

Ticket copy (manifest `copy`, used verbatim as the labels):

~~~~text
Form Designer
Toolbox
Properties Window
Code Window
Project Explorer
~~~~

## 2. Working script (read only, `War/SCRIPT.md` on main 9e6f14a), lines 133–137

~~~~text
**[VISUAL: Side-by-side — the VB4 IDE with labeled callouts: Form Designer, Toolbox, Properties Window, Code Window, Project Window.]**

This IDE had a few key pieces. On the left, you had a toolbox — a vertical strip of icons for things like buttons, text boxes, labels, picture boxes, timers, scroll bars. In the center was your form — a blank gray window that you designed visually. On the right was the properties panel, where you could set things like the caption on a button or the font size of a label. And behind all of it was the code window, where you wrote your actual BASIC.

This was called "RAD" — Rapid Application Development. The whole point was speed. You weren't writing code to create a window. The IDE did that for you. You were writing code to respond to events — a button click, a timer tick, a key press.
~~~~

Commit 9e6f14a ("Apply 6 HIST-sourced script corrections", Writing Lead batch) changed only the cue at line 133: "Project Explorer" became "Project Window". The narration is unchanged.

## 3. Editorial register (`docs/EDITORIAL_REGISTER.md`)

- **R03 — Classic-inspired VB.NET versus actual VB4.** Required handling: "Verify version-specific syntax, platform capabilities, and UI panel names before historical claims."
- **R14 — Per-image licensing, archive capture, and public availability.** Required handling: record the rights holder, terms, access method and credit; unknown rights stay blocked.

## 4. Upstream original (HIST-02), text visible in the screenshot

Transcribed in HIST-02 `evidence/source-excerpts.md` §3 and re-read here at native size and at 1.5x:

- Title bar: `Loan - Microsoft Visual Basic [design]`
- Untitled tool window at the left edge with control icons (pointer, PictureBox, Label "A", TextBox "ab|", Frame, CommandButton, CheckBox, OptionButton, ComboBox, ListBox, scroll bars, Timer, drive/dir/file lists, Shape, Line, Image, Data, OLE, Grid)
- Form window title `LoanSheet`, menu `Options  Down Payment  Loan Length`, design grid dots, a selected grid control with sizing handles
- Project window title `Loan`, buttons `View Form`, `View Code`, entry `LOAN.FRM  LoanSheet`
- Properties window title `Properties - LoanSheet`, object `grdPayments Grid`
- Code window title `LoanSheet`, `Object: grdPayments`, `Proc: Click`, first line `Private Sub grdPayments_Click()`

## 5. Rights record carried forward (HIST-02 `evidence/rights.json`, `evidence/source.json`)

- `rights_status`: `unresolved`; `credit_text`: `null`.
- `proposed_credit_text`: "Microsoft Visual Basic 4.0 (32-bit) screenshot via WinWorld, winworldpc.com. Used with permission from Microsoft."
- `proposed_credit_notes` (source.json): the Microsoft sentence is correct only if the rights review relies on Microsoft's screenshot permission and "must not be used before that decision".
- Microsoft screenshot conditions quoted upstream: "Do not alter the screenshot except to resize it." and "Do not use portions of screenshots."

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
