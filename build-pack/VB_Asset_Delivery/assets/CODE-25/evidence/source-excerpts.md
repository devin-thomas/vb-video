## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:76–93

```text
        If Player1.Count = 0 And Player2.Count > 0 Then
            TheWinner = 2
        ElseIf Player2.Count = 0 And Player1.Count > 0 Then
            TheWinner = 1
        End If

        Select Case TheWinner
            Case 1
                Console.WriteLine("PLAYER 1 WINS THE WAR!")
            Case 2
                Console.WriteLine("PLAYER 2 WINS THE WAR!")
            Case Else
                Console.WriteLine("THE WAR ENDS IN A DRAW.")
        End Select

        Console.WriteLine("Total rounds played : " & RoundNumber)
        Console.WriteLine("Total wars fought    : " & WarCount)
        Console.WriteLine("=====================================")
```

## SCRIPT.md:559–573

```text
**[VISUAL: Let it run to completion. Show the final summary:]**

```
=====================================
PLAYER 1 WINS THE WAR!
Total rounds played : 418
Total wars fought    : 10
=====================================
```

**[VISUAL: Run it a few more times, showing the different results:]**

Every run is different because the shuffle is random. Sometimes it's over in 150 rounds. Sometimes it takes 500. The number of wars varies too — sometimes just a handful, sometimes twenty or more. But it always terminates.

This is about 280 lines of Visual Basic. Not 280 lines of boilerplate and framework code — 280 lines that actually do something. That's the whole game. Build, shuffle, deal, play, win. Done.
```

## SCRIPT.md:729–736

```text
**[VISUAL: The final summary output one more time:]**

```
=====================================
PLAYER 1 WINS THE WAR!
Total rounds played : 347
Total wars fought    : 13
=====================================
```
