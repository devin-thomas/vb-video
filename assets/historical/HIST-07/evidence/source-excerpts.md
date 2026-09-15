# HIST-07 source excerpts

Verbatim excerpts. Project sources are copied unchanged from the hash-locked `sources/` folder. External excerpts are quoted only as far as needed to verify identity, and each one is labeled with where it came from.

## 1. Project sources (hash-locked)

### sources/SCRIPT.md:73–75
sha256 `3821db546c8b3d64423336d73d8ed2b891611f39cadc51b04db4b4f547919acb`

~~~~text
And it worked. It worked incredibly well. Through the 1970s and 1980s, BASIC became the language that shipped with almost every home computer. Your Commodore 64 had BASIC. Your Apple II had Applesoft BASIC. Your TRS-80 had BASIC. When you turned on a home computer in 1982, you were usually staring at a BASIC prompt.

**[VISUAL: Boot screens of Commodore 64, Apple II, TRS-80 — all showing their BASIC prompts. Maybe a montage.]**
~~~~

The same text appears at `War/SCRIPT.md:76–78` (read-only check; not edited).

### sources/ASSET_PLAN.md:91
sha256 `8f1769aacb6f446a00cdb72655a60475f7fa692b2f274effe3c517d33c20eef7`

~~~~text
| 3 | C64 / Apple II / TRS-80 BASIC boot screens | Wikipedia articles for each machine | High — iconic images, widely available |
~~~~

## 2. Acquired image: on-screen text (worker transcription)

Read from `source/original.jpg` at native resolution (TRS-80 monitor, right-hand machine in the photo). I checked it at 1:1 and at 4× nearest-neighbour on 2026-09-15. This is a transcription, not OCR:

~~~~text
MEMORY SIZE?
MEMORY SIZE?
RADIO SHACK LEVEL II BASIC
READY
>?MEM
 31956
READY
>_
~~~~

**What the screen shows:** a short interactive session after power-up, not a clean boot screen.
- Lines 1–4 (`MEMORY SIZE?`, `RADIO SHACK LEVEL II BASIC`, `READY`) are the power-up text documented in the 1978 Level II manual (section 4). `MEMORY SIZE?` appears twice, which suggests a reset or re-prompt. The manual's sequence shows it once.
- Lines 5–8 are **not** part of the documented power-up text. Someone typed the command `?MEM` (`?` is Level II shorthand for PRINT; `MEM` returns free memory). BASIC printed the result ` 31956` with the leading space it gives positive numbers, then `READY` and the `>_` cursor.
- An earlier transcription in this record read line 5 as `>MEM`. That was wrong and is corrected here after the manager's 1:1 check.

The digits `31956` are soft at native resolution. Treat them as the best available reading, not a verified value. The narration does not rely on them.

## 3. Commons file description for File:Trinity77.jpg

Saved copy: `evidence/source-page/commons-file-page.wikitext.txt`. One email address in the description is redacted there and in the other saved page copies.

- description (en): the photo shows the three computers Byte Magazine called the "1977 Trinity": Commodore PET 2001, Apple II, TRS-80 Model I.
- date: `2019-05-25`; source: `{{own}}`; author: `[[User:Springsgrace|Tim Colegrove]]`
- license: `{{self|cc-by-sa-4.0}}`
- file history: 2019-05-26T03:12:09Z Springsgrace, "Cross-wiki upload from en.wikipedia.org", 3973×1853, sha1 `cbaeec4d22aaefe9ffc0ae7656cb0fa9e3adaf59`. Later versions, 2024-01-29 and 2024-01-30 by Pittigrilli, are distortion-corrected edits and were not used.

## 4. Primary documentation confirming the power-up prompt

### Radio Shack, *Level II BASIC Reference Manual*, 1st ed. (1978)
Internet Archive item `Level_II_BASIC_Reference_Manual_1st_Ed._1978_Radio_Shack`, OCR text file `Level_II_BASIC_Reference_Manual_1st_Ed._1978_Radio_Shack_djvu.txt`, lines 417 and 432. The OCR is lightly garbled.

~~~~text
memory size? - will appear on the screen.
...
RADIO SHACK LEVEL II BASIC
READY
~~~~

### Radio Shack, *TRS-80 Model I Preliminary Users Manual* (1977), Level I context
Internet Archive item `TRS80ModelIPreliminaryUsersManual`, OCR text lines 205 and 246.

~~~~text
Keyboard should light up and the screen should show READY.
...
complete course in Radio Shack's Level I BASIC.
~~~~

### Tandy, *TRS-80 Model III Manual* (1980), used for the rejected alternate candidate only
Internet Archive item `trs-80-model-iii-manual`, OCR text lines 621–668.

~~~~text
Cass?
...
Memory Size?
...
Radio Shack Model III Basic
(c) '80 Tandy
READY
~~~~
