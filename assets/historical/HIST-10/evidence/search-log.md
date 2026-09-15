# HIST-10 search log (2026-09-15)

Starting query from the ticket: *Egghead Software storefront 1990s photo*. Every access was an anonymous public request. No account, login, payment, CAPTCHA, or terms acceptance was involved.

| # | Where | Query / method | Result |
|---|-------|----------------|--------|
| 1 | Web search | Egghead Software store storefront photo 1990s; "Egghead Software" store photograph flickr/archive.org/wikimedia; flickr Egghead Software store sign; "Egghead Software" store photo Creative Commons / public domain | Leads: Virtual Moose blog posts, IA catalogs, the Commons coffee cup, the CHM merchandise catalog |
| 2 | Wikimedia Commons API | file search: Egghead, Egghead Software, Egghead store; category search: Egghead | Only the logo-only *Egghead Software Coffee Cup.jpg*. The API returned HTTP 429 on some repeats; the queries that did complete found no storefront |
| 3 | Openverse API | egghead software, egghead store, egghead computer, egghead, egghead sign, egghead discount | Flickr 534320393 (candidate C2: branded power splitter, CC BY-NC 2.0) |
| 4 | Flickr photo page 534320393 | page metadata | 2007-06-06; Adrian Black; CC BY-NC 2.0; not a storefront |
| 5 | virtualmoose.org 2023-09-06 and 2024-11-14 posts | page and image inspection | Night exterior (candidate C3): uncredited, 456x301. Catalog scans credited to a social-media repost |
| 6 | Internet Archive advanced search | egghead AND (software OR store) | Catalogs from 1988, 1990 and 1993, plus **youtube-CcbAC4qI9pQ "Buying Windows 95 on Launch Day"** |
| 7 | IA item youtube-CcbAC4qI9pQ | metadata, thumbnails, files.xml; downloaded the MP4 (for locating the shot) and the WebM original | Egghead storefront shot at 0:08 to 0:19 (timecode 10:46:02 to 10:46:17). Selected as candidate C1 |
| 8 | YouTube channel page @vampirerobot | channel description | No footage-source statement |
| 9 | Video Game Sage forum thread about the channel | fetch | HTTP 403; not read |
| 10 | Wayback CDX, egghead.com/* images 1995-1998 | mimetype image/* | 65 small interface GIFs; no photos |
| 11 | UW Libraries CONTENTdm | full-text search "egghead" | 14 hits, including Egghead annual reports 1989-1999 (In Copyright). The 1995 report was downloaded to scratch and all 25 pages viewed: no store photographs |
| 12 | Library of Congress P&P; loc.gov photos; Calisphere | egghead / egghead software | No Egghead store images |
| 13 | Computer History Museum catalog (via web search) | Egghead | Merchandise records only (t-shirt, sweatshirt) |

## Shot selection

Frames were sampled at 2 fps over 0 to 24 s. The shots at 15.0 s and 15.4 s show the full sign with the doorway clear. Decoded frame 462 (15.415 s, timecode 10:46:14;06) was chosen because the sign sits entirely in frame and the least of it is covered. The same frame index gives matching content in the IA MP4 derivative (PSNR 32.5 dB against about 18 to 21 dB for the neighbouring frames).
