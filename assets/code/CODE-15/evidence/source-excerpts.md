## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:204–205

```text
    Sub PlayRound(ByVal RoundNumber As Integer, ByRef Player1 As Hand, _
                  ByRef Player2 As Hand, ByRef WarCount As Integer)
```

## SCRIPT.md:440–447

```text
The `PlayRound` subroutine is the heart of the game, and it's where the most interesting logic lives. It's also where the War mechanic — the thing the game is named after — actually happens.

```vb
Sub PlayRound(ByVal RoundNumber As Integer, ByRef Player1 As Hand, _
              ByRef Player2 As Hand, ByRef WarCount As Integer)
```

Four parameters. The round number is passed `ByVal` because we just read it. The two hands and the war counter are `ByRef` because this subroutine modifies them.
```
