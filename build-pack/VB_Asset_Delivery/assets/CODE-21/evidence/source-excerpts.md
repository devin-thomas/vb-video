## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:266–266

```text
                    Pot(PotCount) = DrawTopCard(Player1) : PotCount = PotCount + 1
```

## SCRIPT.md:491–497

```text
Notice this line:

```vb
Pot(PotCount) = DrawTopCard(Player1) : PotCount = PotCount + 1
```

That colon `:` is VB's statement separator — it puts two statements on one line. It's the equivalent of putting two lines on one line. Frowned upon by style guides, but convenient for cases like this where the two operations are conceptually atomic.
```
