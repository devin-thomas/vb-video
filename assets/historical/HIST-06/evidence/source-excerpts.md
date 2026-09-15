# HIST-06 — Source excerpts

Access date for every external source: 2026-09-15. Manual citations give the Internet Archive identifier, the OCR text file (`*_djvu.txt`), that file's SHA-256, and line numbers inside it. OCR errors are kept as found. Quotations are short and serve only as evidence; the manuals are not reproduced.

## 1 Asset plan (sources/ASSET_PLAN.md:91)

~~~~text
| 3 | C64 / Apple II / TRS-80 BASIC boot screens | Wikipedia articles for each machine | High — iconic images, widely available |
~~~~

## 2 Script (sources/SCRIPT.md:73–75)

~~~~text
And it worked. It worked incredibly well. Through the 1970s and 1980s, BASIC became the language that shipped with almost every home computer. Your Commodore 64 had BASIC. Your Apple II had Applesoft BASIC. Your TRS-80 had BASIC. When you turned on a home computer in 1982, you were usually staring at a BASIC prompt.

**[VISUAL: Boot screens of Commodore 64, Apple II, TRS-80 — all showing their BASIC prompts. Maybe a montage.]**
~~~~

The same wording is at War/SCRIPT.md:76 and :78 (checked; not edited).

## 3 Prompt characters

**Apple II Reference Manual: A reference manual for the Apple II and the Apple II Plus personal computers** (Christopher Espinosa, Apple, 1979). Internet Archive `apple-ii-ref-manual`, text `Image072217171023.duplex.merged_djvu.txt`, SHA-256 `d6d12d206117d5e9db78715a83ea15d5421ec04396f85349cb3887b91dfe0c4e`, lines 2049–2053 (GETLN, printed page 33).
https://archive.org/details/apple-ii-ref-manual

> …a right caret (>) indicates Apple Integer BASIC, a right bracket (]) is the prompt for Applesoft II BASIC…

**Applesoft BASIC Programming Reference Manual** (Apple Computer). Internet Archive `Applesoft_BASIC_Programming_Reference_Manual_Apple_Computer`, text `…_djvu.txt`, SHA-256 `2cc61e5251a07fe2df0dc1f799911753d83e44e7c06a9329e3b82147a77d404c`.
https://archive.org/details/Applesoft_BASIC_Programming_Reference_Manual_Apple_Computer

- Lines 3129–3130 (glossary, printed page 35): the right bracket "Is displayed when APPLESOFT is ready to accept another command."
- Lines 8725–8726 (firmware card appendix, page 107): "The prompt character ] tells you you're in APPLESOFT." Line 8721 gives > for Integer BASIC.

## 4 Statements on screen

Applesoft BASIC Programming Reference Manual (same file and hash as section 3):

- Lines 4184–4188: HOME "Moves cursor to upper left screen position within the scrolling window and clears all text within the window."
- Lines 4249–4252: INVERSE and NORMAL are among the commands "used to set video output modes."

These explain the image: HOME cleared the screen, INVERSE printed HELLO, WORLD! as green-bar inverse text, and NORMAL restored normal video before the listing.

## 5 What a cold start shows

Apple II Reference Manual (same file and hash as section 3), lines 2216–2239 (Autostart ROM RESET, printed page 36). Summary: on power-on the Autostart ROM performs a cold start, clears the screen, and displays a machine-name banner "top and center". The OCR text reads `‘‘APPLE II’`; the exact printed glyphs (II or ][) were not checked against the page scan. It then looks for a Disk II controller. With no controller, it starts the language in ROM, which is Applesoft II on an Apple II Plus.

Lines 1712–1714 (printed page 25): every Apple II Plus includes the Autostart ROM. Other Apple systems have the older Monitor ROM, whose RESET behaviour differs.

The selected image has no such banner, so it is not a boot screen.

## 6 Which Apple II had Applesoft in ROM

Apple II Reference Manual (same file and hash), lines 1812–1814 (page 27):

> The Apple II Plus is a standard Apple II computer with a Revision 1 board, an Autostart Moni- tor ROM, and the Applesoft II BASIC language in ROM in lieu of Apple Integer BASIC.

**Applesoft Language, Second Edition** (George H. Blackwood & Brian D. Blackwood, 1981). Internet Archive `aslse`, text `ApplesoftLanguage-SecondEdition_djvu.txt`, SHA-256 `2ce00bdf6e45e4ef1f349d994a36907699bddc590c8f288cd0a9e3dc02c5af68`.
https://archive.org/details/aslse

- Lines 403–406: the older Apple II came with Integer BASIC, with Applesoft as an accessory on ROM or cassette; the present II Plus has Applesoft as standard.
- Lines 684–685: "Most Apples in use now will be the Apple II Plus with autostart, or an Apple II Plus with the language card."

**Applesoft II Reference Manual ("Blue Book")** (Apple Computer, 1978). Internet Archive `asb-bluebook`, text SHA-256 `7e001993850463e8184a25be45d78cdae9e1382c7779c6ed5b2a31dfcaa0f7ba`. Consulted for the early cassette-loaded Applesoft: line 3669 describes loading Applesoft from tape before its prompt appears (the OCR time figure reads "14 minutes" and is unverified). Supporting evidence only; nothing in this asset depends on it.

## 7 Commons file page (preserved in evidence/source-page/)

Raw wikitext as fetched (`commons-wikitext.txt`):

~~~~text
== {{int:filedesc}} ==
{{Information
|Description=Applesoft BASIC
|Source={{own}} (Screenshot)
|Date=
|Author=<!-- software author / developer team -->
|Permission={{free screenshot|license=}}
|other_versions=
}}

== {{int:license-header}} ==
{{PD-self}}

[[Category:Text-only screenshots of BASIC]]
[[Category:Hello World source code]]
[[Category:Apple II screenshots]]
~~~~

Upload log (`commons-upload-log.json`): uploaded by Vadimr, 2008-08-30T15:46:55Z. The upload summary had `|Source=Screenshot` and the same empty Author placeholder. There is one file version, and later page edits were categories, bots, and structured data only (`commons-revisions.json`).
