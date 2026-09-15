## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:104–110

```text
        For Rank = 2 To 14
            For SuitIndex = 0 To 3
                Deck(Index).Rank = Rank
                Deck(Index).Suit = Suits(SuitIndex)
                Index = Index + 1
            Next SuitIndex
        Next Rank
```

## SCRIPT.md:277–279

```text
Third: look at the `For` loop syntax. `For Rank = 2 To 14`. Then at the end: `Next Rank`. That `Next Rank` is closing the loop and telling you what variable is being incremented. If you're used to C-style `for (int i = 0; i < 14; i++)`, this is going to look almost quaint. But there's something kind of nice about it — when you have nested loops, each `Next` names its variable, so you can see at a glance which loop is ending.

**[VISUAL: The nested loops with colored brackets showing which `Next` closes which `For`.]**
```
