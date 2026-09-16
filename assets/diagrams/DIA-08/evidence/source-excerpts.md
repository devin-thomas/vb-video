## ASSET_PLAN.md:23–23

```text
| 8 | War mechanic step-by-step | SVG — 4-panel sequence |
```

## SCRIPT.md:188–192

```text
Three. If both players flip the same rank — two sevens, two kings, whatever — it's War. Each player places three cards face-down, then flips a fourth card face-up. Whoever's face-up card is higher takes the entire pot — all ten cards. If it's another tie, you do it again. War can chain.

**[VISUAL: Animation — two equal cards appear, then three face-down cards from each player, then two more face-up cards. The pot grows.]**

Four. You keep playing until one player has all 52 cards. That player wins. If a player can't put up enough cards for a war, they lose.
```

## SCRIPT.md:483–489

```text
**[VISUAL: Step-by-step animation of a War sequence:]**
**Step 1: Two equal cards face up.**
**Step 2: Three face-down cards from each player.**
**Step 3: One face-up card from each player.**
**Step 4: Higher card takes everything.**

Each player burns up to three cards face-down — or fewer, if they don't have three left. Then the loop goes back to the top, draws again, and compares again. If it's another tie, another war. The pot keeps growing.
```

## Program.vb:234–268

```text
            Card1 = DrawTopCard(Player1)
            Card2 = DrawTopCard(Player2)
            Pot(PotCount) = Card1 : PotCount = PotCount + 1
            Pot(PotCount) = Card2 : PotCount = PotCount + 1

            If WarNumber = 0 Then
                Console.WriteLine("Player 1 plays " & CardText(Card1) & _
                    ", Player 2 plays " & CardText(Card2) & ".")
            Else
                Console.WriteLine("        War card - Player 1 plays " & CardText(Card1) & _
                    ", Player 2 plays " & CardText(Card2) & ".")
            End If

            If Card1.Rank > Card2.Rank Then
                Console.WriteLine("        Player 1 wins the round (" & PotCount & " cards).")
                GiveCardsToWinner(Pot, PotCount, Player1)
                Exit Sub

            ElseIf Card2.Rank > Card1.Rank Then
                Console.WriteLine("        Player 2 wins the round (" & PotCount & " cards).")
                GiveCardsToWinner(Pot, PotCount, Player2)
                Exit Sub

            Else
                ' Tie: it's WAR. Each side burns up to 3 face-down cards,
                ' then both flip a new card to compare.
                WarNumber = WarNumber + 1
                WarCount = WarCount + 1
                Console.WriteLine("        ** WAR! ** (war number " & WarNumber & " this round)")

                BurnCount = Math.Min(3, Math.Min(Player1.Count, Player2.Count))
                For i = 1 To BurnCount
                    Pot(PotCount) = DrawTopCard(Player1) : PotCount = PotCount + 1
                    Pot(PotCount) = DrawTopCard(Player2) : PotCount = PotCount + 1
                Next i
```

## Revision 2 — the `endgame` cutdown (round 617 of the first recorded run)

The numbers in the `endgame` variant come from the captured stdout of the 617-round run, the same capture FACT-07 and FACT-08 use: `assets/captures/TERM-04/source/stdout.txt` (SHA-256 `026ce1d7f0c592aab22d5f788b2a8b1ac37223dcad7fca3e44fbbd898c7a4fa0`, 1297 lines, buffer-verified against the live console in `TERM-04/evidence/capture.json`). Line numbers are 1-based.

### TERM-04/source/stdout.txt:5 — the deal

```text
Cards dealt: Player 1 has 26, Player 2 has 26.
```

### TERM-04/source/stdout.txt:1285–1291 — the last three rounds and the ending

```text
Round 615: Player 1 plays King of Diamonds, Player 2 plays 4 of Spades.
        Player 1 wins the round (2 cards).
Round 616: Player 1 plays 10 of Spades, Player 2 plays Jack of Spades.
        Player 2 wins the round (2 cards).
Round 617: Player 1 plays 10 of Diamonds, Player 2 plays 10 of Spades.
        ** WAR! ** (war number 1 this round)
Player 2 has no cards left for the war - Player 1 takes the pot.
```

### TERM-04/source/stdout.txt:1293–1297 — the result banner

```text
=====================================
PLAYER 1 WINS THE WAR!
Total rounds played : 617
Total wars fought    : 26
=====================================
```

### Hand sizes entering round 617 (derived, not printed)

The program never prints hand sizes after the deal, so the 50 / 2 split was replayed from the capture: starting from 26 / 26 (line 5), every `Player N wins the round (M cards).` line moves M/2 cards from the loser to the winner, because both players contribute the same number of cards to every pot (one played card each, then `BurnCount` from each hand — `Program.vb:264` — then one war card each). Replaying lines 7–1288 in order gives Player 1 = 50 and Player 2 = 2 before line 1289 (Player 1 = 51 / Player 2 = 1 before round 616, which Player 2 won for 2 cards). The replay script is quoted in qa.md.

From that state, `Program.vb` gives the four stages exactly as drawn:

- Both play a 10 (line 1289): Player 1 49, Player 2 1, pot 2. Equal ranks, so `** WAR! **` (line 1290; `Program.vb:258–262`).
- `BurnCount = Math.Min(3, Math.Min(Player1.Count, Player2.Count))` = `Math.Min(3, Math.Min(49, 1))` = 1 (`Program.vb:264`): each side burns one card face-down. Player 1 48, Player 2 0, pot 4. The burned identities are not printed, so the burns stay face-down in the asset.
- The `Do` loop returns to its top; `Player1.Count` is 48, so the first check passes, and `Player2.Count = 0` fires (`Program.vb:228–231`), printing line 1291 and giving the four pot cards to Player 1 in pot order (`GiveCardsToWinner`, `Program.vb:275–283`): Player 1 52, Player 2 0, pot 0. Line 1294 confirms the winner.

### Program.vb:220–232 — the empty-hand checks at the top of the war loop

```text
        Do
            ' A player who has run out of cards mid-war loses immediately.
            If Player1.Count = 0 Then
                Console.WriteLine("Player 1 has no cards left for the war - Player 2 takes the pot.")
                GiveCardsToWinner(Pot, PotCount, Player2)
                Exit Sub
            End If

            If Player2.Count = 0 Then
                Console.WriteLine("Player 2 has no cards left for the war - Player 1 takes the pot.")
                GiveCardsToWinner(Pot, PotCount, Player1)
                Exit Sub
            End If

```

### Narration the stages land on (narration/beats.json, section 12)

- S12-B03: "Going into round 617, Player 2 had exactly 2 cards left — against Player 1's 50. Both played a 10: tie, war. […] But Player 2 only had 1 card left after playing that 10."
- S12-B04: "Player 2 had 1, so both players burned 1. After the burn, Player 2's hand was empty. The loop came back to the top, hit the empty-hand check, and that was it — Player 1 took the four-card pot and the game."

The capture agrees with the ticket's numbers (2 vs 50; 10 and 10; 1 vs 49; burn 1 each; 0 vs 48; a 4-card pot to Player 1), so no review question arises from the figures.
