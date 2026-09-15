## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:207–208

```text
        Dim Pot(HAND_CAPACITY * 2 - 1) As Card
        Dim PotCount As Integer
```

## SCRIPT.md:449–458

```text
Inside, there's a pot — an array that collects all the cards at stake this round:

```vb
Dim Pot(HAND_CAPACITY * 2 - 1) As Card
Dim PotCount As Integer
```

**[VISUAL: A diagram of the "pot" — a growing pile between the two players.]**

The pot can theoretically hold every card in the game. In a normal round, it holds two cards. In a war, it holds ten. In a double war, eighteen. In theory, wars can chain indefinitely, though in practice it's extremely rare to go past three.
```
