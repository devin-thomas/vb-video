## ASSET_PLAN.md:38–38

```text
| 4 | Side-by-side C# vs VB comparisons (4+) | HTML two-column layout |
```

## SCRIPT.md:403–416

```text
Then the loop:

```vb
Do While Player1.Count > 0 And Player2.Count > 0
    RoundNumber = RoundNumber + 1
    If RoundNumber > MAX_ROUNDS Then
        ' Safety valve — call it a draw
        Exit Do
    End If
    PlayRound(RoundNumber, Player1, Player2, WarCount)
Loop
```

`Do While...Loop`. In C, that's `while (...) { }`. It keeps going as long as both players have at least one card. When either player hits zero, the loop ends and we have a winner.
```
