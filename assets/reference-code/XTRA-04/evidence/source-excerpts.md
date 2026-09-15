# XTRA-04 — source excerpts

## SCRIPT.md:69–71 (hash-locked `sources/SCRIPT.md`)

```text
**[VISUAL: Side-by-side comparison — a simple program in FORTRAN vs. the same thing in BASIC. The BASIC version is visibly shorter and more readable.]**

In 1964, if you wanted to write a program, you were probably writing FORTRAN or COBOL or assembly language. You were probably punching cards. The learning curve was brutal. Kemeny and Kurtz wanted something that a college freshman with no technical background could sit down and start using. So they made BASIC.
```

The working script `War/SCRIPT.md` carries the same two paragraphs at lines 72 and 74 (checked 2026-09-15). This ticket does not edit either file.

## Authored programs shown on screen

These were written for this production. They are illustrative and were not run.

`src/excerpt-fortran2.f` — FORTRAN II for the IBM 7090/7094 (card columns preserved):

```text
      PRINT 1
    1 FORMAT (6H HELLO)
      CALL EXIT
      END
```

`src/excerpt-dartmouth.bas` — Dartmouth BASIC, October 1964:

```text
10 PRINT "HELLO"
20 END
```

## Primary documentation consulted (short citations; page numbers are the printed ones)

Scans were read page by page from public archive copies (URLs in `provenance.json`). Nothing from them is stored in this repository.

### IBM 7090/7094 Programming Systems: FORTRAN II Programming, form C28-6054-5

- p.5 — each statement goes on its own card; numbers go in columns 1–5; a C in column 1 marks a comment. Figure 1-1 ends with `CALL EXIT` and `END`, and its FORMAT uses `22H1THE LARGEST OF THESE` (carriage-control character inside the H field).
- p.6 — column 6 is for continuation; statements are punched in columns 7–72; blanks are ignored except in column 6 and in certain FORMAT fields.
- p.16 — STOP is "STOP" or "STOP n"; STOP and PAUSE should not be used under the FORTRAN Monitor or IBSYS. END "must be the last statement in the program"; plain `END` is a listed example.
- p.19 — FORMAT is nonexecutable; nine I/O statements carry a list of quantities.
- p.21 — `wH` is followed by w characters; blanks count as part of w. Example: `24H THIS IS ALPHAMERIC DATA`.
- p.22 — the FORMAT is used with an I/O list "except when a FORMAT statement consists entirely of alphameric fields". Under Program Control the first character of each record controls spacing and is not printed; blank means single space; this is required for PRINT.
- p.24 — PRINT general form: `PRINT n, List`, n being a FORMAT statement number; output goes to the on-line printer.
- p.34 — programs run under the Monitor "must be terminated by a CALL EXIT or CALL DUMP statement"; the END card is still necessary.
- p.40 — END may be written plain, or with option indicators `END (I1, ..., I15)`; it must be physically last.
- p.46 (Appendix B) — the source character set includes A–Z, 0–9, blank, `(`, `)`.

### IBM 7090/7094 Programming Systems: FORTRAN IV Language, form C28-6274-2 (pages revised 6/10/64)

- p.21.1 — PRINT and PUNCH "require both a reference to a FORMAT statement and an output list". This is why the listing is labelled FORTRAN II, not FORTRAN IV.

### BASIC, Dartmouth College Computation Center, 1 October 1964

- Title page — "A Manual for BASIC, the elementary algebraic language designed for use with the Dartmouth Time Sharing System."
- p.3 (§2.1) — the first complete example numbers its lines 10–90, ends `90 END`, and includes `65 PRINT "NO UNIQUE SOLUTION"` (the manual prints the letter O with a slash).
- p.28 (§2.6.3) — PRINT forms include `<line number> PRINT "<any string of characters>"`.
- p.30 (§2.6.6) — "An END statement is required in all programs"; it must have the highest line number.
- p.31 (§3.1) — rule 1: a label in quotes is printed just as it appears.
- p.56 (Appendix C) — every statement begins with a line number; PRINT is one of the 15 statements.
