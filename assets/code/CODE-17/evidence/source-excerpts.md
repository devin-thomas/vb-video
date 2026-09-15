## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:220–232

```text
        Do
            ' A player who has run out of cards mid-war loses immediately.
            If Player1.Count = 0 Then
                Console.WriteLine("Player 1 has no cards left for the war - Player 2 takes the pot.")
                GiveCardsToWinner(Pot, PotCount, Player2)
                Exit Sub
            End If

            If Player2.Count = 0 Then
                Console.WriteLine("Player 2 has no cards left for the war - Player 1 takes the pot.")
                GiveCardsToWinner(Pot, PotCount, Player1)
                Exit Sub
            End If
```

## SCRIPT.md:460–462

```text
Then there's an inner `Do...Loop` — not a `Do While`, just `Do...Loop`, which is an infinite loop that we exit with `Exit Sub` when someone wins. Each iteration:

One — check if either player is out of cards. If you can't play, you lose, and the other player takes the pot.
```
