## ASSET_PLAN.md:16–16

```text
| 1 | Event-driven programming diagram | SVG — boxes and arrows |
```

## SCRIPT.md:130–138

```text
**[VISUAL: Side-by-side — the VB4 IDE with labeled callouts: Form Designer, Toolbox, Properties Window, Code Window, Project Explorer.]**

This IDE had a few key pieces. On the left, you had a toolbox — a vertical strip of icons for things like buttons, text boxes, labels, picture boxes, timers, scroll bars. In the center was your form — a blank gray window that you designed visually. On the right was the properties panel, where you could set things like the caption on a button or the font size of a label. And behind all of it was the code window, where you wrote your actual BASIC.

This was called "RAD" — Rapid Application Development. The whole point was speed. You weren't writing code to create a window. The IDE did that for you. You were writing code to respond to events — a button click, a timer tick, a key press.

**[VISUAL: Animated diagram — "Event-Driven Programming" — arrows from user actions (click, type, resize) pointing to Sub procedures in code.]**

Now, for today's project, we're not going to use any of that visual stuff. War is a console program — two CPUs playing cards against each other in a terminal. No forms, no buttons. But I want you to understand that the form designer was the reason people bought VB. The language itself was just one part of the package. The drag-and-drop GUI builder was the killer feature.
```

## SCRIPT.md:98–108

```text
Here's what made Visual Basic revolutionary: in C, if you wanted a button that said "Click Me" and popped up a message, you were writing dozens of lines of boilerplate. In Visual Basic, you drew the button on the form with your mouse, double-clicked it, and typed:

**[VISUAL: Code appearing on screen:]**

```vb
Sub Command1_Click()
    MsgBox "You clicked me!"
End Sub
```

That's it. Three lines. You hit F5, the program ran, the button worked. The gap between having an idea and seeing it work on screen was shorter than it had ever been in the history of programming.
```
