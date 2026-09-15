## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:247–255

```text
            If Card1.Rank > Card2.Rank Then
                Console.WriteLine("        Player 1 wins the round (" & PotCount & " cards).")
                GiveCardsToWinner(Pot, PotCount, Player1)
                Exit Sub

            ElseIf Card2.Rank > Card1.Rank Then
                Console.WriteLine("        Player 2 wins the round (" & PotCount & " cards).")
                GiveCardsToWinner(Pot, PotCount, Player2)
                Exit Sub
```

## SCRIPT.md:466–470

```text
Three — compare ranks.

If Player 1's rank is higher, Player 1 wins the pot. `Exit Sub`.
If Player 2's rank is higher, Player 2 wins the pot. `Exit Sub`.
If they're equal? War.
```
