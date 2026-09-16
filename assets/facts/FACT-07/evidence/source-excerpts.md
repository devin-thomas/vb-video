# FACT-07 — source excerpts

Each figure on the card, with the captured stdout line it was read from (1-based line numbers; the stdout files are unchanged captures, hashes below).

## Run 1 — TERM-04 — `assets/captures/TERM-04/source/stdout.txt` (1297 lines, sha256 026ce1d7f0c592aab22d5f788b2a8b1ac37223dcad7fca3e44fbbd898c7a4fa0)

| Card cell | Value | Line | Captured text |
|---|---|---:|---|
| Rounds | 617 | 1295 | `Total rounds played : 617` |
| Wars | 26 | 1296 | `Total wars fought    : 26` |
| Winner | Player 1 | 1294 | `PLAYER 1 WINS THE WAR!` |
| How it ended | Player 2 ran out of cards in a war | 1291 | `Player 2 has no cards left for the war - Player 1 takes the pot.` |

## Run 2 — TERM-05 — `assets/captures/TERM-05/source/stdout.txt` (2144 lines, sha256 a94ee70d34f82f9aafa6f7732dc994fa27c6db5260c0d7162c9dc99932f88603)

| Card cell | Value | Line | Captured text |
|---|---|---:|---|
| Rounds | 1,056 | 2142 | `Total rounds played : 1056` |
| Wars | 10 | 2143 | `Total wars fought    : 10` |
| Winner | Player 2 | 2141 | `PLAYER 2 WINS THE WAR!` |
| How it ended | Normal round win | 2137 | `Round 1056: Player 1 plays 4 of Spades, Player 2 plays 5 of Spades.` |
| (last round) | — | 2137 | `Round 1056: Player 1 plays 4 of Spades, Player 2 plays 5 of Spades.` |

## Run 3 — TERM-06 — `assets/captures/TERM-06/source/stdout.txt` (332 lines, sha256 7db51b66f27a01d32325f366ec184ecd19a1ca2000e712e29a21a42438f091ce)

| Card cell | Value | Line | Captured text |
|---|---|---:|---|
| Rounds | 150 | 330 | `Total rounds played : 150` |
| Wars | 10 | 331 | `Total wars fought    : 10` |
| Winner | Player 2 | 329 | `PLAYER 2 WINS THE WAR!` |
| How it ended | Normal round win | 325 | `Round 150: Player 1 plays 5 of Clubs, Player 2 plays 6 of Spades.` |
| (last round) | — | 325 | `Round 150: Player 1 plays 5 of Clubs, Player 2 plays 6 of Spades.` |

## Run 4 — TERM-02 — `assets/captures/TERM-02/source/stdout.txt` (4165 lines, sha256 eea4e8792c7a2714316e23d2dd16b46320042b992bbb58e7b2dc4f7f59a397b6)

| Card cell | Value | Line | Captured text |
|---|---|---:|---|
| Rounds | 2,008 | 4163 | `Total rounds played : 2008` |
| Wars | 69 | 4164 | `Total wars fought    : 69` |
| Winner | Player 2 | 4162 | `PLAYER 2 WINS THE WAR!` |
| How it ended | Player 1 ran out of cards in a war | 4159 | `Player 1 has no cards left for the war - Player 2 takes the pot.` |

## Footer

Shortest run: 150 rounds (Run 3, TERM-06 line 330); longest run: 2,008 rounds (Run 4, TERM-02 line 4163).

## War/SCRIPT.md:574 (narration this card sits under)

```text
Every run is different because the shuffle is random. Sometimes it's over in 150 rounds. Sometimes it takes more than 2,000. The number of wars varies too — ten in one game, sixty-nine in another. But it always terminates.
```

## sources/SCRIPT.md:571 (frozen source, manifest reference)

```text
Every run is different because the shuffle is random. Sometimes it's over in 150 rounds. Sometimes it takes 500. The number of wars varies too — sometimes just a handful, sometimes twenty or more. But it always terminates.
```
