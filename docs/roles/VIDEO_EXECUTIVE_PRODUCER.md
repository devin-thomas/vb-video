# Video Executive Producer

You finish the Visual Basic War video unattended and leave Devin a finished review cut, a 4K master, captions, and upload metadata by morning. Repository: `C:\dev\youtube\vb-video-checkout-2` (main, pushed; GitHub `devin-thomas/vb-video`). Devin is asleep: he cannot answer questions, so decide as the producer would (see `docs/roles/PRODUCER.md` and the log's session 8: Devin delegated release judgement, rights are settled, never bring him a rights question) and write everything you decided into `docs/INTEGRATION_LOG.md`.

## State when you start (2026-09-16, about 23:30)

- Asset production is complete: 134/134 tickets produced and release-approved; editor inventory under `assets/ops/OPS-04/exports/`.
- **Narration** is being synthesized by `tools/narration/synth.py` (Qwen3-TTS, speaker `aiden`, on this machine's RTX 4090). Progress is in `narration/synth.log`; it ends with a line `done`. Takes live in `narration/takes/<beat>/01/`. If the log has no `done` and no python process is running `synth.py`, rerun `python tools/narration/synth.py` from the repo root; it resumes and skips finished beats.
- **QA** (`tools/narration/qa.py`, runs in `E:\local-llm\models\narration-tts\envs\asr\Scripts\python.exe`) may still be running from the previous session; check `tasklist | findstr python` and the mtime of `narration/qa.json` before starting another, so two runs never write the file at once.
- **Screen recordings** are done (`recordings/`), **sound effects** are acquired and placed (`assets/audio/sfx/`, `narration/sfx.json`), **music** is chosen and planned from Devin's keeps (`assets/audio/music/`, `narration/music-plan.json`, `narration/sfx-music.json`, all CC0 or CC BY). Blast Processor and Inverse Phase keeps are held for permission requests later; do not use them.
- A silent captioned preview already exists at `build/silent-captioned-1080p60.mp4`; the section 1 mix test is `build/review-1080p60-s1-mixed.mp4` (bed about 8 dB under the voice on chapter cards, ducked under narration, whole mix about -16 LUFS).

## The job, in order

1. Wait for narration to finish (`done` in `narration/synth.log`).
2. Run `bash tools/assembly/finish.sh` from the repo root. It runs QA on every take, `tools/narration/select.py`, regenerates flagged beats as attempt 02 and re-selects, rebuilds `narration/timeline.json`, captions, music plan and effect cues, renders `build/review-1080p60-mixed.mp4`, writes `build/upload-metadata.md`, then renders `build/master-2160p60.mp4`. Expect 40 to 60 minutes. If a step fails, read the error, fix the script (they are small), and rerun the step; the render caches segments.
3. Verify: `narration/timeline.json` shows `beats_without_audio: []`; `ffprobe` both renders (1920x1080 and 3840x2160, 60 fps, duration about 42 minutes); loudness of the mixed review with `ffmpeg -af ebur128 -f null -` near -16 LUFS integrated and true peak under -0.5 dBFS; extract a 3x3 contact sheet (`-vf "fps=1/280,scale=480:-1,tile=3x3"`) and look at it with the Read tool; extract 20 seconds from the middle of section 10 and confirm audio is present. Check `narration/selection.json` for beats still flagged after attempt 02 and list them in the log; do not chase them further.
4. Record: commit `narration/*.json`, `build/captions.srt`, `build/captions.vtt`, `build/transcript.md`, `build/upload-metadata.md` (force-add the build files, `build/` is ignored), and a **Session 9** entry in `docs/INTEGRATION_LOG.md` (what ran, counts, flagged beats, decisions, file paths and sizes). Push `main`.
5. Write `build/MORNING-REPORT.md` for Devin: where the files are, running time, what he should watch for (the flagged beats by timestamp, the music placements), and the two things only he can do: watch the review cut, and upload with `build/upload-metadata.md` and `build/captions.srt`. Then update the status page: read `https://claude.ai/artifact/CMiNc1DppbcY5k266peSHy` with the Artifact tool, edit its "What happens next" list to say the cut is rendered and where, republish to the same URL.

## Rules that hold overnight

- Never switch branches in this checkout; commit on `main`.
- Render with `C:\Python314\python.exe` (the default `python`); never prepend the MSYS2 bin to PATH (it shadows python). Renderers use `h264_nvenc`/`hevc_nvenc`; the GPU is free once narration finishes.
- Do not download anything new, upload anything, create accounts, or contact artists. If music or an effect file is missing, drop that cue and note it.
- Do not edit `War/SCRIPT.md`, `sources/`, or any asset under `assets/<family>/<ID>/`.
- The narration text is final; if a beat is unfixable after attempt 02, keep the better take and log it.
- Leave `recordings/`, `narration/takes/`, `build/*.mp4` uncommitted (size); everything else that changed, commit.
- If the machine is asleep or the GPU job dies, restart the step; nothing here is destructive.
