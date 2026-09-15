# Production bible

## What is inherited and what is proposed
The script requests a Windows-95/VB4-era visual treatment, dark syntax-highlighted code, green felt/card imagery, diagrams, chapter cards, and modern terminal evidence. Those ideas are inherited. All dimensions, colors, timings, interfaces, filenames, and test conventions below are **proposed production defaults added by this build pack**, not statements from the sources. A producer may override them in a recorded decision before the shared system freezes.

## Picture and edit defaults
Use a 1920×1080, 16:9 logical canvas. Generated motion defaults to 30 frames per second and opaque H.264/yuv420p MP4 review exports. Keep editable vector/HTML originals; add transparency only when a ticket explicitly needs it, using PNG for still alpha. Do not claim H.264 supports the required transparent overlay. Optional 4K exports are out of scope unless requested.

Keep essential text within x=120…1800 and y=72…1008. Reserve enough space for captions in the edit; do not burn narration subtitles into every asset. A screenshot keeps its original aspect ratio, framed/pillarboxed rather than stretched. Do not crop a computer screen or title bar in a way that conceals a different product/version.

Narration is not supplied as audio. The chapter metadata is a locator, not a locked 43:30 timeline. Ticket seconds are proposed local storyboard timings. Motion should have a readable opening and closing hold. A code focus with many targets may be lengthened rather than sped past comprehension. Each asset owns its own local timeline and named cutdowns.

## Visual tokens
Desktop teal #008080; window gray #C0C0C0; active title navy #000080; dark code background #111318; light code foreground #F1F3F5; keywords #79ADFF; strings #EAB676; comments #8DC48C; felt #0B6B3A. These are original style defaults, not claims of pixel-perfect historical system values. Red/black card suits are conventional; pair every emphasis color with labels, outlines, or position.

Use installed system sans-serif fonts (e.g., Segoe UI or a local generic sans fallback) and an installed monospace for code (e.g., Consolas or generic monospace). Record the resolved font and inspect fallback layout. **Do not bundle font files.** No remote font/CDN dependency. Suggested 1080p sizes: title 64–80 px, chapter 56–72, body/diagram 34–42, code 30–36, optional micro-labels at least 26. Check actual legibility rather than blindly enforcing a tiny font to fit. Split a dense comparison or page a long code excerpt; do not force 286 source lines onto one screen.

## Original Win95-inspired UI
Use square corners, restrained bevels, gray controls, and dark blue title bars. The design is a reconstruction. Do not forge original application screenshots. No decorative slogans, arbitrary error messages, invented company branding, forced meme copy, or extra CTAs. Only the requested end card carries Subscribe/Like/Next video.

## Cards and algorithm grammar
Use original SVG cards with rank 2…14 and suit S/H/D/C. Map J=11,Q=12,K=13,A=14. Keep red suits distinguishable without color alone. Player1 left, Player2 right, pot center. Queue index 0 is the top; winning cards enter the bottom. Face-down burns conceal identities on screen, even when fixtures retain them for audit.

`fixtures/war_storyboard.json` is an **authored teaching fixture**, not a real terminal run. Its same-scene identities are unique and every counter state sums to 52. `fixtures/deck_order.json` derives from the literal nested loops. `fixtures/shuffle_storyboard.json` is a small deterministic example, not evidence of randomness or unbiasedness. Never present these as captured program execution.

## Editable formats and deterministic motion
Diagram stills: SVG primary where practical. Layout/code/text cards: offline HTML/CSS primary. Historical images: native original plus framing/annotation layers, not an AI redraw. Local export requires an actually available renderer; source generation being Tier 1 does not magically make every export tool available.

Animated HTML implements `window.__ASSET__` with `id`, `durationSeconds`, `fps`, `width`, `height`, `ready` (a Promise), and `renderAt(seconds)`. Calling renderAt must fully establish the scene at that time with no dependence on prior playback. Clamp time to the supported range, eliminate wall-clock/random/network dependence, wait for local fonts/assets, and set every animated element from the requested time. Pause CSS animations or drive them deterministically. Export frames at t=frameIndex/fps, frame indices 0…ceil(duration×fps)−1. A separate final hold state may be exposed for poster extraction. Do not autoplay sound. Timeline JSON identifies beats, state variables, named cutdowns, and source/event provenance.

The worker records its exact local render command and tool versions. If the export capability is missing, deliver editable source and a capability blocker, not a fake PNG/MP4. A video made from real transcript playback is a replay, not a live desktop recording.

## Evidence, publication, and human boundaries
Every artifact has a provenance classification: source-code derived, authored teaching illustration, original mockup, actual runtime capture, historical source, or stock candidate. Internal proofs can exist while factual/rights gates remain open. **Production completion and release approval are different fields.** Do not add big “UNVERIFIED” watermarks to reusable source content as a substitute for metadata; keep blocked previews in their own state and exclude them from the cleared-media manifest.

No account creation, payment, permission agreement, security change, download bypass, real-voice cloning, or public upload is authorized by a ticket. Use the relevant human handoff. Human-only labels in the original plan are retained as workflow boundaries, not universal claims about what every possible future agent environment can operate.

## Definition of done
A ticket is complete only when its promised files exist, its own content-specific checks pass, the producer can identify source and variant, the QA record includes full-size and 720p inspection, and the status truthfully distinguishes produced/reviewed/released. A source file alone is not a rendered asset; a public URL alone is not cleared acquired footage; a pretty screenshot alone is not runtime evidence.
