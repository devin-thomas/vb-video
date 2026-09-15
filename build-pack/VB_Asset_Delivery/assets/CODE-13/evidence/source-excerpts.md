## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:59–71

```text
        Do While Player1.Count > 0 And Player2.Count > 0
            RoundNumber = RoundNumber + 1

            If RoundNumber > MAX_ROUNDS Then
                Console.WriteLine()
                Console.WriteLine("No winner after " & MAX_ROUNDS & _
                    " rounds - calling it a draw (deck cycle detected).")
                TheWinner = 0
                Exit Do
            End If

            PlayRound(RoundNumber, Player1, Player2, WarCount)
        Loop
```

## SCRIPT.md:403–420

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

**[VISUAL: Flowchart — "Both have cards?" → Yes → Play round → loop back. No → Determine winner.]**

The `MAX_ROUNDS` check is a safety valve. War is theoretically capable of cycling forever — the same cards going back and forth in a loop. In practice, with a random shuffle, games almost always end in a few hundred rounds. But just in case, we cap it at 20,000 rounds and call it a draw. In my testing, I've never actually hit the cap.
```
