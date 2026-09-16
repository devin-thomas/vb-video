# CODE-27 source excerpts

The card is an authored teaching example; nothing here is a Program.vb excerpt.

## sources/SCRIPT.md:166–166 (narration, final)

```text
Two important settings in the project file: `Option Explicit On` and `Option Strict On`. In classic VB, variables didn't need to be declared. You could just start using a variable called `x` and VB would create it for you on the spot as a Variant — a type that could hold anything. This was convenient and also the source of approximately ten million bugs, because if you misspelled a variable name, VB would just silently create a new empty variable instead of telling you something was wrong. `Option Explicit` forces you to declare everything. We're being responsible.
```

## docs/tickets/CODE-27.md:36–43 (exact copy payload, authored)

```text
' Visual Basic 4 · Option Explicit off
Dim Nintendo As Integer
Nintendo = 1985
Nintendont = Nintendo + 1   ' typo: creates a NEW empty variable
Print Nintendo              ' still 1985

' with Option Explicit On:
' Nintendont = Nintendo + 1  → Variable not defined: Nintendont
```

## review/cut-notes-2026-09-16.md:12 (Devin's review note 6, origin)

```text
| 6 | At about 8:45–9:00 the narration says an undeclared variable is created as a Variant; show it. Then show a variable being set and a typo'd name being used: `Nintendo` as the correct name, `Nintendont` as the misspelling. | Section 4, around 8:45–9:00 | No asset carries this today; the beat holds the previous visual. New code asset(s): one card showing the undeclared name silently becoming a Variant, one showing `Nintendo` set and `Nintendont` used, with the consequence (silent new variable, and what `Option Explicit` does about it). Names exactly as Devin gave them. |
```
