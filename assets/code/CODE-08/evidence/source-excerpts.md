## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:149–152

```text
    Sub AddCardToBottom(ByRef H As Hand, ByVal C As Card)
        H.Cards(H.Count) = C
        H.Count = H.Count + 1
    End Sub
```

## SCRIPT.md:332–338

```text
Adding a card to the bottom is simple — drop it at position Count and increment:

```vb
Sub AddCardToBottom(ByRef H As Hand, ByVal C As Card)
    H.Cards(H.Count) = C
    H.Count = H.Count + 1
End Sub
```
