# HIST-17 source excerpts

## Production sources (hash-locked, unchanged)

`sources/ASSET_PLAN.md` line 100 (sha256 8f1769aacb6f446a00cdb72655a60475f7fa692b2f274effe3c517d33c20eef7):

~~~~text
| 12 | TUCOWS / Download.com circa 1996 | Wayback Machine (web.archive.org) — no login needed | High — Wayback Machine is publicly accessible |
~~~~

`sources/SCRIPT.md` lines 595–597 (sha256 3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb). The same cue is at `War/SCRIPT.md` line 652 in the working script.

~~~~text
**[VISUAL: Screenshots of shareware download sites — TUCOWS, Download.com circa 1996, maybe a BBS file listing.]**

You'd distribute your game by uploading it to a BBS or a shareware site. Users would download it, but they'd also need the VB runtime — a DLL file called something like `VBRUN300.DLL` that shipped separately from your program. If the user didn't already have it installed, your game wouldn't launch. So a lot of shareware authors would bundle the runtime with their download, which turned a 200-kilobyte game into a 1.5-megabyte download. On a 14.4 modem, that's nearly ten minutes of downloading. For a card game.
~~~~

## External evidence: the archived page (`source/original.html`)

Wayback Machine capture `19961022175612` of `http://www.tucows.com:80/`, retrieved in `id_` mode (bytes as archived). Memento-Datetime: Tue, 22 Oct 1996 17:56:12 GMT. Relevant lines, verbatim (the © sign is stored as byte 0xA9, Latin-1):

~~~~html
<title>The Ultimate Collection of Winsock Software</title>
<LINK rev=made href="mailto:helpdesk@tucows.com">
<img src="images/Logo.gif"><br>
<font size="+2" color="#ff0000">For fastest service, select one of the locations closest to you 
<A HREF="http://www.connectsoft.com/corp/products/emc/tucows">
<IMG SRC="images/adds/cs_ad.gif"></A>
<font size = "+3"><i><font size="+2" color="blue"><b>Primary TUCOWS Mirrors</font></b></i></font><br>
Copyright © 1996 Scott A. Swedorski<p>Tucows Limited has no liability for 
any content or goods on the Tucows site or the Internet, except as set 
forth in the <a href="http://tucows.idirect.com/warn.html">terms and 
conditions</a>
~~~~

## Comparison capture (`source/raw/comparison-19961228134206.html`)

The same URL on 28 Dec 1996 has a different page with title `TUCOWS World Wide Mirror Site Locations` and the footer `Copyright © 1996 TUCOWS Ltd.` It is kept to show that the footer's named rights holder changed within 1996.

## Alternate candidates

`source/candidates/B-idirect-19961230/original.html` is the mirror `http://tucows.idirect.com:80/`, capture `19961230051406`, titled `Welcome to TUCOWS`. Verbatim strings: `Software Listings for:`, `SHAREWARE CENTER`, `SOFTWARE <I>COW</I>NOISSEUR!`. It has no copyright footer.

`source/candidates/C-phoenix-win95oct96-19961117/original.html` is the mirror `http://tucows.phoenix.net:80/archive/win95oct96.html`, capture `19961117161725`, titled `Windows 95 New Software`. Its footer reads `Copyright © 1996 ComputerLink OnLine Inc.`

## Internet Archive terms (access terms, not a content licence)

Wayback capture `20170103040112` of `http://archive.org/about/terms.php`. The current `https://archive.org/about/terms` page loads as a JavaScript app, and no terms text could be extracted from it on 2026-09-15. Verbatim sentence:

> Access to the Archive’s Collections is provided at no cost to you and is granted for scholarship and research purposes only.
