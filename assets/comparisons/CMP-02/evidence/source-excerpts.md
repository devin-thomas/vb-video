## ASSET_PLAN.md:38–38

```text
| 4 | Side-by-side C# vs VB comparisons (4+) | HTML two-column layout |
```

## SCRIPT.md:265–270

```text
First: `Sub`. Not `void`, not `function` — `Sub`. Short for "subroutine." In Visual Basic, there's a hard distinction between a `Sub`, which does something and doesn't return a value, and a `Function`, which does something and gives you back a result. In C-family languages, a function that returns nothing is just a function with a `void` return type. In VB, it's a completely different keyword.

**[VISUAL: Side-by-side comparison:]**
```
C#:    void BuildDeck(Card[] deck) { ... }
VB:    Sub BuildDeck(ByRef Deck() As Card) ... End Sub
```

## review/cut-notes-2026-09-16.md:20–21 (revision 2 brief, not a script source)

```text
| 14 | "Sub = a function that returns nothing; Function = a function that returns a value" needs a visual or animation, and a more obvious pairing: `void HelloWorld` and `int Add` on the C-style side against `Sub HelloWorld` and `Function Add` on the VB side. | Section 7, the Sub/Function beat (CMP-02 area) | New or reworked comparison asset with the two pairs side by side, ideally animated (the return value appearing on the Function/`int` row and nothing on the Sub/`void` row). Header lists the languages per note 13. |
| 15 | The for-loop explanation says "i" in the narration but the on-screen variable is `rank`. Make the screen say `i`. | Section 7, the `For` loop beat (CMP-03 / CODE card around 13:30–14:30) | Rename the loop variable on the card(s) to `i`. The narration is final, so the asset follows the voice. Check the same card is not also quoted as a literal excerpt of Program.vb (the validator treats code cards as excerpts); if it is, the card becomes a teaching example and is labelled as such. |
```
