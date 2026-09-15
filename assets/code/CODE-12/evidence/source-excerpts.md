## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:136–146

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
```

## SCRIPT.md:399–401

```text
We build a deck, shuffle it, create two empty hands, and deal — alternating cards, one to Player 1, one to Player 2, until all 52 are distributed. Each player gets 26.

**[VISUAL: Animation — a deck splitting into two piles, cards alternating left and right.]**
```
