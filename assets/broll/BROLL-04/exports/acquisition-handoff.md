# BROLL-04 acquisition handoff

Access date for all pages: 2026-09-15.

> **Update, 2026-09-15 (acquisition pass, branch `ticket/BROLL-04-media`).** Item 1 **has now been downloaded**, on Devin's approval of that single file. It is at `source/1995-08-23_compusa-norwalk_dan-lynch_original.mp4` (32,302,815 bytes, sha256 `f6d309c70d1eccbc9e3af3ba124bf123724e0427dca83789635e74310baeccb6`, byte-identical to the Internet Archive original); the full record is in `source/source.json` and `qa.md` Part 2. Item 2 was **not** downloaded. Devin also ruled that the CC0 applied by the Internet Archive uploader "The Nostalgist777" — not by the filmmaker Dan Lynch — is accepted as-is, and that filmmaker permission will **not** be pursued, which closes **H02-a** as *not pursued by decision* (not as *permission obtained*). The rest of this document is the original handoff and is left as written. **Acquisition is still not clearance:** R14 stays open and release stays blocked pending the OPS-04 review deck.

## Ungated free acquisition — item 1 downloaded 2026-09-15, item 2 not downloaded

These files are technically downloadable without login, payment, terms click-through or CAPTCHA. **Rights are not cleared.**
- The item pages show CC0 1.0, but it was asserted by the Internet Archive uploader "The Nostalgist777", who is not the named creator. Internet Archive states it "does not make guarantees as to the copyright status of items on archive.org" (https://help.archive.org/help/rights/).
- Any download is for internal proof and review only, and stays out of the cleared-media bin until R14 is decided.

| # | Item page (loaded) | Download option as shown on page | File name (IA metadata) | Dimensions | Duration | fps | Size | Save as |
|---|---|---|---|---|---|---|---|---|
| 1 (best) | https://archive.org/details/1995.08.23-windows-95-midnight-madness-norwalk-ct-wg-g-7-klymsg-0-854x-480 | DOWNLOAD OPTIONS → "MPEG4", 30.8M (original) | `1995.08.23-Windows95-Midnight-Madness-NorwalkCT[WgG7KLymsg0][854x480].mp4` | 854×480 | 230.62 s | not shown | 32,302,815 bytes (metadata API) | `assets/broll/BROLL-04/source/1995-08-23_compusa-norwalk_dan-lynch_original.mp4` |
| 2 (alt) | https://archive.org/details/comp-usa-windows-95-launch-pt-1-of-3 | DOWNLOAD OPTIONS → "MPEG4" (3 files: 670.3M, 588.9M, 541.4M); only part 1 is needed | `CompUSA Windows 95 Launch pt1 of 3.mp4` | 852×480 | 1357.44 s | not shown | 702,816,586 bytes (metadata API) | `assets/broll/BROLL-04/source/1995-08_compusa-nyc_ted-spero_pt1_original.mp4` |

**Notes for whoever performs the download:**
- The per-file download URLs for the **original** MPEG4 files were not opened in this pass. Take them from the item page's DOWNLOAD OPTIONS → SHOW ALL listing, or the file list at the metadata URL. Match the exact file names above.
- The in-page player streamed the derivative `https://archive.org/download/1995.08.23-windows-95-midnight-madness-norwalk-ct-wg-g-7-klymsg-0-854x-480/1995.08.23-Windows95-Midnight-Madness-NorwalkCT%5BWgG7KLymsg0%5D%5B854x480%5D.ia.mp4` ("H.264 IA", 30.1M). Prefer the original "MPEG4".
- Also save the item metadata JSON (`https://archive.org/metadata/<identifier>`) and a copy of the item page as license evidence.
- After download, run `ffprobe` to record the real fps, codec and duration. Then confirm the out point 00:02:24.0 frame-accurately (item 1) and 00:10:43–00:10:53 (item 2).
- Item 2's original is 670 MB. Download only after item 1 is judged insufficient.

## H02 gated items (human decision required; no action taken)

| # | What | Where | Barrier / cost | Human step |
|---|---|---|---|---|
| H02-a | Written confirmation or permission from the actual camera operators for items 1 and 2, so the CC0 is backed by the rights holder | Dan Lynch, https://www.youtube.com/@danlynch203 (original `WgG7KLymsg0`); Ted Spero, https://www.youtube.com/@tedspero4545 (originals `rjwidy5VEGw`, `K1742uWS0a8`, `yGe8WW2JtFw`) | Contacting them means sending a message on Devin's behalf. Cost unknown. The YouTube license line on the originals was **not** read (page fetch returned only footer) | Devin decides whether the uploader's CC0 is enough, or contacts the creators |
| H02-b | KXAS-TV "[News Clip: Comp USA]", 3 Aug 1993, 1:22 Betacam news footage (not viewed) | https://texashistory.unt.edu/ark:/67531/metadc2152255/ ; licensing FAQ https://library.unt.edu/special-collections/nbc-5kxas-wbap-research-faq/ | In Copyright (rights holder NBC5/KXAS-TV). License required for public use. Beginning rate "$90 per second", case-by-case (a 10 s use at that starting rate would be $900 before other factors; no quote obtained). The viewer page shows a CAPTCHA | A human views the clip past the CAPTCHA, decides whether it shows browsing, then submits UNT's "Request to License Special Collections Materials" form. Contact per FAQ: askus@unt.edu, 940.565.2411 |
| H02-c | "Inside a computer store in 1991" (NYC), 6:46 | https://www.youtube.com/watch?v=nYeOrO1ZFCc (author Vampire Robot) | YouTube-hosted: the standard platform license is not reuse permission. Not motion-reviewed | Lead only: would need permission from the uploader and underlying rights holder |
| H02-d | "Buying Windows 95 on Launch Day" (Egghead Software and CompUSA, 24 Aug 1995 per description), 1:38 | https://www.youtube.com/watch?v=CcbAC4qI9pQ (author Vampire Robot) | Same as H02-c. The description suggests news-style footage, so a broadcaster may own the rights | Lead only |
| H02-e | Pond5 item 47021392, "1990s Interior computer retail store, ty…" | https://www.pond5.com/pt/stock-footage/item/47021392-1990s-interior-computer-retail-store-types-screens-shelf (URL from web search; page did not load for the agent) | Paid stock; price not seen (HTTP 403 / captcha marker). The title suggests screens on a shelf rather than boxed software | Human may open and preview. No purchase without explicit decision |

## Not commissioned

An AI-generated stand-in or a staged reenactment would need separate explicit approval and a new, labeled assignment (ticket requirement 6). Neither was created.
