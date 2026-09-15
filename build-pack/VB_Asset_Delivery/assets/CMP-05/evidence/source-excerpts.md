## ASSET_PLAN.md:38–38

```text
| 4 | Side-by-side C# vs VB comparisons (4+) | HTML two-column layout |
```

## SCRIPT.md:362–377

```text
Now, look at the `Function` return syntax:

```vb
DrawTopCard = Top
```

**[VISUAL: This line highlighted with a "wait, what?" annotation.]**

This is one of the weirdest things in VB if you're coming from any other language. To return a value from a function, you assign to the function's own name. You don't write `return Top;` — you write `DrawTopCard = Top`, where `DrawTopCard` is the name of the function you're inside of. The function name acts as an implicit local variable that holds the return value.

This is pure old-school BASIC heritage. It's been this way since the 1960s. VB.NET also supports the `Return` keyword, but the assign-to-function-name style is the traditional way, and it's what you would have seen in the 90s.

**[VISUAL: Side-by-side:]**
```
C#:    return top;
VB:    DrawTopCard = Top
```
