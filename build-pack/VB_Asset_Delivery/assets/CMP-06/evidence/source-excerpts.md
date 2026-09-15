## ASSET_PLAN.md:38–38

```text
| 4 | Side-by-side C# vs VB comparisons (4+) | HTML two-column layout |
```

## SCRIPT.md:422–428

```text
Notice the string concatenation operator: `&`. In C# and C++, you use `+` to glue strings together. In VB, you use `&`. The reason is that `+` in VB does different things depending on the types involved — it might add numbers or concatenate strings — and this ambiguity caused enough bugs that Microsoft recommended always using `&` for strings. It's one of those "we made it too easy and now we need a rule to prevent the easy thing from biting you" situations.

**[VISUAL: Quick comparison chart:]**
```
C#:     "Hello " + name
VB:     "Hello " & name
```
```
