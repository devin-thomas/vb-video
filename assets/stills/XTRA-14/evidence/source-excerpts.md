# XTRA-14 source excerpts

## SCRIPT.md:685–687

Hash-locked original `sources/SCRIPT.md` (SHA-256 `3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb`). The working script `War/SCRIPT.md` carries the same three lines, character for character, at lines 742–744 (checked 2026-09-15 against `main` at 5e1825e). Neither file was edited by this ticket.

```text
That's not hyperbole. Before VB, writing a Windows application was a professional skill that required significant training. After VB, a motivated person with a $100 software purchase and a library book could build something real in a weekend. Accountants wrote tools to automate their spreadsheets. Teachers built quiz applications. Small business owners made inventory trackers. None of these people would have called themselves programmers. They were people with problems who discovered that Visual Basic was good enough to solve them.

**[VISUAL: Collage of real-world VB applications — maybe screenshots from old forums or software archives. Internal business tools, data entry forms, simple utilities.]**
```

## Exact panel copy (ticket XTRA-14, "Exact copy / source payload")

```text
Business tools · Data entry · Utilities
```

On screen, each of the three phrases labels one panel, in ticket order. The separator dots are not drawn. `src/build.py` asserts that the labels joined with " · " equal the manifest copy.

## Upstream credit records (verbatim; the source of every on-screen credit)

**XTRA-11**, `assets/historical/XTRA-11/evidence/rights.json`, field `credit_text`:

> INVOICE-IT for Windows (Eastern Digital Resources, 1993). Screenshot: Internet Archive Software Library, item MEDLEY_SEC90034.

On screen: "INVOICE-IT for Windows (Eastern Digital Resources)." / "Screenshot: Internet Archive Software Library, item MEDLEY_SEC90034." The software year is left off screen so the panel is not read as a 1993 capture; see claim check D1.

**XTRA-12**, `assets/historical/XTRA-12/evidence/rights.json`, field `credit_text`:

> Microsoft Corporation, "Developing Applications with the Microsoft Visual Basic 6.0 Data Object Wizard," Figure 16 (December 1998). Used with permission from Microsoft.

On screen: verbatim, with "Used with permission from Microsoft." on its own line. The upstream `credit_text_note` says that clause is correct only if the reviewer accepts that Microsoft's screenshot guidelines apply (XTRA-12-RQ1).

**XTRA-13**, `assets/historical/XTRA-13/evidence/rights.json`, field `credit_text_proposed` (`credit_text_approved` is null):

> Karen's Window Watcher (Visual Basic 6), screenshot © Karen Kenworthy, karenware.com — via Internet Archive Wayback Machine

On screen: verbatim.

## Upstream VB-provenance statements re-read for requirement 1

These are short quotations from the upstream evidence files, re-read on 2026-09-15. They are not reproduced in the artwork.

- **XTRA-11** (`evidence/source-excerpts.md`, publisher's 1993 RELEASE.TXT and MANUAL.WRI in the archived distribution): "Recompiled program using Visual BASIC 2.0"; the installation section requires "the Visual BASIC runtime library, VBRUN200.DLL".
- **XTRA-12** (`evidence/source-excerpts.md` and `evidence/source.json`, Microsoft article page): title "Developing Applications with the Microsoft Visual Basic 6.0 Data Object Wizard"; lead-in "A DOW-generated Single Record User Control:"; caption "Figure 16. Single Record User Control".
- **XTRA-13** (`evidence/source-excerpts.md`; stored Wayback captures under `evidence/captures/`): download page "You'll also find the program's Visual Basic 6.0 source code"; 2003 page "Visual Basic Runtime v6.0 — Required to install and run Window Watcher". The screenshot's own detail pane reads "MSVBVM60.DLL" and "ThunderRT6CommandButton". A case-insensitive search of the stored capture HTML found "Visual Basic Runtime" / "VB6 source" / "Visual Basic 6" in 3 of the 7 capture files (8 matches).

## Dates visible inside the source pixels (not captions)

- XTRA-11: the form's Date field reads "02-27-2016", the emulator clock on the Internet Archive capture day (upstream `evidence/claim-checks.json`, R11 era check).
- XTRA-13: the status bar reads "9/3/2003" (upstream `qa.md`); the image was archived by the Wayback Machine on 2003-09-17.
