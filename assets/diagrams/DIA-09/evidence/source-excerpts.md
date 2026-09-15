## ASSET_PLAN.md:24–24

```text
| 9 | Pot growth diagram (2→10→18 cards) | SVG bar/stack diagram |
```

## SCRIPT.md:449–489

```text
Inside, there's a pot — an array that collects all the cards at stake this round:

```vb
Dim Pot(HAND_CAPACITY * 2 - 1) As Card
Dim PotCount As Integer
```

**[VISUAL: A diagram of the "pot" — a growing pile between the two players.]**

The pot can theoretically hold every card in the game. In a normal round, it holds two cards. In a war, it holds ten. In a double war, eighteen. In theory, wars can chain indefinitely, though in practice it's extremely rare to go past three.

Then there's an inner `Do...Loop` — not a `Do While`, just `Do...Loop`, which is an infinite loop that we exit with `Exit Sub` when someone wins. Each iteration:

One — check if either player is out of cards. If you can't play, you lose, and the other player takes the pot.

Two — both players draw their top card. Both cards go into the pot.

Three — compare ranks.

If Player 1's rank is higher, Player 1 wins the pot. `Exit Sub`.
If Player 2's rank is higher, Player 2 wins the pot. `Exit Sub`.
If they're equal? War.

```vb
WarNumber = WarNumber + 1
WarCount = WarCount + 1

BurnCount = Math.Min(3, Math.Min(Player1.Count, Player2.Count))
For i = 1 To BurnCount
    Pot(PotCount) = DrawTopCard(Player1) : PotCount = PotCount + 1
    Pot(PotCount) = DrawTopCard(Player2) : PotCount = PotCount + 1
Next i
```

**[VISUAL: Step-by-step animation of a War sequence:]**
**Step 1: Two equal cards face up.**
**Step 2: Three face-down cards from each player.**
**Step 3: One face-up card from each player.**
**Step 4: Higher card takes everything.**

Each player burns up to three cards face-down — or fewer, if they don't have three left. Then the loop goes back to the top, draws again, and compares again. If it's another tie, another war. The pot keeps growing.
```

## SCRIPT.md:546–557

```text
```
Round 4: Player 1 plays 4 of Spades, Player 2 plays 4 of Diamonds.
        ** WAR! ** (war number 1 this round)
        War card - Player 1 plays 2 of Spades, Player 2 plays 2 of Hearts.
        ** WAR! ** (war number 2 this round)
        War card - Player 1 plays 9 of Diamonds, Player 2 plays Ace of Diamonds.
        Player 2 wins the round (18 cards).
```

**[VISUAL: Highlight the "18 cards" — that's a huge haul.]**

A double war — both players tied twice in a row before someone won. Eighteen cards in the pot. That's a third of the entire deck changing hands in a single round.
```

## Program.vb:207–208

```text
        Dim Pot(HAND_CAPACITY * 2 - 1) As Card
        Dim PotCount As Integer
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
