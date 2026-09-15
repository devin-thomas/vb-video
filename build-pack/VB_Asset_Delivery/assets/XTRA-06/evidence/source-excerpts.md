# XTRA-06 source excerpts
Unchanged line ranges from the hash-locked originals in `sources/`.

## SCRIPT.md:164–166

~~~~text
**[VISUAL: The War.vbproj file, briefly, with `OptionExplicit` and `OptionStrict` highlighted.]**

Two important settings in the project file: `Option Explicit On` and `Option Strict On`. In classic VB, variables didn't need to be declared. You could just start using a variable called `x` and VB would create it for you on the spot as a Variant — a type that could hold anything. This was convenient and also the source of approximately ten million bugs, because if you misspelled a variable name, VB would just silently create a new empty variable instead of telling you something was wrong. `Option Explicit` forces you to declare everything. We're being responsible.
~~~~

## Program.vb:7–8

~~~~text
Option Explicit On
Option Strict On
~~~~
