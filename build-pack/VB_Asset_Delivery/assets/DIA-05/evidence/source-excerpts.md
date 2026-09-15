## ASSET_PLAN.md:20–20

```text
| 5 | Array-as-queue animation | HTML with step-through JS or multi-frame SVG |
```

## SCRIPT.md:315–360

```text
Here's where things get interesting from a data structures perspective. Each player has a hand of cards, and that hand needs to behave like a queue — first in, first out. When you win cards, they go to the bottom of your pile. When you play a card, it comes off the top.

In C#, you'd use `Queue<Card>` and call it a day. In C++, you'd use `std::queue`. In 1995 VB? You didn't have generic collections. You didn't even have a built-in queue. You had arrays, and you had `ReDim`, and that was about it.

So we fake it:

```vb
Structure Hand
    Dim Cards() As Card
    Dim Count As Integer
End Structure
```

**[VISUAL: A visual diagram of the Hand structure — an array of 52 slots, with only the first N filled. An arrow labeled "Count" points to the boundary.]**

The hand is an array of 52 slots — the maximum possible, since you could theoretically hold all the cards — and a counter that tracks how many slots are actually in use. Cards zero through Count-minus-one are live. Everything past Count is garbage.

Adding a card to the bottom is simple — drop it at position Count and increment:

```vb
Sub AddCardToBottom(ByRef H As Hand, ByVal C As Card)
    H.Cards(H.Count) = C
    H.Count = H.Count + 1
End Sub
```

Drawing from the top is more expensive. You take the card at position zero, then shift everything else forward by one slot:

```vb
Function DrawTopCard(ByRef H As Hand) As Card
    Dim Top As Card
    Dim i As Integer

    Top = H.Cards(0)
    For i = 1 To H.Count - 1
        H.Cards(i - 1) = H.Cards(i)
    Next i
    H.Count = H.Count - 1

    DrawTopCard = Top
End Function
```

**[VISUAL: Animation — cards in a row. The leftmost card is removed, and all the others slide left to fill the gap.]**

That shift is O(n) — every card in the hand moves one position. With a proper circular buffer or a linked list, you could do this in O(1). But we're writing 1995 VB. Nobody was thinking about algorithmic complexity when they had 26 cards in a hand. Computers were slower, but data sets were tiny. The whole game finishes in a few hundred rounds, and each round shifts at most 52 cards. A Pentium 75 could handle this without breaking a sweat.
```

## Program.vb:23–26

```text
    Structure Hand
        Dim Cards() As Card
        Dim Count As Integer
    End Structure
```

## Program.vb:128–167

```text
    Function NewHand() As Hand
        Dim H As Hand
        ReDim H.Cards(HAND_CAPACITY - 1)
        H.Count = 0
        NewHand = H
    End Function

    ' Deals the 52-card deck alternately into the two hands, 26 apiece.
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

    ' Removes and returns the top card of a hand's queue, shifting the
    ' remaining cards up by one slot.
    Function DrawTopCard(ByRef H As Hand) As Card
        Dim Top As Card
        Dim i As Integer

        Top = H.Cards(0)
        For i = 1 To H.Count - 1
            H.Cards(i - 1) = H.Cards(i)
        Next i
        H.Count = H.Count - 1

        DrawTopCard = Top
    End Function
```
