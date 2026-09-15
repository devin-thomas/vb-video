# Shared contract — win95-workbench-1.0.0

The media canvas is 1920 × 1080. Motion is 30 fps, H.264, yuv420p, silent. Color roles and drawing primitives live in `tools/render/studio.py`. Each asset owns its own scene files, timeline, variants, evidence, and exports. No network resources or font files are included.

## Authoring
`python tools/render/build_assets.py --id CODE-02` regenerates the authored scene and the exact source excerpt. `python tools/render/render_assets.py --id CODE-02` rasterizes and encodes it. Building sources resets that ticket to in_progress; run the QA and delivery finishing steps before relying on its state again. These commands do not install missing tools.

The shared authoring scripts encode this production batch's individual compositions. For normal per-asset edits, edit that asset's SVG states or timeline/build.json and use the renderer directly. Do not run build_assets.py afterward unless intentionally discarding those local source edits. Use only the assets explicitly selected by --id when refreshing sources.

## Deterministic HTML
Each `src/index.html` inlines its SVG states and exposes `window.__ASSET__`: id, width, height, fps, durationSeconds, ready, renderAt(seconds). `renderAt` clamps time and selects the last authored state whose start time is not greater than that time. It is independent of prior seek position. The delivered motion is discrete instructional state animation, not continuous optical simulation or a real screen recording. There are deliberate reading holds.

Space plays; Home resets. The gallery adds visible controls and seeking. Still assets use time zero. No fetch, CDN, icon library, tracking, remote font, or external image is required. Browser testing used in-memory loading because this sandbox blocks direct file URL navigation; offline structure was verified rather than assuming file:// was permitted here.

## Exports and variants
PNG and SVG are clean artwork. MP4 uses the same states as HTML at 30 fps. `src/build.json` is the raster/video build driver; `src/timeline.json` is the editorial timing record. Update both when manually changing motion timing, or use the authoring script to keep them together. Named cutdowns have independent MP4s where required by the original ticket. All other named variants have separate SVG and PNG files.

The 52 card primitives in assets/shared/cards/ are original vectors. Small cards omit redundant corner details to remain legible. They do not use copied game sprites. Do not redistribute system font files; install the named fonts locally or accept a deliberate reflow when regenerating. Existing rendered media does not depend on the viewer having any fonts.
