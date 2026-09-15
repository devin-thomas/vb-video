# Output and status contract

## Paths and ownership
All paths in a ticket’s required-output list are relative to `assets/<family>/<ID>/`. Each agent owns that folder only, except for the explicitly named OPS ownership additions. Do not rename outputs or overwrite originals to make a validation error disappear. `source/original.*` means one actual native original with its real extension; `source/raw/*.png` means one or more actual raw PNG captures. Globs are accepted only where specified. Gated discovery can return blocked/no_match without these media; it cannot claim produced/reviewed.

`manifest.json` is an immutable assignment index for this pack version. Live state is `assets/<family>/<ID>/state.json`. Each ticket is a complete work order, not an automatically executed command. Assets, external sources, recordings, narration, and video assembly have **not** been produced merely because their paths are listed here.

## Per-ticket delivery metadata
Copy `docs/schemas/delivery.example.json` to your asset’s `delivery.json`, then replace every example value. Required keys: id, title, production_status, release_status, provenance_type, shared_version, duration_seconds (null for stills/scouting), dimensions, fps (null for stills/scouting), outputs, variants, sources, credits, tests, unresolved_gates, toolchain, and notes. Every output entry includes a relative path, role, byte size, and SHA-256. Inventory every required concrete file except delivery.json itself; do not attempt a self-referential hash. state.json is live workflow state and is not part of the immutable output inventory. Variants list concrete paths and local timeline ranges where relevant. A source entry links to the copied original or source record and classifies the relationship (literal excerpt, teaching illustration, real capture, historical original, derivative crop, stock candidate).

`evidence/provenance.json` records source files and exact line ranges/hash, provenance classification, authored additions, and any producer decisions. `evidence/source-excerpts.md` preserves the relevant input excerpts. `evidence/claim-checks.json` maps every assigned R gate to status, evidence paths, and an approval/decision record; a gate cannot disappear because the artist ignored it. An applicable gate may be approved, blocked, or explicitly not applicable with a reason and review, never auto-cleared by the mere existence of the source script.

`qa.md` records tests actually run, results, full-size/720p proof paths, content checks, remaining blockers, and reviewer. An unchecked copied checklist is not a passed QA report. Record the exact renderer/capture/compiler commands and versions. This pack’s validators inspect structure and selected machine-checkable conditions, not visual quality or historical/legal truth.

## Required exports
Generated stills have an editable SVG or offline HTML source as specified, a 1920×1080 poster PNG, and named variant PNGs. Motion/code cards also have offline HTML, timeline JSON, a review MP4, and start/middle/end PNGs. Named cuts for DIA-02 and DIA-08 get separate MP4s so the editor can reuse dealing/award sequences. All other named variants are still states unless the ticket explicitly requests additional motion. A local renderer/encoder capability is needed; source-only work is recorded as partial/blocked, not completed media.

A source-based diagram or code screenshot can contain exact content without pretending to be a live recording. Keep literal code excerpts separately. Captures preserve real raw screenshots and transcripts; program runs also retain the exact copied Program.vb. `stderr.txt` may legitimately be empty when the run succeeds. `project-diff.txt` may be empty only if the recorded project did not need edits; no file is omitted just because its content is empty.

Archives retain an acquired native original, source.json, rights.json, and an editorial-frame PNG. A source record contains creator, title, original/publication date, depicted-event date (separate), exact source URL, access date, version/model evidence, original dimensions, transformations, license/permission terms and URL, rights status, and credit text. Unknown dates are null/unknown, not invented.

Stock scouting delivers a ranked candidate report, structured candidates, and a handoff. It does not require a video download when access is gated. Each candidate names its inspected shot, source URL, creator, duration, native size, proposed source in/out, license evidence, access barrier, and acquisition status. A no-match result is explicit. Actual downloaded footage, when permitted, is preserved as additional original media; never remove watermarks or bypass restrictions.

## Distinguish workflow state from release
Production statuses: planned, in_progress, produced, blocked, scouted, no_match. Release statuses: unreviewed, blocked, approved, not_applicable. A still with an unverified historical caption can be produced as a proof while release remains blocked. A scouted B-roll URL is not an acquired video.

**A dependency is satisfied once it is produced.** Dependents may proceed as soon as the upstream ticket reaches `produced`; they do not wait for release approval.

**Editorial gates are agent work.** Each worker checks its ticket's flagged claims against primary sources, records evidence in `evidence/claim-checks.json`, and fixes the asset or `War/SCRIPT.md` when the claim is wrong. A question that evidence cannot settle becomes a **review question** handed to the producer for the review deck (OPS-04).

**Release approval comes from the review deck**, not per-asset producer sign-off. The producer collects all produced assets and their review questions into the OPS-04 review deck; Devin approves or requests changes there. Until that review, release stays `unreviewed` or `blocked`.

The asset owner updates its state file. Do not authorize yourself to resolve a rights/payment/publication question. Production coordination may continue around blocked assets and must report exceptions rather than dropping them silently.

## QA tools
`python tools/validate_pack.py` validates the planning package: source hashes, ID/path uniqueness, original-plan and script coverage, line ranges, dependencies, cycles, and fixture integrity. It does not require future media to exist.

`python tools/validate_delivery.py --id CODE-02` checks a claimed delivery against file requirements, metadata, hashes, output paths, PNG sizes, and literal source excerpts. It also flags unresolved gates when release is claimed approved. It does not perform OCR, judge image content, establish licenses, or fully decode MP4s. Use ffprobe/playback and manual proof review separately and record them in qa.md.

`python tools/dispatch.py --lane motion` lists eligible tickets based on current per-ticket states; it does not start agents or create cloud tasks. `--all` shows all tickets, including work waiting on dependencies. Read the full ticket before performing work.
