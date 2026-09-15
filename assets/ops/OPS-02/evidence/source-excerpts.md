# OPS-02 source excerpts
Unchanged line ranges from the hash-locked originals in `sources/`.

## Program.vb:1–29

~~~~text
' War.vb
' A simulation of the card game War between two computer players.
' Written in the style of classic Visual Basic (VB4/VB5, circa 1995-96):
' one Module, one Sub Main, plain procedural flow, no LINQ, no lambdas,
' User-Defined Types (Structures) and parallel logic instead of classes.

Option Explicit On
Option Strict On

Module Program

    ' A single playing card. Rank runs 2 through 14 (11=Jack, 12=Queen,
    ' 13=King, 14=Ace). Suit is kept only for the printout - War does not
    ' care about suits.
    Structure Card
        Dim Rank As Integer
        Dim Suit As Char
    End Structure

    ' A player's hand of cards, stored as a simple array acting as a queue.
    ' Cards(0) is the top of the deck (next card to be played).
    ' Count is how many of the array slots are actually in use.
    Structure Hand
        Dim Cards() As Card
        Dim Count As Integer
    End Structure

    Const HAND_CAPACITY As Integer = 52
    Const MAX_ROUNDS As Integer = 20000
~~~~

## SCRIPT.md:144–166

~~~~text
**[VISUAL: Modern terminal — `dotnet new console -lang VB` being typed and executed.]**

**NARRATION:**

Here's a small confession: you cannot legally install Visual Basic 4.0 in 2024. Microsoft stopped selling it decades ago. There's no download. The license doesn't transfer. You could find it on abandonware sites, but I'm making a YouTube video, so let's stay on the right side of copyright law.

What you can do is use VB.NET — the modern descendant of Visual Basic, which ships with every copy of the .NET SDK. When you install .NET, you get a compiler called `vbc` — the Visual Basic compiler. It's the real thing. Microsoft still maintains it.

**[VISUAL: Terminal showing `dotnet --version` returning a version number, then the project creation command.]**

So we create a new console project:

```
dotnet new console -lang VB
```

And we get a `.vbproj` file and a `Program.vb` file. That's our canvas.

Now, the code I'm going to write uses modern VB.NET syntax, but I'm deliberately writing it in the old style. One module. One `Sub Main`. Structures instead of classes. Manual array management instead of generic collections. `Select Case` instead of pattern matching. `Do While...Loop` instead of LINQ. If you squint at this code, it should feel like something you'd see in a VB4 textbook from 1996.

**[VISUAL: The War.vbproj file, briefly, with `OptionExplicit` and `OptionStrict` highlighted.]**

Two important settings in the project file: `Option Explicit On` and `Option Strict On`. In classic VB, variables didn't need to be declared. You could just start using a variable called `x` and VB would create it for you on the spot as a Variant — a type that could hold anything. This was convenient and also the source of approximately ten million bugs, because if you misspelled a variable name, VB would just silently create a new empty variable instead of telling you something was wrong. `Option Explicit` forces you to declare everything. We're being responsible.
~~~~
