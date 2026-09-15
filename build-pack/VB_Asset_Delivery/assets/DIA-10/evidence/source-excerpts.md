## ASSET_PLAN.md:25–25

```text
| 10 | Game flowchart (Build→Shuffle→Deal→Loop→Winner) | SVG flowchart |
```

## SCRIPT.md:388–420

```text
The main game loop is where everything comes together. Let's walk through `Sub Main`:

```vb
BuildDeck(Deck)
ShuffleDeck(Deck)

Player1 = NewHand()
Player2 = NewHand()
DealCards(Deck, Player1, Player2)
```

We build a deck, shuffle it, create two empty hands, and deal — alternating cards, one to Player 1, one to Player 2, until all 52 are distributed. Each player gets 26.

**[VISUAL: Animation — a deck splitting into two piles, cards alternating left and right.]**

Then the loop:

```vb
Do While Player1.Count > 0 And Player2.Count > 0
    RoundNumber = RoundNumber + 1
    If RoundNumber > MAX_ROUNDS Then
        ' Safety valve — call it a draw
        Exit Do
    End If
    PlayRound(RoundNumber, Player1, Player2, WarCount)
Loop
```

`Do While...Loop`. In C, that's `while (...) { }`. It keeps going as long as both players have at least one card. When either player hits zero, the loop ends and we have a winner.

**[VISUAL: Flowchart — "Both have cards?" → Yes → Play round → loop back. No → Determine winner.]**

The `MAX_ROUNDS` check is a safety valve. War is theoretically capable of cycling forever — the same cards going back and forth in a loop. In practice, with a random shuffle, games almost always end in a few hundred rounds. But just in case, we cap it at 20,000 rounds and call it a draw. In my testing, I've never actually hit the cap.
```

## SCRIPT.md:460–489

```text
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

## Program.vb:44–94

```text
        BuildDeck(Deck)
        ShuffleDeck(Deck)

        Player1 = NewHand()
        Player2 = NewHand()
        DealCards(Deck, Player1, Player2)

        Console.WriteLine("Cards dealt: Player 1 has " & Player1.Count & _
            ", Player 2 has " & Player2.Count & ".")
        Console.WriteLine()

        RoundNumber = 0
        WarCount = 0
        TheWinner = 0

        Do While Player1.Count > 0 And Player2.Count > 0
            RoundNumber = RoundNumber + 1

            If RoundNumber > MAX_ROUNDS Then
                Console.WriteLine()
                Console.WriteLine("No winner after " & MAX_ROUNDS & _
                    " rounds - calling it a draw (deck cycle detected).")
                TheWinner = 0
                Exit Do
            End If

            PlayRound(RoundNumber, Player1, Player2, WarCount)
        Loop

        Console.WriteLine()
        Console.WriteLine("=====================================")

        If Player1.Count = 0 And Player2.Count > 0 Then
            TheWinner = 2
        ElseIf Player2.Count = 0 And Player1.Count > 0 Then
            TheWinner = 1
        End If

        Select Case TheWinner
            Case 1
                Console.WriteLine("PLAYER 1 WINS THE WAR!")
            Case 2
                Console.WriteLine("PLAYER 2 WINS THE WAR!")
            Case Else
                Console.WriteLine("THE WAR ENDS IN A DRAW.")
        End Select

        Console.WriteLine("Total rounds played : " & RoundNumber)
        Console.WriteLine("Total wars fought    : " & WarCount)
        Console.WriteLine("=====================================")
    End Sub
```

## Program.vb:218–270

```text
        Console.Write("Round " & RoundNumber & ": ")

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
            End If
        Loop
```
