# BROLL-01 acquisition handoff

> **STATUS UPDATE 2026-09-15 — rank 1 acquired.** Devin approved the rank 1 download; it was fetched, verified and committed as
> `source/mixkit-100384-deck-of-cards-being-shuffled-1080p.mp4` (73,935,932 bytes, sha256 `65b65dd0…7f73ff2`, 1920x1080, 19.394375 s, 23.976 fps, no audio).
> Production status is now `produced`. Release remains `blocked` (R14 open). **Ranks 2 and 3 were not approved and were not downloaded.**
> The download encountered no login, payment, CAPTCHA or terms gate. See `source/source.json` and section 3 of `qa.md`.
> The table below is the pre-acquisition record, left as written.

**Original text follows.**

**No file has been downloaded.** Scouting status: `scouted`. Acquisition status: not acquired. Release: `blocked` (R14 open).

## Ungated free acquisition — pending download approval

These are free Mixkit clips. The asset pages show no login, payment or terms-acceptance step before the download button. The button was **not** clicked, so the no-login path is observed, not exercised. Each option URL below is the `value` of the download radio input as it appears on the asset page's DOM (read 2026-09-15). The URL was **not** requested. The page's "File Size" attribute shows the HD Ready size; the Full HD size comes from that option's `data-size` attribute.

| Rank | Asset page | Download option (label as shown) | Option URL (from page, not loaded) | Dimensions / fps | Size | Save as |
|---|---|---|---|---|---|---|
| 1 | https://mixkit.co/free-stock-video/deck-of-cards-being-shuffled-100384/ | "Full HD 1920x1080" (button text with default selection: "Download Free HD Ready Video") | https://mixkit.co/free-stock-video/download/100384/?context=sidebar&type=1080p | 1920x1080, 24 fps, 0:19 | 70.51 MB | `assets/broll/BROLL-01/source/mixkit-100384-deck-of-cards-being-shuffled-1080p.mp4` |
| 2 | https://mixkit.co/free-stock-video/person-shuffling-playing-cards-over-green-table-100398/ | "Full HD 1920x1080" | https://mixkit.co/free-stock-video/download/100398/?context=sidebar&type=1080p | 1920x1080, 24 fps, 0:10 | 36.53 MB | `assets/broll/BROLL-01/source/mixkit-100398-person-shuffling-playing-cards-over-green-table-1080p.mp4` |
| 3 | https://mixkit.co/free-stock-video/close-up-of-hands-shuffling-playing-cards-100372/ | "Full HD 1920x1080" | https://mixkit.co/free-stock-video/download/100372/?context=sidebar&type=1080p | 1920x1080, 24 fps, 0:18 | 66.35 MB | `assets/broll/BROLL-01/source/mixkit-100372-close-up-of-hands-shuffling-playing-cards-1080p.mp4` |

The smaller "HD Ready 1080x720" options (720p type URLs, 6.97 / 3.49 / 6.43 MB) also exist. They are not recommended as the original for a 1920x1080 edit.

**Minimum approval to proceed:** rank 1 only (70.51 MB). **Full set:** 173.39 MB.

### After approval (owner steps)
1. Select "Full HD 1920x1080" on the asset page and click the download button in a normal browser session. Stop if any login, CAPTCHA or terms prompt appears, and move the item to H02 below.
2. Save the file under the name above. Keep it byte-identical, with no re-encode or trim.
3. Save a copy of the license modal text and the asset page (title, ID, license line) as `source/<name>.license.txt` alongside the file.
4. Run `ffprobe` to confirm 1920x1080, 24 fps and the duration. Check that the content matches the frames listed in `evidence/candidates.json` and that there is no watermark. Record the results in qa.md and add the file to delivery.json.

## H02 gated or rights-blocked items

None of the ranked candidates needs H02. These leads were not pursued and would need a human:

| Item | Where | Barrier | Cost |
|---|---|---|---|
| Pexels shuffling clips (e.g. 6813541 "A Person Shuffling the Cards", 35356475 "Close-up of Card Shuffling on Patterned Table", 7330829 "Person Shuffling Playing Cards") | https://www.pexels.com/search/videos/shuffling%20cards/ | Cloudflare bot-verification interstitial for the agent browser; HTTP 403 to fetch. Not bypassed. Devin could view them manually if the Mixkit set is rejected. The Pexels license page (https://www.pexels.com/license/) was readable. | Free per Pexels license; individual clip terms unverified |
| "Gambling — U.S.A." (1959) | https://archive.org/details/0763_Gambling_U_S_A_02_45_51_24 | No `licenseurl` or `rights` in the item metadata, so rights are unknown and blocked. Also off-style (640x480). | Unknown |
| iStock shuffling-cards footage | https://www.istockphoto.com/videos/shuffling-cards (seen in web search results only; not opened) | Paid stock, outside the project boundary (no paid footage) | Not investigated |

No YouTube or other platform-hosted leads were used.
