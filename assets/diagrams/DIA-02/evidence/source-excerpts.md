## ASSET_PLAN.md:17–17

```text
| 2 | War game rules animation | HTML with CSS animations or multi-frame SVG |
```

## SCRIPT.md:170–194

```text
## SECTION 5: THE CARD GAME WAR — RULES IN 60 SECONDS

**[VISUAL: Animated diagram of a War game — two decks, cards flipping, a "pot" in the middle. Simple, clean, maybe hand-drawn style.]**

**NARRATION:**

Before we write any code, let's make sure we all know how War works, because you might not have played it since you were eight. Or maybe you've never played it at all. It's a children's card game — no strategy, no decisions, pure luck — which makes it perfect for a computer simulation, because there are no choices to model.

Here are the rules:

One. Take a standard 52-card deck and shuffle it. Deal it evenly — 26 cards to each player, face down. Neither player looks at their cards.

**[VISUAL: Animation — deck splits into two piles.]**

Two. Each round, both players flip their top card face-up at the same time. Whoever played the higher card takes both cards and puts them at the bottom of their pile. Aces are high — they beat everything.

**[VISUAL: Animation — two cards flip, the higher one "wins" and both slide to the bottom of a pile.]**

Three. If both players flip the same rank — two sevens, two kings, whatever — it's War. Each player places three cards face-down, then flips a fourth card face-up. Whoever's face-up card is higher takes the entire pot — all ten cards. If it's another tie, you do it again. War can chain.

**[VISUAL: Animation — two equal cards appear, then three face-down cards from each player, then two more face-up cards. The pot grows.]**

Four. You keep playing until one player has all 52 cards. That player wins. If a player can't put up enough cards for a war, they lose.

That's it. No bluffing, no bidding, no trump suits. Just flip, compare, collect. A game a five-year-old can play — and a game that maps beautifully onto about 250 lines of code.
```

## SCRIPT.md:399–401

```text
We build a deck, shuffle it, create two empty hands, and deal — alternating cards, one to Player 1, one to Player 2, until all 52 are distributed. Each player gets 26.

**[VISUAL: Animation — a deck splitting into two piles, cards alternating left and right.]**
```

## Program.vb:136–152

```text
    Sub DealCards(ByRef Deck() As Card, ByRef Player1 As Hand, ByRef Player2 As Hand)
        Dim i As Integer

        For i = 0 To 51
            If i Mod 2 = 0 Then
                AddCardToBottom(Player1, Deck(i))
            Else
                AddCardToBottom(Player2, Deck(i))
            End If
        Next i
    End Sub

    ' Adds a card to the bottom (end) of a hand's queue.
    Sub AddCardToBottom(ByRef H As Hand, ByVal C As Card)
        H.Cards(H.Count) = C
        H.Count = H.Count + 1
    End Sub
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
