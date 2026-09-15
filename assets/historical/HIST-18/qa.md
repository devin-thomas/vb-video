# HIST-18 — QA: Download.com archived site circa 1996

**Production:** produced. **Release:** blocked (R14 rights unresolved). **Reviewer:** none yet (goes to the OPS-04 review deck).

## What was acquired
- `source/original.html` is the Wayback Machine `id_` record of `http://www.download.com:80/`, capture **19961221110042**. It is saved byte-exact: 14,744 bytes, sha256 `167109450df3f44d4b7aa42a9637ef5cce4aaeaaa0cc461d99deccc8f4211d24`. This is the earliest download.com capture in the Wayback index.
- `source/embeds/` holds all 28 images the page visibly references, each fetched from its own archived URL. All were captured 1996-12-21 between 11:01:00Z and 11:10:23Z (per-image record in `evidence/embeds.json`). **None were missing; none were substituted.** Images inside HTML comments do not render and were not fetched.
- `evidence/wayback-replay-page.png` shows the live Wayback replay page with the archive toolbar (DEC 21 1996). `evidence/wayback-response-headers.txt` and `evidence/cdx-download.com-1996.json` hold the archive headers and capture index.
- Access was anonymous public GET only. Some image requests hit Wayback rate limiting (connection refused / HTTP 429) and were retried with pauses. No account, terms click-through, CAPTCHA or payment was involved.

## Checks actually performed
1. **Identity/date:** checked by reading the original HTML. It has the title `DOWNLOAD.COM -- Welcome`, a server comment dated `Sat Dec 21 02:03:11 1996` and the footer `Copyright© 1996 CNET Inc.`. The archive memento is `Sat, 21 Dec 1996 11:00:42 GMT` and the origin Date header is `21-Dec-96 11:00:47 GMT`. The live Wayback replay matches the offline render in layout and imagery (compared visually).
2. **Offline render integrity** (`src/capture.py`, log `evidence/capture-log.json`). The page loaded with zero broken images at both scales. There were zero aborted (unarchived) requests and no network access. Layout measured 800×905 CSS px. Fonts were computed by Chromium defaults: Times New Roman, monospace, and Courier New.
3. **Wayback replay capture:** the page loaded with zero HTTP ≥400 responses.
4. **Export structure:** both exports are genuine RGB PNGs at 1920×1080 (checked with Pillow).
5. **Crop reversibility:** crop box, uniform scale and placement are recorded in `evidence/transforms.json`. Scaling is uniform only, with no stretch. The first editorial crop (CSS y 0–720) cut through the sidebar "search yahoo" label at its bottom edge. It was moved to 0–706, which ends at the bottom of the special-offer bar. The crop removes only the lower sidebar Yahoo! search box and the footer (CNET disclaimer/copyright). The uncropped variant keeps both, so no meaning-changing context is lost.
6. **Manual visual inspection, full size:** both exports were viewed as 1:1 960×540 tiles covering the whole canvas. Page text and archived GIFs are sharp. GIF upscaling shows original low-resolution dithering, as expected. Nothing sits outside the canvas. The caption (Segoe UI 28 px) sits inside the title-safe band (y 54–1026), and no crop edge shows a partial label.
7. **Manual visual inspection, 720p:** `evidence/proofs/editorial-frame-720p.png` and `evidence/proofs/original-720p.png` were viewed. The editorial frame reads clearly. In the uncropped variant, the sidebar links and footer text are small but legible, so it suits reference rather than on-screen reading.
8. **Content check:** no private information is visible. A CNET staff name appears only in an HTML comment of the byte-exact original; it is not rendered and not repeated in records. No remote font/CDN dependency exists in the exports, and no UI was added inside the page pixels.
9. **Delivery validator:** `python tools/validate_delivery.py --id HIST-18` is run after `delivery.json` is generated. Its actual output is recorded in `state.json` notes and the worker report, because this file is hash-locked in the inventory.

Not checked: OCR, colour accuracy against a 1996 display, and how Netscape Navigator 3 would have rendered the page.

## Authenticity notes
- The capture is a **modern Chromium rendering** of archived 1996 bytes, not a period screenshot. Text rasterization and default fonts are 2026 Windows ones, although the 1996 page did request Courier New for highlight headings. Layout follows the fixed-width HTML tables.
- The 800 px viewport is an authored choice meant to represent a common 1996 desktop width. The page content is a fixed 600 px table.
- The source line under the image, the flat RGB(32,34,37) ground and the crop are authored additions (`evidence/provenance.json`).

## Remaining blockers / review questions
- **R14 rights (blocking release):** the page is "© 1996 CNET Inc. All rights reserved". It includes a General Magic banner ad, Magic: The Gathering artwork and sponsor/Yahoo! logos. The Internet Archive grants no license. Decision needed: fair use, permission, or drop.
- **Editorial taste:** the top banner ad reads "BUTT / KICK MORE OF IT." It is authentic to the capture but prominent in the editorial frame. Keep it, or choose a lower crop that starts below the banner (CSS y ≥ 70)?
- **Authenticity label:** is a modern-browser render of archived bytes acceptable for a "circa 1996 screenshot", given the caption already says "Internet Archive Wayback Machine capture"?

## Reproduction (from repository root, Windows)
```
# acquisition (network): native original + per-image records
curl -o assets/historical/HIST-18/source/original.html "http://web.archive.org/web/19961221110042id_/http://www.download.com:80/"
#   each image: GET the "request" URL listed in evidence/embeds.json, save to source/embeds/<saved>
# capture (offline; add --replay for the Wayback toolbar evidence shot, needs network)
python assets/historical/HIST-18/src/capture.py
# framing
python assets/historical/HIST-18/src/frame.py
# metadata + validation
python assets/historical/HIST-18/src/make_delivery.py
python tools/validate_delivery.py --id HIST-18
```
Toolchain: Python 3.14.0; Playwright 1.63.0 with Chromium 153.0.8010.12 (headless); Pillow 12.3.0; curl (Git for Windows); font Segoe UI from `C:/Windows/Fonts/segoeui.ttf` (system, not bundled). The 720p proofs and 1:1 tiles were made with Pillow LANCZOS resize and crop.
