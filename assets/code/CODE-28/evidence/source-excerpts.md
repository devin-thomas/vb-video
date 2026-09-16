## SCRIPT.md:305–305

```text
Also notice: every single variable is declared at the top of the subroutine with `Dim`. In classic VB, you couldn't declare variables in the middle of the code. Everything went at the top. It's like writing C89 — all declarations before any statements. C# and modern C++ let you declare variables wherever you want. VB was stricter about this.
```

## Program.vb:114–126

```text
    Sub ShuffleDeck(ByRef Deck() As Card)
        Dim Rnd As New Random()
        Dim i As Integer
        Dim j As Integer
        Dim Temp As Card

        For i = 51 To 1 Step -1
            j = Rnd.Next(0, i + 1)
            Temp = Deck(i)
            Deck(i) = Deck(j)
            Deck(j) = Temp
        Next i
    End Sub
```

## War/Program.vb:114–126 (identical line for line to sources/Program.vb:114–126)

```text
    Sub ShuffleDeck(ByRef Deck() As Card)
        Dim Rnd As New Random()
        Dim i As Integer
        Dim j As Integer
        Dim Temp As Card

        For i = 51 To 1 Step -1
            j = Rnd.Next(0, i + 1)
            Temp = Deck(i)
            Deck(i) = Deck(j)
            Deck(j) = Temp
        Next i
    End Sub
```
