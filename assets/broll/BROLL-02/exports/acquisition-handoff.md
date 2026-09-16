# BROLL-02 — Acquisition handoff

**Prepared:** 2026-09-15 · **Updated 2026-09-15: item 1 is now acquired.** Items 2 and 3 remain *not acquired*.

None of these clips shows the card game War. All ungated items are **generic card-game fallbacks** (see `candidates.md`).

> **Acquisition update — 2026-09-15.** Devin approved downloading item 1, and it was fetched ungated with `curl -L` and a generic browser User-Agent: no login, no payment, no terms click-through, and no Cloudflare or CAPTCHA check appeared. It is saved unchanged at `source/pexels-38810850-jellymarketing-elderly-couple-cards-1920x1080.mp4` (4,393,818 bytes; sha256 `7b43b09327990d2b6bcd606a47a3646565c3a8788d9bde46142a244952eec188`; 1920×1080, 9.634625 s, 23.976 fps, H.264, no audio track). Its full source record is `source/source.json`. Acquiring it did not change what it shows: it is still a labeled generic card-game fallback, **not War**.

## Ungated free acquisition

These need no account, payment, CAPTCHA or terms acceptance to download. Item 1 is done. For items 2 and 3, the manager still needs a download approval from Devin; after approval, save the original file unchanged at the listed path and record its actual size, duration and dimensions.

| # | Asset page | Creator | Download option as shown | Download URL | Dimensions / fps | File size | Save as |
|---|---|---|---|---|---|---|---|
| 1 (rank 1) — **ACQUIRED 2026-09-15** | https://www.pexels.com/video/elderly-couple-enjoying-card-game-indoors-38810850/ | Jelly Marketing | "Free download" dropdown → "Choose a size:" → **"Full HD 1920x1080"** → "Download Selected Size" | `https://www.pexels.com/download/video/38810850/` (302 → `https://videos.pexels.com/video-files/38810850/16496615_1920_1080_24fps.mp4`) | 1920×1080, 23.976 fps (verified with ffprobe), 9.634625 s, no audio | 4,393,818 bytes (verified) | `assets/broll/BROLL-02/source/pexels-38810850-jellymarketing-elderly-couple-cards-1920x1080.mp4` |
| 2 (rank 2) | https://pixabay.com/videos/card-game-game-cards-gambling-card-254893/ | KamiArtist | **"Free download"** button (size dropdown opened but rendered no options in this session) | No download URL recorded; use the page button | 1920×1080, 30 fps, MP4 (page details) | Not displayed | `assets/broll/BROLL-02/source/pixabay-254893-kamiartist-friends-playing-cards-1920x1080.mp4` |
| 3 (rank 3, **motion not reviewed**) | https://www.pexels.com/video/grandfather-playing-a-card-game-with-his-granddaughter-9058103/ | SHVETS production | "Free download" dropdown → "Choose a size:" → **"4K UHD 3840x2160"** (original) → "Download Selected Size"; other listed sizes: SD 426x240, SD 640x360, SD 960x540, HD 1280x720, Full HD 1920x1080, Quad HD 2560x1440 | No download URL recorded; use the page button | 3840×2160, 50 fps (page) | Not displayed | `assets/broll/BROLL-02/source/pexels-9058103-shvets-grandfather-granddaughter-cards-3840x2160.mp4` |

Recommendation: #1 was approved and is acquired. Only approve #3 after someone plays it through, because its motion was not reviewed.

License evidence to save alongside any download (read on 2026-09-15):
- Pexels License: https://www.pexels.com/license/ (free use and modification, attribution optional; no bad-light depiction of identifiable people, no endorsement implication, no unaltered resale or redistribution on stock platforms, no trademark or business-name use).
- Pixabay Content License summary: https://pixabay.com/service/license-summary/ (full terms at https://pixabay.com/service/terms/, not loaded) (free use without attribution, modification allowed; no standalone unchanged resale, no commercial use of visible trademarks or brands, no immoral, illegal or deceptive use of identifiable people; the user checks third-party rights).

## H02 — gated or rights-blocked items

These are the only leads that visibly promise real War play. They are YouTube videos under the standard platform terms, which do **not** grant reuse permission. Using one needs the rights holder's explicit permission, which is a user or producer decision. No agent action was taken.

| Lead | Channel (from YouTube oEmbed) | What it likely shows | Barrier | Cost |
|---|---|---|---|---|
| https://www.youtube.com/watch?v=kEhF96ea7wo — "How to Play the War Card Game With 2 Players" | ExpertVillage Leaf Group (https://www.youtube.com/@expertvillage) | Two-player War instruction (title only; **not viewed**) | Standard YouTube terms; needs permission or licensing from the rights holder | Unknown; not requested |
| https://www.youtube.com/watch?v=LeB_PnAWJXA — "How To Play War: A Quick Game of CHANCE and BATTLE!" | Game Rules (https://www.youtube.com/@GameRulesCom) | War rules tutorial (title only; **not viewed**) | Standard YouTube terms; needs permission or licensing from the rights holder | Unknown; not requested |

Not verified for either lead: duration, resolution, the license field on the watch page, on-screen captions or watermarks, narration, and whether the footage shows a live table flip or an animation. The watch pages returned only footer markup to WebFetch, and they were not played.

Out of scope (not scouted): paid iStock clips advertised on the Pixabay page, excluded by the "no paid footage" boundary. A staged live shoot or an AI-generated stand-in needs separate explicit approval and a new labeled assignment (ticket requirement 6).

## Steps for the human (H02 checklist)
1. Decide between fallback rank 1, a permission request for a YouTube War demo, or a new staged or AI assignment (see the review questions in `candidates.md`).
2. For ungated items: approve the batched download; save the originals at the paths above together with the license page evidence.
3. For YouTube leads: any contact with rights holders, terms acceptance or payment belongs to the user.
4. After acquisition, the owner verifies duration, dimensions and fps against this sheet and re-checks for watermarks or captions at full size.
