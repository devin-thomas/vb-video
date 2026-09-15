> Preserved README of the 2026-09-15 produced-asset delivery (session 1, 71 assets). Links are updated for this repository; counts and prose describe that delivery. See [../README.md](../README.md) for the current state.

# Visual Basic — Produced asset delivery

**71 individually packaged assets + the shared visual/export system.** Open [START_HERE.html](../START_HERE.html) after extracting the entire folder. No server or installation is required to browse the gallery and watch the MP4s.

## See the work
[Preview reel](../review/PREVIEW_REEL.mp4) · [Visual contact sheet](../review/CONTACT_SHEET.jpg) · [Remaining tickets](../review/REMAINING_TICKETS.md) · [Original ticket index](TICKET_INDEX.md)

This is an asset-production delivery, not the final narrated episode. Media is 1920 × 1080; motion is H.264 at 30 fps with no audio. The animations use deliberate step states and reading holds. They are not live program captures. The preview reel is a silent selection of assets, not narration-synchronized editing.

## Produced
| Family | Assets |
|---|---:|
| Opening and end cards | 2 |
| Chapter cards | 16 |
| Exact Program.vb code cards | 25 |
| C# / VB comparisons | 8 |
| Fact cards | 6 |
| War GUI and download mockups | 2 |
| MsgBox and BASIC reference-code visuals | 2 |
| Diagrams and algorithm animations | 10 |
| **Total asset tickets with rendered deliverables** | **71** |

There are **54 motion assets**, **17 still assets**, **60 MP4 files** including required cutdowns, and **211 full-HD export PNGs** excluding contact sheets and temporal-keyframe subfolders. Main animation durations total **500.75 seconds**, excluding duplicated cutdowns. OPS-01 supplies the shared system, original 52-card vector deck plus card back, atlas, capability report, and export contract.

## Working with an asset
`assets/CODE-02/` is an example. `exports/` contains usable rendered media, `src/` contains separately editable SVG states plus HTML/timing data, `evidence/` preserves source anchors and actual checks, `proofs/` contains review-size imagery, and `delivery.json` inventories the outputs by SHA-256. `qa.md` describes the review actually performed and remaining gates. Each original ticket has a delivery addendum and links back to its own results.

Import PNGs and MP4s from the chosen asset's exports folder into your editor. Code-card clean and highlighted variants are separate, and long excerpts have extra clean pages rather than being reduced to illegible type. No narration timing is locked. For regeneration, read [shared/REBUILD.md](../tools/render/REBUILD.md). Do not redistribute system fonts: no font files are included.

## Status and limits
**Produced is not release-approved.** All 71 have rendered files and executed technical checks. No publication approval is invented. Claim-gated proofs retain their original wording rather than silently rewriting your script. In particular, CH-10 still carries the source's “recursion” title; the matching diagram depicts the actual inner loop. Historical fact cards and other assigned claims remain marked for editorial review. See [EDITORIAL_REGISTER.md](EDITORIAL_REGISTER.md).

**59 asset tickets remain unproduced.** The .NET SDK is absent here, so runtime captures and the actual project-settings capture are blocked. Code illustrations are not terminal screenshots. Historical-image sourcing and stock-footage scouting were not attempted in this batch; no reconstructed interface is passed off as archive material. Narration, music, effects, final assembly, and upload remain outside this delivery.

## Verification
The unchanged original sources passed their hash checks. The original pack's 130-ticket/50-family/74-cue coverage validator passed. All produced media packages are checked with the original delivery validator. Full-HD dimensions and MP4 codec/rate/duration are checked; offline HTML, deterministic seeking, and text canvas bounds are tested in installed Chromium. Visual review includes all posters on contact sheets and selected detailed/temporal views. It is not a claim that every frame received independent full-resolution human review.

Reports live in `review/`: summary.json, delivery-validation.json, browser-summary.json, pack-validation.txt, manual-review.json, reel-edit.json, and production-index.json. The immutable planning manifest remains in manifest.json; current production state is in assets/<ID>/state.json. The original start guide is preserved under docs/ORIGINAL_BUILD_PACK_README.md.
