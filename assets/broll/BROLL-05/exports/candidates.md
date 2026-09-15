# BROLL-05 — Floppy disk insertion close-up: candidate report

Scouted 2026-09-15. **Scouting only — no media acquired, nothing cleared.** Release stays blocked on R14.

Timecodes are seconds from clip start, read from each page's own preview player while seeking it in the in-app Browser.

## 1. Recommended — Pexels 20503026 (Stefan)

| Field | Value |
|---|---|
| Asset page | https://www.pexels.com/video/floppy-disk-80s-computer-retro-diskette-20503026/ |
| Creator | Stefan (Pexels) |
| Duration | 0:11 on page; 11.16 s in player |
| Source size / fps | 1920×1080, 23.98 fps |
| Proposed in / out | **00:00.00 → 00:06.00** (6.0 s) |
| License | Pexels License, https://www.pexels.com/license/ — free to use, no attribution required, modification allowed; not allowed: selling unaltered copies, redistributing on stock platforms, implying endorsement, trademark use, showing identifiable people in a bad light |
| Barrier | None seen: no login, no CAPTCHA. Download not attempted |
| Motion review | Done. 13 frames from 0.1 s to 10.9 s |

**What happens:**
- **0.0–0.8 s:** empty drive (clean handle).
- **1.0–2.2 s:** a red disk goes in.
- **3.0 s:** a thumb pushes it home.
- **About 3.5–6.0 s:** static hold, no hand.
- **From 6.5 s:** the hand returns, presses eject at 7.0–7.5 s, and the disk pops out at about 9 s.

**Checks against the brief:**
- **Media size, pass.** It's a 3.5-inch disk: rigid square shell, label legible at 1.5 s as "2HD", "IBM" and "1.44", and the disk is as wide as the slot. It isn't 5.25-inch or 8-inch.
- **Drive, pass.** One narrow horizontal slot, a push-button eject at the right end and an indicator window at the left. There's no 5.25-inch latch lever. The drive model isn't identified.
- **Direction, pass with a caveat.**
  - The drive lies flat and the label side faces up.
  - The metal shutter isn't visible in any frame I sampled.
  - At 2.2 s the trailing edge shows the corner holes. On a 3.5-inch disk those are on the edge opposite the shutter, so the shutter end leads. This is inferred, not seen directly.
- **Hand and disk in frame, pass** for 1.0–3.0 s.
- **Captions or watermarks:** none seen. Audio wasn't checked.
- **Weaknesses:**
  - It's 6 s, short of the 8–12 s target.
  - It's a bare drive on diamond plate at a diagonal angle, not a drive inside a period PC.
  - "IBM" is legible on the label.

## 2. Alternative, rights-blocked — Mixkit 48937

| Field | Value |
|---|---|
| Asset page | https://mixkit.co/free-stock-video/floppy-disk-being-inserted-into-the-system-unit-48937/ |
| Creator | Not shown on the rendered page (unconfirmed) |
| Duration | 0:07 on page; 7.24 s in player |
| Source size / fps | 1280×720 free version (4K via Envato), 25 fps, 2.44 MB |
| Proposed in / out | 00:00.00 → 00:07.24 (7.24 s) |
| License | **Mixkit Restricted License**, https://mixkit.co/license/#videoRestricted. The page says "for Personal Use only". Mixkit's info page says it can't be used in monetized or commercial content. The commercial 4K version needs a paid Envato subscription. |
| Barrier | Free 720p link needs no login, but its license doesn't fit a public video. The commercial version is paid, so it goes to H02. |
| Motion review | Done. 4 frames (0.1, 2.0, 4.0, 6.5 s) |

**Checks against the brief:**
- **Drive, pass.** Horizontal 3.5-inch-style bay in a pale case.
- **Media size, likely 3.5-inch**, but the disk is seen nearly edge-on, so the size isn't confirmed from a label.
- **Direction, not verifiable.** Neither label side nor shutter end can be seen.
- **Readability as a floppy is weak.**

No second acceptable alternative was found.

## Rejected after inspection

- **Pexels 20503027 (Stefan, 5.6 s).** It's an eject, not an insertion, even though the page describes it as inserting. The disk is inside at 0.1 s, the eject is pressed at 1.2 s and the disk slides out with no hand at 2.5 s. Played in reverse, the disk would slide in by itself.
- **Pexels 33125208 (Stefan, 7 s, 20 fps).** A 5.25-inch disk goes into a Commodore 1541 drive with a latch lever. Wrong media and wrong drive.
- **Pexels 20503028, 20503031 and 20503030 (Stefan, 3–5 s).** I excluded these on their page descriptions (a disk stack, a drive mechanism, hands handling a disk). Motion wasn't reviewed.

## Searched with no usable result

- **Pixabay:** 4 queries, no floppy video.
- **Coverr:** 0 results.
- **Wikimedia Commons:** 0 video results.
- **Internet Archive:** 195 hits. Mostly YouTube mirrors and podcasts; no close-up stock clip.
- **Videvo and Vista Create:** HTTP 403 to WebFetch; not browser-checked.

The full log is in `evidence/candidates.json`.

## Review questions

See `evidence/claim-checks.json`, RQ1 to RQ4.
