# CMP-09 — source excerpts

Exact lines from the frozen `sources/` copies (hash-locked; see provenance.json). The `War/` working copies carry the same text: War/Program.vb differs from sources/Program.vb only by CRLF line endings, and War/SCRIPT.md line numbers are offset (its copy of the CMP-09 sentence is line 320 and of the CODE-29 sentence line 746).

<!-- source creative brief -->
## SCRIPT.md:317–317

```text
In C#, you'd use `Queue<Card>` and call it a day. In C++, you'd use `std::queue`. In 1995 VB? You didn't have generic collections. You didn't even have a built-in queue. You had arrays, and you had `ReDim`, and that was about it.
```

<!-- literal excerpt (Structure Hand) -->
## Program.vb:23–26

```text
    Structure Hand
        Dim Cards() As Card
        Dim Count As Integer
    End Structure
```

<!-- literal excerpt (ReDim in NewHand) -->
## Program.vb:130–130

```text
        ReDim H.Cards(HAND_CAPACITY - 1)
```

<!-- literal excerpt (DrawTopCard shift loop) -->
## Program.vb:160–164

```text
        Top = H.Cards(0)
        For i = 1 To H.Count - 1
            H.Cards(i - 1) = H.Cards(i)
        Next i
        H.Count = H.Count - 1
```

