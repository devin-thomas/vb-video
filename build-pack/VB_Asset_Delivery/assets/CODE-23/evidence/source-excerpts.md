## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:169–182

```text
    Function RankName(ByVal Rank As Integer) As String
        Select Case Rank
            Case 11
                RankName = "Jack"
            Case 12
                RankName = "Queen"
            Case 13
                RankName = "King"
            Case 14
                RankName = "Ace"
            Case Else
                RankName = CStr(Rank)
        End Select
    End Function
```

## SCRIPT.md:217–221

```text
A card has two things: a rank and a suit. The rank is an integer from 2 to 14. Two through ten are obvious. Eleven is Jack, twelve is Queen, thirteen is King, and fourteen is Ace. Why not one for Ace? Because in War, Aces are high — they beat everything — and if Ace is 14, then comparing two cards is just comparing two integers. Higher number wins. No special cases needed.

**[VISUAL: A visual chart: 2=2, 3=3... 10=10, J=11, Q=12, K=13, A=14]**

The suit is a single character — S, H, D, or C. Spades, Hearts, Diamonds, Clubs. War doesn't actually care about suits. They're there purely so the output looks nice. When the program tells you "Player 1 plays the Ace of Spades," that's the suit doing its job. But the game logic never looks at it.
```
