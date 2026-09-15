# XTRA-19 source excerpts

## Script cue (input)

`sources/SCRIPT.md:579–593` (read-only original, SHA-256 `3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb`). The cue line is `sources/SCRIPT.md:579`, which is the same text as `War/SCRIPT.md:636`:

~~~~text
**[VISUAL: Screenshots of 90s shareware card games — Solitaire, Hearts, FreeCell. Windows 3.1 and Windows 95 versions. The classic green felt background.]**
~~~~

The narration context in the same range includes this line (`sources/SCRIPT.md:593`, `War/SCRIPT.md:650`):

~~~~text
The shareware scene of the 1990s was full of card games, board games, and puzzle games written in Visual Basic. Windows came bundled with Solitaire and Minesweeper (written in C), but the thousands of freeware and shareware alternatives that flooded BBS boards and early web sites? A huge number of those were VB apps.
~~~~

This ticket fills only the FreeCell part of the cue. Solitaire belongs to another ticket, and Hearts belongs to XTRA-18.

## Selected image: hosting-page excerpts (external evidence)

The image comes from WinWorld (winworldpc.com), accessed 2026-09-15. These excerpts are text extracted from the public HTML with no login.

**Screenshot gallery** https://winworldpc.com/screenshot/c3b2c3af-c2b1-c3a0-4b62-11c3a4c28d58, titled "Screenshots for Microsoft Entertainment Pack 2". The gallery holds four images: About, Cards, Games and Life. The selected image's tag reads:

> `src="/res/img/screenshots/2-e0249a99db7492f217c030c559f6c27c-Microsoft Entertainment Pack 2 - Cards.png"` … `title="Microsoft Entertainment Pack 2 - Cards"`

**Detail page** https://winworldpc.com/screenshot/c3b2c3af-c2b1-c3a0-4b62-11c3a4c28d58/c2b3c2ab-c2a4-064b-c3b0-11c3a4c28d58 shows only the caption "Microsoft Entertainment Pack 2 - Cards". It names no contributor or capture date.

**Product page** https://winworldpc.com/product/microsoft-entertainm/2:

> Microsoft Entertainment Pack Volume 2 | Contains the games: Freecell, JigSawed, Pipe Dream, RattlerRace, Rodent's Revenge, Stones, and Tut's Tomb.

> This version is for Windows 3.0 and later.

> Release date | 1991

**Site copyright page** https://winworldpc.com/copyright:

> Under most interpretations of international copyright law, copyright is retained by the original publisher or a licensed distributor unless explicitly stated even if the software is considered 'abandoned'.

The site footer reads "© 2026 WinWorld". No page read states terms for screenshots.

## What the image itself shows (read from the pixels)

These readings were made at 1:1 and at 4× nearest-neighbour. They are not taken from a caption.

- Front window title: **"FreeCell Game #14601"**.
- Front window menu bar: **Game · Options · Help**, with **"Cards Left: 52"** at the right of the menu bar.
- Centre of the top row: the FreeCell king icon, between four empty free cells on the left and four empty home cells on the right.
- Behind it, a second window titled **"Tut's Tomb"** (another Entertainment Pack 2 game) with the menu **Game · Help** and a status line **"Time: 28"**.
- Bottom-left: a minimized **"File Manager"** icon on a grey desktop.
- Window chrome: Windows 3.x style. Each title bar is flat, with a system-menu box on the left and minimize/maximize arrow buttons on the right. There are no Windows 95 close (×) buttons and no bevelled 95-style captions. The active FreeCell title bar is dithered, which fits a 16-colour display. The image holds 13 distinct palette colours.
- The FreeCell window is sized smaller than its own card layout. Its right and bottom window borders are visible, and the columns are clipped inside the window. A mouse pointer shows near the home cells. That is how the capture was taken; this package crops nothing.
- The chrome alone cannot tell Windows 3.0 from Windows 3.1, and the pixels do not identify the FreeCell binary (Entertainment Pack 2, Best of, or Win32s). The Entertainment Pack 2 attribution comes from WinWorld's gallery context and the Tut's Tomb window, which is also a Pack 2 game.

## Background history sources (for claim checks)

- Microsoft Knowledge Base **Q106715**, "How to Troubleshoot Win32s Installation Problems". It applies to Win32s 1.25a, 1.30, 1.30a and 1.30c, and was last reviewed May 21, 1998. Mirror consulted: http://web.mit.edu/cascon/microsoft/q106715.htm, accessed 2026-09-15. It states:
  > The installation guide for Win32s that is included in the Win32 SDK recommends running Freecell to verify that the installation was successful.
- Michael Keller, "FreeCell - Frequently Asked Questions", Solitaire Laboratory, http://solitairelaboratory.com/fcfaq.html, accessed 2026-09-15. The page is undated. It says the Windows version first appeared on Microsoft Entertainment Pack 2 in 1992. It also says:
  > Later versions were bundled with Windows For Workgroups and Win32s (the 32-bit extension to Windows 3), and eventually with Windows 95 (and 98).
- Eli's Software Encyclopedia, "Microsoft Entertainment Pack Volume 2 (PC, 1.2MB 5 1/4" Disk) Microsoft - 1991 USA, Canada Release", accessed 2026-09-15. It lists FreeCell, dates the release 1991, and gives "PC Windows 3.1" as a requirement. This is a secondary catalogue entry.
- Internet Archive item `wep_best-of`, "Windows Entertainment Pack - Best of - Disk Image", accessed 2026-09-15. Its description reads "1994 release on a single 3.5" 1440K floppy disk" and "This includes the following games for Windows 3.x", and FreeCell is on the list. The uploader's `wep_best-of_screenshot-2.png` shows a German Windows 3.1 Program Manager with a "Free Cell" icon in a "Best of Entertainment" group. It was inspected but not copied into this package.
- Internet Archive item `Freecell_Windows`, "Freecell (Windows 9x)". The uploader's description (Italian) calls it the FreeCell v4.0.0.950 included in Italian Windows 95/98. The archive's listing of `Freecell.zip` shows `Freecell.EXE 1996-08-24 12:11 28736`. This is the rejected alternate candidate; see `evidence/provenance.json`.
