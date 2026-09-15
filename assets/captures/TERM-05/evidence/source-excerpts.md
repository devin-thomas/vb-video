# TERM-05 source excerpts
Unchanged line ranges from the hash-locked originals in `sources/`.

## ASSET_PLAN.md:73–73

~~~~text
| 2 | Terminal: `dotnet run` full game output | Run it, screenshot. Run multiple times for different outcomes |
~~~~

## SCRIPT.md:569–573

~~~~text
**[VISUAL: Run it a few more times, showing the different results:]**

Every run is different because the shuffle is random. Sometimes it's over in 150 rounds. Sometimes it takes 500. The number of wars varies too — sometimes just a handful, sometimes twenty or more. But it always terminates.

This is about 280 lines of Visual Basic. Not 280 lines of boilerplate and framework code — 280 lines that actually do something. That's the whole game. Build, shuffle, deal, play, win. Done.
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
