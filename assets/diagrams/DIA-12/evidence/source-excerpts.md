## ASSET_PLAN.md:27–27

```text
| 12 | Mac vs Windows comparison table | SVG or HTML table |
```

## SCRIPT.md:659–671

```text
**[VISUAL: Side-by-side comparison chart:]**

| | Windows (VB4) | Mac (CodeWarrior) |
|---|---|---|
| Language | BASIC | C/C++ |
| GUI builder | Yes (drag & drop) | Sort of (ResEdit) |
| Learning curve | Low | Medium-high |
| Runtime required | Yes (VB runtime DLL) | No (native binary) |
| Console app like ours | Trivial | Also pretty easy, actually |

For a console card game like ours — no GUI, just logic and text output — the difficulty would have been roughly comparable. C is a harder language than BASIC, but the actual logic of building a deck, shuffling, and comparing cards is the same in any language. You'd use structs, arrays, and printf instead of structures, arrays, and Console.WriteLine. The algorithm doesn't change.

Where VB had the massive advantage was in the next step — putting a GUI on it. In VB, that was an afternoon of dragging controls onto a form. On the Mac with CodeWarrior, you'd be writing Carbon or Toolbox API calls, managing window records, handling update events, and doing your own drawing into grafPorts. It was not an afternoon. It was a week, minimum, for someone who knew what they were doing.
```
