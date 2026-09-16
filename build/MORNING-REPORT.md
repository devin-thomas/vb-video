# Morning report — the Visual Basic War video is cut

Finished overnight on 2026-09-16 by the Video Executive Producer session. Running time **42:00**. Nothing was uploaded.

## Where the files are

| File | What it is | Size |
|---|---|---|
| `build/review-1080p60-mixed.mp4` | The cut to watch: 1080p60, narration, music beds, effects | 289 MB |
| `build/master-2160p60.mp4` | The upload master: 4K60 HEVC, same audio | 660 MB |
| `build/captions.srt`, `build/captions.vtt` | 553 caption cues from the written script | |
| `build/upload-metadata.md` | Title, description, tags, 17 chapters at the real times | |
| `build/transcript.md` | 6,102-word transcript | |

`build/pass1-*.mp4` are the first render before four assets were placed (see below). Delete them when you like.

## What was done

- Aiden read all 166 beats (39.4 min of voice). 63 beats were flagged by the transcription check and read a second time; the better take was chosen by measurement for each, and 32 of the second reads made the cut.
- The timeline has 183 segments and uses all 130 cleared assets. Four had been left off by the placement rules and were placed by producer judgement; look at them once: the Pentium-era PC at **5:45**, the runtime fact card at **29:01**, the 1995 tools comparison at **32:49**, the code scroll-through at **41:05**.
- Music: your eight keeps as section beds with chapter stings, ducked under the voice. Effects: Windows 95 chime at 4:58, shuffles at 9:12, 9:32 and 15:54, card slaps at 21:43 and 22:40.
- Checked by machine: both files run 42:00, the mix sits at -16.3 LUFS with true peak -0.8 dBFS (YouTube-safe), captions end with the last beat, and the 17 chapter times in the metadata match the chapter cards.

## What to listen for

The transcriber heard a different word on these beats. Most are the same sound written differently, but they are the places a misread would hide. Timestamps are for the review cut.

| Time | Beat | What was heard |
|---|---|---|
| 1:49 | S02-B02 | "COBOL" as "cobalt" |
| 2:32 | S02-B04 | "learned" as "learn" |
| 5:28 | S03-B02 | "disc" as "disk" |
| 6:15 | S03-B05 | "BASIC" as "basics" |
| 16:44 | S08-B01 | "queue" as "cue", "structures" as "structure's" |
| 17:52 | S08-B07 | "data sets" as "datasets" |
| 18:53 | S08-B12 | "assign" as "assigned" |
| 23:14 | S10-B12 | "pot array" as "potteray" |
| 23:23 | S10-B13 | "won" as "one" |
| 30:50 | S14-B04 | "preferred" as "prefer" |
| 35:25 | S15-B10 | ".WriteLine" as "writeline" |

Slow reads worth a glance: 4:17, 24:20, 30:16 and 38:32 sit just under 120 words a minute. The "fast" flags are all on beats shorter than six seconds and are not real.

## The two things only you can do

1. **Watch the review cut.** If a beat needs a re-read, say which; the chain regenerates and re-renders from `bash tools/assembly/finish.sh --force`.
2. **Upload** the master with `build/upload-metadata.md` and `build/captions.srt`.

## One note

The producer had also launched a background session with the same overnight brief. It went dormant behind a wait script that could not see the synthesis finish and had not woken by the time this report was written. If it wakes and runs the finish script, the script now sees a finished master and exits without rendering anything. You can stop that session in the app if it is still listed. Details are in `docs/INTEGRATION_LOG.md`, Session 9.
