# HIST-02 — Source excerpts

Access date for all external material: 2026-09-15 (UTC). Local copies of the pages quoted below are in `evidence/pages/` with SHA-256 in `evidence/provenance.json`.

## 1. Pack inputs (verbatim, hash-locked `sources/`)

`sources/SCRIPT.md` (sha256 `3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb`), line 49:

~~~~text
**[VISUAL: Magazine covers — Visual Basic Programmer's Journal, old MSDN ads, screenshots of the VB4 IDE.]**
~~~~

`sources/SCRIPT.md`, lines 130–134:

~~~~text
**[VISUAL: Side-by-side — the VB4 IDE with labeled callouts: Form Designer, Toolbox, Properties Window, Code Window, Project Explorer.]**

This IDE had a few key pieces. On the left, you had a toolbox — a vertical strip of icons for things like buttons, text boxes, labels, picture boxes, timers, scroll bars. In the center was your form — a blank gray window that you designed visually. On the right was the properties panel, where you could set things like the caption on a button or the font size of a label. And behind all of it was the code window, where you wrote your actual BASIC.

This was called "RAD" — Rapid Application Development. The whole point was speed. You weren't writing code to create a window. The IDE did that for you. You were writing code to respond to events — a button click, a timer tick, a key press.
~~~~

`sources/ASSET_PLAN.md` (sha256 `8f1769aacb6f446a00cdb72655a60475f7fa692b2f274effe3c517d33c20eef7`), line 89:

~~~~text
| 1 | VB 1.0 / VB 4.0 / VB 6.0 IDE screenshots | Wikipedia "Visual Basic" article, Wikimedia Commons | High — these exist on Wikipedia |
~~~~

## 2. Acquired original — host labels (WinWorld)

Page: https://winworldpc.com/product/microsoft-visual-bas/40 (local copy `evidence/pages/winworldpc-product-microsoft-visual-bas-40.html`).

- Screenshot caption / alt text of the acquired file: `Microsoft Visual Basic 4.0 32 bit - Edit`
- Sibling screenshots on the same page: `Microsoft Visual Basic 4.0 32 bit - About`, `Microsoft Visual Basic 4.0 16 bit - Edit`, `Microsoft Visual Basic 4.0 16 bit - About`
- Release notes line (short quote): "the first version that could create 32-bit executables for Windows NT and 95."
- Product facts listed: vendor Microsoft; release date 1995.

## 3. Identity evidence read from images (transcribed by the worker)

Acquired file `source/original.png` (800×600), visible text:

- Title bar: `Loan - Microsoft Visual Basic [design]`
- Menu bar: `File Edit View Insert Run Tools Add-Ins Help`
- Project window titled `Loan`, buttons `View Form` / `View Code`, entry `LOAN.FRM  LoanSheet`
- Properties window title: `Properties - LoanSheet`, object `grdPayments Grid`
- Code window title `LoanSheet`, `Object: grdPayments`, `Proc: Click`, first line `Private Sub grdPayments_Click()`
- Windows 95 taskbar: `Start`, task button `Loan - Microsoft Visual Ba...`, clock `10:43 PM`

Sibling file `Microsoft Visual Basic 4.0 32 bit - About` (not committed because it displays a product serial number; URL and hash in `evidence/source.json`), visible text:

- Dialog `About Microsoft Visual Basic`: `Microsoft Visual Basic Version 4.0` / `For 32-bit Windows Development` / `Copyright © 1987-1995 Microsoft Corp.`
- Same Windows 95 shell, same IDE window arrangement (toolbox left, Project window top right, Properties window bottom right), clock `10:41 PM`.

Sibling file `Microsoft Visual Basic 4.0 16 bit - About` (not committed): `Microsoft Visual Basic Version 4.0` / `For 16-bit Windows Development`, shown on a Windows 3.1 shell (Program Manager / File Manager icons).

## 4. Rights terms (short quotes)

WinWorld copyright page, https://winworldpc.com/copyright (local copy `evidence/pages/winworldpc-copyright.html`): the page licenses library descriptions under CC BY-SA 4.0 and the site software under AGPL 3.0; it states no license for screenshots.

Microsoft, "Use of Microsoft Copyrighted Content", https://www.microsoft.com/en-us/legal/intellectualproperty/copyright/permissions (local copy `evidence/pages/microsoft-copyright-permissions.html`). Screenshot conditions as published (list items, verbatim):

- "Do not alter the screenshot except to resize it."
- "Do not use portions of screenshots."
- "Do not include screenshots in your product user interface."
- "Do not use screenshots that contain third-party content."
- "Do not use screenshots that contain an image of an identifiable individual."

Required statement named on the same page: "Used with permission from Microsoft."

## 5. Terminology evidence (Project window)

Microsoft KnowledgeBase article Q136399, "INFO: Visual Basic and Source Code Control Glyphs", archived at https://jeffpar.github.io/kbarchive/kb/136/Q136399/ — see `evidence/claim-checks.json` for the quoted sentence and applicability.
