# HIST-18 — source excerpts

## Production inputs (read-only `sources/`, unchanged)

### `sources/ASSET_PLAN.md` line 100 (sha256 `8f1769aacb6f446a00cdb72655a60475f7fa692b2f274effe3c517d33c20eef7`)

~~~~text
| 12 | TUCOWS / Download.com circa 1996 | Wayback Machine (web.archive.org) — no login needed | High — Wayback Machine is publicly accessible |
~~~~

### `sources/SCRIPT.md` lines 595–597 (sha256 `3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb`)

~~~~text
**[VISUAL: Screenshots of shareware download sites — TUCOWS, Download.com circa 1996, maybe a BBS file listing.]**

You'd distribute your game by uploading it to a BBS or a shareware site. Users would download it, but they'd also need the VB runtime — a DLL file called something like `VBRUN300.DLL` that shipped separately from your program. If the user didn't already have it installed, your game wouldn't launch. So a lot of shareware authors would bundle the runtime with their download, which turned a 200-kilobyte game into a 1.5-megabyte download. On a 14.4 modem, that's nearly ten minutes of downloading. For a card game.
~~~~

## External evidence: identity and date lines in the acquired original

From `source/original.html` (Wayback `id_` record of `http://www.download.com:80/`, capture 19961221110042). Quoted as short identifying lines only; the full file is preserved byte-for-byte.

- Line 1 server comment: `<!-- c|net Sat Dec 21 02:03:11 1996  $Revision: 2.7 $  -->`
- Title: `<title>DOWNLOAD.COM -- Welcome</title>`
- Head comment: `<!-- ( 1.25 ) Copyright (C) 1996 CNET Inc. All rights reserved. -->`
- Footer (rendered): `Copyright© 1996 CNET Inc. All rights reserved.` and `CNET disclaims any responsibility for software obtained through this site.`
- A template-change comment dated 25-Oct-1996 also appears in the head (it names a CNET staff member; not reproduced here and not visible in the render).

## External evidence: archive response headers (see `evidence/wayback-response-headers.txt`)

- `memento-datetime: Sat, 21 Dec 1996 11:00:42 GMT`
- `x-archive-orig-date: Saturday, 21-Dec-96 11:00:47 GMT`
- `x-archive-orig-server: Netscape-Communications/1.12`
- `x-archive-src: INA-HISTORICAL-2007-GROUP-KUR-20100812000000-00000-c/INA-HISTORICAL-EMBEDS-1996-GROUP-AAA-20100812000000-00000.arc.gz`

## External evidence: rights terms of the host archive (accessed 2026-09-15)

- Internet Archive Help Center, "Rights" (https://help.archive.org/help/rights/): the Archive states it "does not make guarantees as to the copyright status of items on archive.org".
- Internet Archive Terms of Use (https://archive.org/about/terms.php; wording as quoted in the Archive's 2014-12-30 announcement https://blog.archive.org/2014/12/30/update-to-terms-of-use/): users certify their use of the Collections "will be limited to noninfringing or fair use under copyright law." The live terms page is script-rendered and could not be text-extracted here; the current wording was not independently re-read.
