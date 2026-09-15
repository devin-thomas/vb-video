## ASSET_PLAN.md:38–38

```text
| 4 | Side-by-side C# vs VB comparisons (4+) | HTML two-column layout |
```

## SCRIPT.md:265–270

```text
First: `Sub`. Not `void`, not `function` — `Sub`. Short for "subroutine." In Visual Basic, there's a hard distinction between a `Sub`, which does something and doesn't return a value, and a `Function`, which does something and gives you back a result. In C-family languages, a function that returns nothing is just a function with a `void` return type. In VB, it's a completely different keyword.

**[VISUAL: Side-by-side comparison:]**
```
C#:    void BuildDeck(Card[] deck) { ... }
VB:    Sub BuildDeck(ByRef Deck() As Card) ... End Sub
```
