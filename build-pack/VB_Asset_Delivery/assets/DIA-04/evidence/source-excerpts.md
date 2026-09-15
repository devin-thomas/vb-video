## ASSET_PLAN.md:19–19

```text
| 4 | ByRef vs ByVal diagram | SVG — two-panel reference vs copy arrows |
```

## SCRIPT.md:273–275

```text
Second: `ByRef`. See that in the parameter list? In VB, you had to explicitly say whether a parameter was passed by reference or by value. `ByRef` means the subroutine receives a pointer to the original — changes are visible to the caller. `ByVal` means it gets a copy. In classic VB4, the default was `ByRef` for everything, which was efficient but dangerous. It meant you could accidentally modify data the caller didn't expect you to touch.

**[VISUAL: Diagram — ByRef: arrow pointing from sub back to caller's variable. ByVal: a copy being made, arrow pointing to a separate box.]**
```

## SCRIPT.md:443–447

```text
Sub PlayRound(ByVal RoundNumber As Integer, ByRef Player1 As Hand, _
              ByRef Player2 As Hand, ByRef WarCount As Integer)
```

Four parameters. The round number is passed `ByVal` because we just read it. The two hands and the war counter are `ByRef` because this subroutine modifies them.
```

## Program.vb:149–152

```text
    Sub AddCardToBottom(ByRef H As Hand, ByVal C As Card)
        H.Cards(H.Count) = C
        H.Count = H.Count + 1
    End Sub
```

## Program.vb:204–208

```text
    Sub PlayRound(ByVal RoundNumber As Integer, ByRef Player1 As Hand, _
                  ByRef Player2 As Hand, ByRef WarCount As Integer)

        Dim Pot(HAND_CAPACITY * 2 - 1) As Card
        Dim PotCount As Integer
```
