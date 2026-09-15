## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:97–111

```text
    Sub BuildDeck(ByRef Deck() As Card)
        Dim Suits() As Char = {"S"c, "H"c, "D"c, "C"c}
        Dim Rank As Integer
        Dim SuitIndex As Integer
        Dim Index As Integer

        Index = 0
        For Rank = 2 To 14
            For SuitIndex = 0 To 3
                Deck(Index).Rank = Rank
                Deck(Index).Suit = Suits(SuitIndex)
                Index = Index + 1
            Next SuitIndex
        Next Rank
    End Sub
```

## SCRIPT.md:235–259

```text
**[VISUAL: The `BuildDeck` subroutine on screen.]**

**NARRATION:**

Next, we need a deck. Fifty-two cards: thirteen ranks times four suits.

```vb
Sub BuildDeck(ByRef Deck() As Card)
    Dim Suits() As Char = {"S"c, "H"c, "D"c, "C"c}
    Dim Rank As Integer
    Dim SuitIndex As Integer
    Dim Index As Integer

    Index = 0
    For Rank = 2 To 14
        For SuitIndex = 0 To 3
            Deck(Index).Rank = Rank
            Deck(Index).Suit = Suits(SuitIndex)
            Index = Index + 1
        Next SuitIndex
    Next Rank
End Sub
```

Two nested `For` loops. The outer loop walks through ranks 2 to 14. The inner loop walks through the four suits. We drop each card into the array at the current index and bump the index. After both loops finish, we have a perfectly ordered 52-card deck.
```
