## ASSET_PLAN.md:38–38

```text
| 4 | Side-by-side C# vs VB comparisons (4+) | HTML two-column layout |
```

## SCRIPT.md:223–229

```text
Now, let's talk about something that might look weird if you're coming from C# or C++: the keyword `Dim`.

**[VISUAL: The word `Dim` highlighted, with a thought bubble: "Dimension?"]**

`Dim` is how you declare a variable in Visual Basic. It stands for "Dimension" — as in, dimension an array, allocate space for this thing. That name goes all the way back to the original 1964 BASIC at Dartmouth. In the earliest versions, `DIM` was specifically for declaring the dimensions of arrays. Over time, it got repurposed to declare any variable. Fifty years later, VB programmers are still typing `Dim` and most of them have no idea they're invoking an abbreviation from 1964.

Compare that to C#, where you'd write `int rank;` or `char suit;`. In VB, the type comes after the name: `Dim Rank As Integer`. It reads more like English: "Dimension a variable called Rank, as an Integer." That's very much a deliberate design choice — BASIC was always supposed to read like English.
```
