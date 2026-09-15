## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:184–199

```text
    Function CardText(ByVal C As Card) As String
        Dim SuitName As String

        Select Case C.Suit
            Case "S"c
                SuitName = "Spades"
            Case "H"c
                SuitName = "Hearts"
            Case "D"c
                SuitName = "Diamonds"
            Case Else
                SuitName = "Clubs"
        End Select

        CardText = RankName(C.Rank) & " of " & SuitName
    End Function
```

## SCRIPT.md:221–221

```text
The suit is a single character — S, H, D, or C. Spades, Hearts, Diamonds, Clubs. War doesn't actually care about suits. They're there purely so the output looks nice. When the program tells you "Player 1 plays the Ace of Spades," that's the suit doing its job. But the game logic never looks at it.
```

## SCRIPT.md:422–428

```text
Notice the string concatenation operator: `&`. In C# and C++, you use `+` to glue strings together. In VB, you use `&`. The reason is that `+` in VB does different things depending on the types involved — it might add numbers or concatenate strings — and this ambiguity caused enough bugs that Microsoft recommended always using `&` for strings. It's one of those "we made it too easy and now we need a rule to prevent the easy thing from biting you" situations.

**[VISUAL: Quick comparison chart:]**
```
C#:     "Hello " + name
VB:     "Hello " & name
```
```
