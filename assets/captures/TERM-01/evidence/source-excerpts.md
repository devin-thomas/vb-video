# TERM-01 source excerpts
Unchanged line ranges from the hash-locked originals in `sources/`.

## ASSET_PLAN.md:72–72

~~~~text
| 1 | Terminal: `dotnet new console -lang VB` | Run the command, screenshot the terminal |
~~~~

## SCRIPT.md:144–160

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
~~~~

## Program.vb:7–8

~~~~text
Option Explicit On
Option Strict On
~~~~

## Program.vb:28–29

~~~~text
    Const HAND_CAPACITY As Integer = 52
    Const MAX_ROUNDS As Integer = 20000
~~~~
