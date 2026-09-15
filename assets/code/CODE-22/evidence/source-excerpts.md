## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:275–283

```text
    Sub GiveCardsToWinner(ByRef Pot() As Card, ByRef PotCount As Integer, ByRef Winner As Hand)
        Dim i As Integer

        For i = 0 To PotCount - 1
            AddCardToBottom(Winner, Pot(i))
        Next i

        PotCount = 0
    End Sub
```

## SCRIPT.md:499–513

```text
The `GiveCardsToWinner` subroutine at the end is simple — it walks the pot array and adds each card to the bottom of the winner's hand:

```vb
Sub GiveCardsToWinner(ByRef Pot() As Card, ByRef PotCount As Integer, ByRef Winner As Hand)
    Dim i As Integer
    For i = 0 To PotCount - 1
        AddCardToBottom(Winner, Pot(i))
    Next i
    PotCount = 0
End Sub
```

**[VISUAL: The pot cards sliding into the winner's hand, one at a time, at the bottom of the pile.]**

This is what determines the eventual outcome of the game. The order in which won cards get added to your hand affects what you'll play in future rounds, which affects who wins those rounds. War is deterministic after the shuffle — the outcome is sealed the moment the cards are dealt. There's no randomness during play. The only randomness is in the initial shuffle.
```
