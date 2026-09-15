## ASSET_PLAN.md:22–22

```text
| 7 | Deck building nested-loop animation (4×13 grid) | HTML grid filling in |
```

## SCRIPT.md:239–279

```text
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

**[VISUAL: Animated grid filling in — 4 columns (suits) × 13 rows (ranks), each cell lighting up as the loop hits it.]**

Let's pause and look at a few VB-specific things here.

First: `Sub`. Not `void`, not `function` — `Sub`. Short for "subroutine." In Visual Basic, there's a hard distinction between a `Sub`, which does something and doesn't return a value, and a `Function`, which does something and gives you back a result. In C-family languages, a function that returns nothing is just a function with a `void` return type. In VB, it's a completely different keyword.

**[VISUAL: Side-by-side comparison:]**
```
C#:    void BuildDeck(Card[] deck) { ... }
VB:    Sub BuildDeck(ByRef Deck() As Card) ... End Sub
```

Second: `ByRef`. See that in the parameter list? In VB, you had to explicitly say whether a parameter was passed by reference or by value. `ByRef` means the subroutine receives a pointer to the original — changes are visible to the caller. `ByVal` means it gets a copy. In classic VB4, the default was `ByRef` for everything, which was efficient but dangerous. It meant you could accidentally modify data the caller didn't expect you to touch.

**[VISUAL: Diagram — ByRef: arrow pointing from sub back to caller's variable. ByVal: a copy being made, arrow pointing to a separate box.]**

Third: look at the `For` loop syntax. `For Rank = 2 To 14`. Then at the end: `Next Rank`. That `Next Rank` is closing the loop and telling you what variable is being incremented. If you're used to C-style `for (int i = 0; i < 14; i++)`, this is going to look almost quaint. But there's something kind of nice about it — when you have nested loops, each `Next` names its variable, so you can see at a glance which loop is ending.

**[VISUAL: The nested loops with colored brackets showing which `Next` closes which `For`.]**
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
