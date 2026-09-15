# XTRA-20 source excerpts

## Script request (sources/SCRIPT.md:595–597, unchanged)

~~~~text
**[VISUAL: Screenshots of shareware download sites — TUCOWS, Download.com circa 1996, maybe a BBS file listing.]**

You'd distribute your game by uploading it to a BBS or a shareware site. Users would download it, but they'd also need the VB runtime — a DLL file called something like `VBRUN300.DLL` that shipped separately from your program. If the user didn't already have it installed, your game wouldn't launch. So a lot of shareware authors would bundle the runtime with their download, which turned a 200-kilobyte game into a 1.5-megabyte download. On a 14.4 modem, that's nearly ten minutes of downloading. For a card game.
~~~~

The working script, War/SCRIPT.md:652–654, has the same text.

## Archived listing lines used in the frame

Decoded from CP437 in source/original.txt (SHA-256 883c34aefc363c4acaa5b1db9586e446b69fb9961935b70a666799ce6b875bc2). Numbers are 1-based source line numbers. Trailing spaces are not shown here, but the rendering keeps them.

~~~~text
 541       █▓▒░█▓▒░█▓▒░█▓▒░ THE ACCESS SYSTEM - HUNTSVILLE, AL ░▒▓█░▒▓█░▒▓█░▒▓█
 542
 543                  Catalog of Files by Subject as of : 09/09/1992
 544
 545                        Main Board Directory 04 - Games!
 546
 547 File Name        Size    Date     D e s c r i p t i o n
 548 ================================================================================
     [549–585 not shown]
 586 TRSK.ZIP         8597  08-22-88  EGA Puzzel - Triskelion Rings ..........
 587 ULTRAQIZ.ZIP    62986  07-18-92  Deduce answers from hints provided
 588 UWDEMO.ZIP    1197223  03-31-92  A playable demo of the UnderWorld Adventure
 589                                  Game.  Requires a 286 or better.
 590                                  3 files - New:03/10/1992  Old:01/21/1992
 591 VBRUN.ZIP      169469  06-09-92  The Dynamic Link Library required to run any
 592                                  compiled Visual Basic program.
 593 VGATRON.ZIP     66538  08-05-92  VGA  Laser Beam Chase Game  (Check it out)
 594 VPOKER.ZIP     171568  12-23-90  Vol 9 no 4 PC Mag games with source
 595 VSHARKS1.ZIP   148309  06-11-91  Good VGA game;avoid sharks get fish
 596 W3DXLV11.ZIP    22634  09-04-92  Exciting new level for Wolfenstein 3-D demo
 597                                  version. (make your own with MAPED41.ZIP)
 598 ================================================================================
 599 File listing created with WGM-DMS v.3.5.                             Page   10
~~~~

## Corroborating excerpts (not stored as media)

- access.old (same board, catalog as of 07/20/1992), line 496: `VBRUN.ZIP      169469  06-09-92  The Dynamic Link Library required to run any`
- southexp.lst (Southern Express BBS, 1992), lines 3410–3412: `VBRUN100.ZIP   169480  06-23-91  Microsoft's visual basic runtime. Download` / `| this and save the trouble of including it in` / `| all uploads and downloads in V.B. programs`
- Microsoft KB Q99251: fixed VBRUN300.DLL, 12-MAY-1993, 398416 bytes, version 03.00.0538.
- Microsoft KB Q196286: Vb40016.dll 913KB; Vb40032.dll 705KB.

## Search record (2026-09-15)

1. textfiles.com/bbs/FILELISTS/ has 32 captured board listings (1989–1994). I downloaded 25 of these text files and grepped them for "vbrun"; VBRUN300 appeared in none. Runtime hits: mbfile.txt 18 (VBRUN100; dated 03/15/93; board not named in file), southexp.lst 11 (VBRUN100), allfile3.txt 11 (VBRUN100), allfiles.lst 4 (VBRUN100/VBRUN_X, 1992–93), owlabama.lst 2 (VBRUN100, VBRUN2), rocktcty.lst 2 (VBRUN100), access.lst 1, north444.lst 1. The rest had none: buzzardsnest4.txt (1994), cybahq.lst (1993), fuzzylogic.txt (c.1994), totselist.txt (1993), tdrfiles.txt, 170-609.asc, ajfafile.txt, allfile1/2.txt, asblist.txt, bbsfiles.cat, filelist.txt, filelst.txt, sysop.txt, totlist.txt, wfobbs.lst, liberty.txt. Not downloaded: catalog.6, filearea.txt, files.bbs, mastlist.txt (same size as rocktcty.lst), snakepit.dld.txt, spacelnk.lst. These are pre-1993 or text-file-only, and none is likely to hold VBRUN300.
2. access.lst was chosen because its board name and catalog date appear in the file itself on every page, a Wayback capture confirms it byte-for-byte, and a separately dated earlier catalog from the same board corroborates its runtime entry.
3. VBRUN300 does appear in discmaster.textfiles.com FILES.BBS listings on shareware CD-ROMs: Software Vault: The Collection for Windows 2 (1994-12-08) and The Arsenal Files 3 (1995-02-03). These are CD-ROM directory listings, not board listings, so neither was used.
