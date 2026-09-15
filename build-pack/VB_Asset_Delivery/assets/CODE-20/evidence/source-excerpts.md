## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:260–268

```text
                WarNumber = WarNumber + 1
                WarCount = WarCount + 1
                Console.WriteLine("        ** WAR! ** (war number " & WarNumber & " this round)")

                BurnCount = Math.Min(3, Math.Min(Player1.Count, Player2.Count))
                For i = 1 To BurnCount
                    Pot(PotCount) = DrawTopCard(Player1) : PotCount = PotCount + 1
                    Pot(PotCount) = DrawTopCard(Player2) : PotCount = PotCount + 1
                Next i
```

## SCRIPT.md:472–489

```text
```vb
WarNumber = WarNumber + 1
WarCount = WarCount + 1

BurnCount = Math.Min(3, Math.Min(Player1.Count, Player2.Count))
For i = 1 To BurnCount
    Pot(PotCount) = DrawTopCard(Player1) : PotCount = PotCount + 1
    Pot(PotCount) = DrawTopCard(Player2) : PotCount = PotCount + 1
Next i
```

**[VISUAL: Step-by-step animation of a War sequence:]**
**Step 1: Two equal cards face up.**
**Step 2: Three face-down cards from each player.**
**Step 3: One face-up card from each player.**
**Step 4: Higher card takes everything.**

Each player burns up to three cards face-down — or fewer, if they don't have three left. Then the loop goes back to the top, draws again, and compares again. If it's another tie, another war. The pot keeps growing.
```
