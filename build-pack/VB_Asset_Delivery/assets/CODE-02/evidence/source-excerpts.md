## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:15–18

```text
    Structure Card
        Dim Rank As Integer
        Dim Suit As Char
    End Structure
```

## SCRIPT.md:198–229

```text
## SECTION 6: MODELING A CARD IN VB

**[VISUAL: The `Structure Card` code block, appearing on screen with syntax highlighting. Maybe a dark background with VB syntax colors — blue keywords, black identifiers.]**

**NARRATION:**

Let's start building. The first question any card game has to answer is: how do you represent a card?

In C++ or C#, you'd probably make a class, or at least a struct. In 1995 Visual Basic, you'd use something called a User-Defined Type — a `Type` block. In VB.NET, the equivalent is `Structure`. Same idea: a container that groups related pieces of data together.

```vb
Structure Card
    Dim Rank As Integer
    Dim Suit As Char
End Structure
```

**[VISUAL: The structure on screen with annotations pointing to each field.]**

A card has two things: a rank and a suit. The rank is an integer from 2 to 14. Two through ten are obvious. Eleven is Jack, twelve is Queen, thirteen is King, and fourteen is Ace. Why not one for Ace? Because in War, Aces are high — they beat everything — and if Ace is 14, then comparing two cards is just comparing two integers. Higher number wins. No special cases needed.

**[VISUAL: A visual chart: 2=2, 3=3... 10=10, J=11, Q=12, K=13, A=14]**

The suit is a single character — S, H, D, or C. Spades, Hearts, Diamonds, Clubs. War doesn't actually care about suits. They're there purely so the output looks nice. When the program tells you "Player 1 plays the Ace of Spades," that's the suit doing its job. But the game logic never looks at it.

Now, let's talk about something that might look weird if you're coming from C# or C++: the keyword `Dim`.

**[VISUAL: The word `Dim` highlighted, with a thought bubble: "Dimension?"]**

`Dim` is how you declare a variable in Visual Basic. It stands for "Dimension" — as in, dimension an array, allocate space for this thing. That name goes all the way back to the original 1964 BASIC at Dartmouth. In the earliest versions, `DIM` was specifically for declaring the dimensions of arrays. Over time, it got repurposed to declare any variable. Fifty years later, VB programmers are still typing `Dim` and most of them have no idea they're invoking an abbreviation from 1964.

Compare that to C#, where you'd write `int rank;` or `char suit;`. In VB, the type comes after the name: `Dim Rank As Integer`. It reads more like English: "Dimension a variable called Rank, as an Integer." That's very much a deliberate design choice — BASIC was always supposed to read like English.
```
