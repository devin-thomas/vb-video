## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:7–8

```text
Option Explicit On
Option Strict On
```

## SCRIPT.md:162–166

```text
Now, the code I'm going to write uses modern VB.NET syntax, but I'm deliberately writing it in the old style. One module. One `Sub Main`. Structures instead of classes. Manual array management instead of generic collections. `Select Case` instead of pattern matching. `Do While...Loop` instead of LINQ. If you squint at this code, it should feel like something you'd see in a VB4 textbook from 1996.

**[VISUAL: The War.vbproj file, briefly, with `OptionExplicit` and `OptionStrict` highlighted.]**

Two important settings in the project file: `Option Explicit On` and `Option Strict On`. In classic VB, variables didn't need to be declared. You could just start using a variable called `x` and VB would create it for you on the spot as a Variant — a type that could hold anything. This was convenient and also the source of approximately ten million bugs, because if you misspelled a variable name, VB would just silently create a new empty variable instead of telling you something was wrong. `Option Explicit` forces you to declare everything. We're being responsible.
```
