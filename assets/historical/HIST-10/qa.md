# HIST-10 — Production QA

**Production:** produced (archival proof). **Release:** blocked on R14. The rights holder of the footage is unknown and there is no license.

## Delivered
- `source/original.webm`: the Internet Archive original file for item `youtube-CcbAC4qI9pQ` ("Buying Windows 95 on Launch Day"), byte-identical to IA's recorded md5 and sha1.
- `source/raw/frame-000462.png`: the uncropped frame used (native 480×360, decoded frame 462, burned-in timecode 10:46:14;06). This is the `original` variant still.
- `exports/editorial-frame.png`: the 1920×1080 editorial frame (`editorial-frame` variant).
- `proofs/editorial-frame-720.png`: the 720p review proof.
- Evidence files:
  - `evidence/source.json` and `evidence/rights.json`
  - `evidence/provenance.json` and `evidence/claim-checks.json`
  - `evidence/candidates.json` (three candidates, ranked) and `evidence/search-log.md`
  - `evidence/source-excerpts.md` and `evidence/framing.json`
  - `evidence/archive-records/…_files.xml`
  - `evidence/qa-tests.json`
- Scripts: `src/build_hist10.py` and `src/finish_hist10.py`.
- Every file above is listed with its size and SHA-256 in `delivery.json`.

Variants are stills that hold for editorial timing. There is no motion and no cutdown timing.

## Method
1. Searched the public archives and indexes listed in `evidence/search-log.md`: Commons, Openverse/Flickr, Internet Archive, Wayback, UW Libraries, LoC, Calisphere, CHM, and the blog leads.
2. The only authentic storefront image with a stated period date was the IA video. I downloaded IA's original file anonymously and verified its hashes.
3. Located the shot on 2 fps contact sheets, then decoded exact frame 462.
4. Framed it without cropping: an integer 3× Lanczos upscale, pillarboxed on black. No text was added and the timecode was not removed.

## Checks actually performed
- **Original integrity against the IA record:** passed. md5 and sha1 match.
- **ffprobe stream check:** passed. VP9 480×360, 30000/1001 fps, 97.861 s.
- **Same frame in the IA original and the derivative MP4:** passed. PSNR 32.5 dB against about 18–21 dB for the neighbouring frames.
- **PNG dimensions:** raw 480×360, export 1920×1080, proof 1280×720 (checked by `finish_hist10.py`).
- **Privacy scan:** passed. Two raw IA metadata copies containing a personal e-mail address were removed before delivery.
- **`python tools/validate_delivery.py --id HIST-10`:** run after `delivery.json` was written; the result is reported to the manager.

## Manual visual inspection
- **Native (480×360), `source/raw/frame-000462.png`:**
  - The EGGHEAD SOFTWARE lettering is legible.
  - The door is open, with a yellow Store Hours card; its small print is not legible.
  - Boxed software is stacked in the window.
  - One shopper is seen from behind, with no identifiable face.
- **Full size (1920×1080), `exports/editorial-frame.png`:**
  - Correct 4:3 geometry with symmetric 240 px bars; no stretch or crop.
  - The sign is clearly readable.
  - The image is soft, with visible compression blocking from the 3× upscale of 480×360 video.
  - The burned-in timecode box sits at about y=15–65, above the y=72 safe line. It is source content, left intact.
- **720p (1280×720), `proofs/editorial-frame-720.png`:** the storefront and sign read immediately, and the softness is less noticeable.

## Content and authenticity limits
- **Identity:** verified from the visible signage.
- **Date:** 1995-08-24 is the uploader's claim. It is partly corroborated: the same continuous timecode run includes CompUSA Windows 95 Upgrade launch displays. No date is drawn into the asset.
- **Place:** not stated by any source, so it is not recorded or captioned.
- **Script check:** SCRIPT.md:128 (Egghead as a physical store in 1995) is verified against Egghead's 1995 annual report (UW Libraries). No script change is needed.

## Gates and review questions
- **R14:** blocked. The per-image record is complete (creator unknown, no license, access route and hashes, credit text drafted), but the rights holder is unknown and no fair-use or public-domain assumption was made.
- **Review question 1:** use this frame on an editorial or fair-use basis, try to trace and ask the footage owner, or drop it?
- **Review question 2:** if the frame is used, is the credit line acceptable, and should the burned-in timecode stay visible?
- **Lead, unverified:** a higher-quality dusk exterior photo (candidate C3) may come from an Egghead annual report other than 1995. Its rights would still be In Copyright.
- **Dependency OPS-01:** not consumed. No shared template was used, because the image is an archival still framed by this ticket's own script.

## Reproduction
Run from the repository root:

```
python assets/historical/HIST-10/src/build_hist10.py
python assets/historical/HIST-10/src/finish_hist10.py
python tools/validate_delivery.py --id HIST-10
```

To re-acquire the original:

```
curl -L https://archive.org/download/youtube-CcbAC4qI9pQ/CcbAC4qI9pQ.webm -o assets/historical/HIST-10/source/original.webm
```

The build refuses to run if the SHA-1 differs from the IA record.

**Toolchain:** Windows 11 (10.0.26200); Python 3.14.0; Pillow 12.3.0; ffmpeg/ffprobe 6.0 essentials build (gyan.dev); curl. No fonts and no remote dependencies.

**Reviewer:** none yet. Inspection was done by the producing agent only; release decisions belong to the review deck.
