## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:156–167

```text
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

## SCRIPT.md:341–360

```text
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
