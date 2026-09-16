## ASSET_PLAN.md:38–38

```text
| 4 | Side-by-side C# vs VB comparisons (4+) | HTML two-column layout |
```

## SCRIPT.md:277–279

```text
Third: look at the `For` loop syntax. `For Rank = 2 To 14`. Then at the end: `Next Rank`. That `Next Rank` is closing the loop and telling you what variable is being incremented. If you're used to C-style `for (int i = 0; i < 14; i++)`, this is going to look almost quaint. But there's something kind of nice about it — when you have nested loops, each `Next` names its variable, so you can see at a glance which loop is ending.

**[VISUAL: The nested loops with colored brackets showing which `Next` closes which `For`.]**
```

## Program.vb:104–110

```text
        For Rank = 2 To 14
            For SuitIndex = 0 To 3
                Deck(Index).Rank = Rank
                Deck(Index).Suit = Suits(SuitIndex)
                Index = Index + 1
            Next SuitIndex
        Next Rank
```

## Authored teaching example (not a Program.vb excerpt)

```text
C / C++ / C# / Java
for (int i = 2; i <= 14; i++) {
    ...
}

VB
For i = 2 To 14
    ...
Next i
```

The ticket’s revision 2 renames the counter to `i` on both sides so the screen matches the narration. The left snippet is a proposed equivalent-bounds example valid in C, C++, C# and Java; the right snippet is the same loop in VB. Neither was compiled or run.

## Real loop check

`src/excerpt.vb` equals `sources/Program.vb` lines 104–110 byte for byte (LF newlines); `War/Program.vb` (CRLF, sha256 42d0bcf3320d6b29342961b97a4247e5dff69249c06a2a838c9c6fcda0e14f02) has the same seven lines at the same numbers. On screen the end state shows lines 104 and 110 with the common eight-space indent removed and lines 105–109 elided as `...`. The ticket text cites lines 244–255 for this loop; those lines are the round-resolution `If Card1.Rank > Card2.Rank` block, not a `For` loop. The only `For Rank = 2 To 14 ... Next Rank` in Program.vb is at 104–110 (BuildDeck).
