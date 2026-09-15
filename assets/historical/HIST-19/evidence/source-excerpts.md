# HIST-19 source excerpts

Two kinds of excerpt are kept apart here:

- **Literal project inputs** are copied byte-for-byte from `sources/`, which is hash-locked.
- **External evidence** is quoted only in short phrases and otherwise paraphrased, with exact locators. Access date for every external item: 2026-09-15.

## 1. Literal project inputs

### sources/ASSET_PLAN.md:101
SHA-256 of file: `8f1769aacb6f446a00cdb72655a60475f7fa692b2f274effe3c517d33c20eef7`

~~~~text
| 13 | Windows Solitaire (Win 3.1 / Win95) | Wikipedia "Microsoft Solitaire" | High |
~~~~

### sources/SCRIPT.md:579–593
SHA-256 of file: `3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb`

The same wording appears in `War/SCRIPT.md` at lines 636–650 (line numbers shifted; text unchanged).

~~~~text
**[VISUAL: Screenshots of 90s shareware card games — Solitaire, Hearts, FreeCell. Windows 3.1 and Windows 95 versions. The classic green felt background.]**

**NARRATION:**

Okay, so we've built a console War simulator. In 1995, what would have happened next?

You would have put a GUI on it.

This is where Visual Basic's form designer would have come in. You'd open the IDE, draw a form the size of a card table, drop some `PictureBox` controls on it to represent the card positions, maybe load bitmap images of playing cards from a resource file, and wire up the game logic to a Timer control that advanced the game one round at a time. You'd add a "Deal" button, a "Watch" button, maybe a speed slider.

**[VISUAL: Mockup of what a VB4 War GUI might look like — a green-felt form with card images, buttons along the bottom. Labeled: "This is what you'd build next."]**

And this is how a lot of actual software got made in the mid-90s. People would start with the logic — get the algorithms working in a console or a simple form — and then layer the visual design on top. Visual Basic made that second step dramatically easier than anything else available.

The shareware scene of the 1990s was full of card games, board games, and puzzle games written in Visual Basic. Windows came bundled with Solitaire and Minesweeper (written in C), but the thousands of freeware and shareware alternatives that flooded BBS boards and early web sites? A huge number of those were VB apps.
~~~~

## 2. External evidence

### 2.1 Acquired image — Internet Archive item `solitaire-windows-3.1`
- Item page: https://archive.org/details/solitaire-windows-3.1
- File: https://archive.org/download/solitaire-windows-3.1/Solitaire%20(Windows%203.1).png
- Metadata API: https://archive.org/metadata/solitaire-windows-3.1 (redacted copy: `evidence/source-page/item-record.json`)
- Fields recorded from the metadata:
  - title: "Solitaire"
  - creator: "Matthew Paul Argall"
  - date: 2025-05-03
  - publicdate/addeddate: 2025-05-17 08:38:19
  - subject: Screenshot; Solitaire
  - collection: `matthew-paul-argall-screenshots`
  - mediatype: image
  - The only original file is named `Solitaire (Windows 3.1).png`.
  - **No `licenseurl` or `rights` field is present.**
- Description, paraphrased: the uploader's personal goal is to win Solitaire on as many operating systems as possible.
- Archive checksums for the original file:
  - SHA-1 `d5f767d4c4d43020bb681035daf29e6ca2e6da0b`
  - MD5 `2ae802371d5d7529ce5bd62825a20b5d`
  - Both match the downloaded bytes.

### 2.2 Capturer's collection statement — Internet Archive collection `matthew-paul-argall-screenshots`
- Metadata API: https://archive.org/metadata/matthew-paul-argall-screenshots (redacted copy: `evidence/source-page/collection-record.json`)
- The collection summary covers screenshots the uploader took between 2006 and 2025. It opens "Feel free to do what you wish with these screenshots". It adds that the uploader prefers to be credited, and lists blogs, news sites and forums as example uses.
- This is an informal permission from the person who made the capture. It is not a named licence. It cannot grant rights in Microsoft's software UI or card artwork.

### 2.3 Microsoft's screenshot guideline — "Use of Microsoft copyrighted content"
- URL: https://www.microsoft.com/en-us/legal/intellectualproperty/permissions/default (no date shown on the page)
- Under "Screenshots", paraphrased:
  - Boot, splash and beta or unreleased screens are excluded.
  - Other screenshots may be used in videos and similar media, on these conditions:
    - The screenshot is not altered except by resizing.
    - Portions of screenshots are not used.
    - The screenshot is not placed in a product UI.
    - It contains no third-party content.
    - It contains no identifiable individuals.
- General requirements, paraphrased:
  - Use the full product name.
  - Make no disparaging use.
  - Include the statement "Used with permission from Microsoft."

### 2.4 Product identity context — Microsoft Windows User's Guide, version 3.1 (April 1992)
- Internet Archive (bitsavers): https://archive.org/details/bitsavers_microsoftwindows3.1PC216690492Windows3.1UsersGuide_27129713
- Document number PC21669-0492.
- OCR search results, paraphrased:
  - Printed p. 73 (scan leaf index 99) tells new users they can practise Windows skills with Solitaire or Minesweeper, which Setup copied to the hard disk.
  - Printed p. 540 (leaf 566) lists `SOL.EXE, SOL.HLP` as the Solitaire game and its Help text.
  - The index sends readers to Solitaire's online Help.
- The guide contains **no picture of the Solitaire playfield**, so it cannot serve as the image source.
- Comparison: the Windows 3.0 User's Guide (September 1989 printing; https://archive.org/details/bitsavers_microsoftwUsersGuide198909_23166485) names the two Windows 3.0 games as Solitaire and Reversi. Minesweeper does not appear there.
