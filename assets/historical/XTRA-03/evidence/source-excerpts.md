# XTRA-03 — source excerpts and research evidence

## 1. Script anchor (hash-locked original)

`sources/SCRIPT.md` lines 63–71, unchanged. The working copy `War/SCRIPT.md` has the same visual cue at line 66, identical wording.

~~~~text
**[VISUAL: Black and white photo of Kemeny and Kurtz at Dartmouth, 1964. Old terminal hardware. Transition to a green-screen terminal showing BASIC code.]**

**NARRATION:**

To understand Visual Basic, you need to understand BASIC. Capital B, capital A, capital everything — it's an acronym. Beginner's All-purpose Symbolic Instruction Code. It was invented in 1964 at Dartmouth College by John Kemeny and Thomas Kurtz, and its entire reason for existing was that programming was too hard.

**[VISUAL: Side-by-side comparison — a simple program in FORTRAN vs. the same thing in BASIC. The BASIC version is visibly shorter and more readable.]**

In 1964, if you wanted to write a program, you were probably writing FORTRAN or COBOL or assembly language. You were probably punching cards. The learning curve was brutal. Kemeny and Kurtz wanted something that a college freshman with no technical background could sit down and start using. So they made BASIC.
~~~~

This ticket fills only "Old terminal hardware". HIST-04 owns the Kemeny and Kurtz photograph; its folder held only a planning `state.json` when checked (2026-09-15), so there is no duplicate.

## 2. What terminals Dartmouth actually used (primary evidence)

**A. Dartmouth College Computation Center, *The Dartmouth Time-Sharing System: A Brief Description*, 19 October 1964.** Scan of the original on Wikimedia Commons:
<https://commons.wikimedia.org/wiki/File:The_Dartmouth_Time-Sharing_System,_A_Brief_Description_-_October_19,_1964_(original).pdf>
(file URL `https://upload.wikimedia.org/wikipedia/commons/4/45/The_Dartmouth_Time-Sharing_System%2C_A_Brief_Description_-_October_19%2C_1964_%28original%29.pdf`; 6 pages; SHA-256 of the copy read on 2026-09-15: `653e0ebc10ff8f8e8f3bfdae71834637f4a08688fdc7beb309ca8b3a86d8274f`; not vendored here.)

- Page (1), "External Description": the remote consoles are "model 35 teletype machines".
- Page (2), hardware schematic: the terminal boxes are labelled "Model 35 Teletypes". The two computers are labelled Datanet-30 and GE-235.

**B. General Electric Computer Dept. Laboratory, Sunnyvale, same title, 26 March 1965**, "revised from" the 19 October 1964 Dartmouth publication. This is a retyped transcription on Commons, not a scan:
<https://upload.wikimedia.org/wikipedia/commons/0/0f/The_Dartmouth_Time-Sharing_System,_A_Brief_Description_-_October_19,_1964.pdf>
(SHA-256 of the copy read: `0c77c30c63219a946dca65f7996a268f22cc110892bb169ea98bd1026ef5a524`; PDF metadata: created 2019 in OpenOffice.)

- The GE revision widens the wording to "model 33/35 teletype machines".

**Reading.** In Dartmouth's own October 1964 description, the terminals are Teletype **Model 35**. By GE's March 1965 revision, the system description names **Model 33 or 35**. No source checked says which model was on the College Hall floor on 1 May 1964. The October 1964 document already names a GE-235. Dartmouth's "BASIC at 50" site (<https://www.dartmouth.edu/basicfifty/basic.html>, read 2026-09-15) says the 1963 NSF grant was for a GE-225. The narration in this range names neither computer, so no script change follows.

## 3. Genuine Dartmouth 1964 terminal photographs located (not acquired)

*Dartmouth Alumni Magazine*, November 1964 (Vol. 57, No. 2), "The Computer Revolution", pp. 26–29:
<https://archive.dartmouthalumnimagazine.com/article/1964/11/1/the-computer-revolution>

- p. 27: students at one of about six input-output stations in the former Commons dining hall, College Hall. By the October 1964 description these are Model 35 Teletypes.
- p. 28: a Computation Center supervisor with the Datanet-30; an engineering professor and a student at remote stations.
- p. 29: a senior programmer at central headquarters, College Hall, with the GE-235 console behind him.
- p. 3 masthead: published by the Dartmouth Secretaries Association, with "All publication rights reserved" and reprinting only by the editor's permission.
- The archive serves only 448×600 page and 896×600 spread thumbnails anonymously (larger sizes returned HTTP 403). That is too small for a 1080p frame, and there is no reproduction licence. **Not acquired**; it is recorded as the preferred permission route (see rights.json).

## 4. Chosen image: identity evidence

Wikimedia Commons, "File:ASR-33 at CHM.agr.jpg":
<https://commons.wikimedia.org/wiki/File:ASR-33_at_CHM.agr.jpg>

- Commons description (by the photographer): Teletype Corporation ASR-33 on display at the Computer History Museum.
- Author ArnoldReinhold, "Own work". Date 2 February 2014 (EXIF DateTime 2014:02:02 12:35:44, Apple iPhone 4S).
- Licence: CC BY-SA 3.0 Unported and GFDL 1.2 or later.
- Commons imageinfo API: SHA-1 `5df1ff6e74dd12536bd381955a1a440e62256a77`, 1,748,549 bytes, 3264×2448, uploaded 2014-02-10T23:37:59Z. The acquired file matches byte for byte.
- In-picture evidence: the museum card at the right edge is headed "ASR-33 Telet…" (the rest is cut off). Its partly visible first words match the CHM *Revolution* gallery label for the ASR-33 (<https://www.computerhistory.org/revolution/minicomputers/11/337/1934>, which gives "Date Introduced: 1964"). The machine has the Model 33 ASR's integrated paper-tape reader and punch, with START/STOP/FREE control, and the Model 33 keyboard.
- Contrary or confounding context kept visible, not cropped: a decal reading "TimeShare Corporation" on the platen cover. It shows the unit had a commercial time-sharing history unrelated to Dartmouth. The unit's manufacture date is not given at the source.
