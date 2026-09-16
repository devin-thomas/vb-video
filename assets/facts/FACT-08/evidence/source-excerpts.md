# FACT-08 — source excerpts

## Card copy — War/SCRIPT.md:624–626 (the cue), relabelled per docs/tickets/FACT-08.md

```text
**[VISUAL: Side-by-side comparison:
TERM-04: 2 cards → play 10 → burn 1 → empty → 4-card pot
TERM-02: 3 cards → play 8 → burn 2 → empty → 6-card pot]**
```

The ticket's exact copy replaces the capture IDs with run labels: "Run 1 · 617 rounds" (TERM-04) and "Run 4 · 2,008 rounds" (TERM-02).

## Run 1 · 617 rounds — TERM-04 — `assets/captures/TERM-04/source/stdout.txt` (1297 lines, sha256 026ce1d7f0c592aab22d5f788b2a8b1ac37223dcad7fca3e44fbbd898c7a4fa0)

| Step | Card | Check | Evidence |
|---|---|---|---|
| hand | 2 cards | reconstructed: Player 1 50, Player 2 2 going into round 617 | every `wins the round (N cards)` line up to line 1288 |
| play | play 10 | both played rank 10 | line 1289: `Round 617: Player 1 plays 10 of Diamonds, Player 2 plays 10 of Spades.` |
| burn | burn 1 | min(3, 2 − 1) = 1 | Program.vb:264 `BurnCount = Math.Min(3, Math.Min(Player1.Count, Player2.Count))` |
| empty | empty | 2 − 1 − 1 = 0 | line 1291: `Player 2 has no cards left for the war - Player 1 takes the pot.` |
| pot | 4-card pot | 2 played + 2 × 1 burned = 4 | same lines; Player 1 takes the pot |
| rounds | 617 rounds | total | line 1295: `Total rounds played : 617` |

Reconstruction: 2 cards → play 10 → burn 1 → empty → 4-card pot — matches the script.

## Run 4 · 2,008 rounds — TERM-02 — `assets/captures/TERM-02/source/stdout.txt` (4165 lines, sha256 eea4e8792c7a2714316e23d2dd16b46320042b992bbb58e7b2dc4f7f59a397b6)

| Step | Card | Check | Evidence |
|---|---|---|---|
| hand | 3 cards | reconstructed: Player 1 3, Player 2 49 going into round 2008 | every `wins the round (N cards)` line up to line 4156 |
| play | play 8 | both played rank 8 | line 4157: `Round 2008: Player 1 plays 8 of Diamonds, Player 2 plays 8 of Clubs.` |
| burn | burn 2 | min(3, 3 − 1) = 2 | Program.vb:264 `BurnCount = Math.Min(3, Math.Min(Player1.Count, Player2.Count))` |
| empty | empty | 3 − 1 − 2 = 0 | line 4159: `Player 1 has no cards left for the war - Player 2 takes the pot.` |
| pot | 6-card pot | 2 played + 2 × 2 burned = 6 | same lines; Player 2 takes the pot |
| rounds | 2,008 rounds | total | line 4163: `Total rounds played : 2008` |

Reconstruction: 3 cards → play 8 → burn 2 → empty → 6-card pot — matches the script.

## War/SCRIPT.md:580 (section title used as the kicker)

```text
## SECTION 12: WHEN THE CARDS RUN OUT
```

## sources/SCRIPT.md:267 (frozen source, manifest reference)

```text
**[VISUAL: Side-by-side comparison:]**
```
