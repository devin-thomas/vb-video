# TERM-02 source excerpts
Unchanged line ranges from the hash-locked originals in `sources/`.

## ASSET_PLAN.md:73–73

~~~~text
| 2 | Terminal: `dotnet run` full game output | Run it, screenshot. Run multiple times for different outcomes |
~~~~

## SCRIPT.md:519–541

~~~~text
**[VISUAL: Terminal. The program runs. Full output scrolling, but slowed down enough to read the first few rounds.]**

**NARRATION:**

Let's run it.

```
dotnet run
```

**[VISUAL: Output appearing on screen:]**

```
=====================================
   W A R   -   CPU vs CPU Simulator
=====================================

Cards dealt: Player 1 has 26, Player 2 has 26.

Round 1: Player 1 plays 10 of Hearts, Player 2 plays King of Hearts.
        Player 2 wins the round (2 cards).
Round 2: Player 1 plays Ace of Hearts, Player 2 plays 3 of Diamonds.
        Player 1 wins the round (2 cards).
~~~~

## SCRIPT.md:559–566

~~~~text
**[VISUAL: Let it run to completion. Show the final summary:]**

```
=====================================
PLAYER 1 WINS THE WAR!
Total rounds played : 418
Total wars fought    : 10
=====================================
~~~~

## SCRIPT.md:717–736

~~~~text
**[VISUAL: Return to the terminal. The War simulator runs one more time, fast. Cards fly. A winner is declared.]**

**NARRATION:**

So that's Visual Basic. A language born from the idea that programming should be accessible. A tool that put software development within reach of people who'd never taken a computer science class. A product that dominated the 1990s and then got swept aside by its own successor.

And in about 280 lines, we used it to build something that works: a complete card game, with real deck management, a proper shuffle algorithm, and a game loop that handles every edge case — including wars that chain three and four levels deep.

If you want to try it yourself, the code is straightforward. Install the .NET SDK — it's free — run `dotnet new console -lang VB`, and start typing. The language will feel strange if you're used to curly braces and semicolons. But give it a few minutes, and you might start to see what millions of people saw in it thirty years ago.

It's readable. It's obvious. And it works.

**[VISUAL: The final summary output one more time:]**

```
=====================================
PLAYER 1 WINS THE WAR!
Total rounds played : 347
Total wars fought    : 13
=====================================
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
