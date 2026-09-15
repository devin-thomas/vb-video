## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:23–26

```text
    Structure Hand
        Dim Cards() As Card
        Dim Count As Integer
    End Structure
```

## SCRIPT.md:311–330

```text
**[VISUAL: The `Hand` structure and the `AddCardToBottom` / `DrawTopCard` functions.]**

**NARRATION:**

Here's where things get interesting from a data structures perspective. Each player has a hand of cards, and that hand needs to behave like a queue — first in, first out. When you win cards, they go to the bottom of your pile. When you play a card, it comes off the top.

In C#, you'd use `Queue<Card>` and call it a day. In C++, you'd use `std::queue`. In 1995 VB? You didn't have generic collections. You didn't even have a built-in queue. You had arrays, and you had `ReDim`, and that was about it.

So we fake it:

```vb
Structure Hand
    Dim Cards() As Card
    Dim Count As Integer
End Structure
```

**[VISUAL: A visual diagram of the Hand structure — an array of 52 slots, with only the first N filled. An arrow labeled "Count" points to the boundary.]**

The hand is an array of 52 slots — the maximum possible, since you could theoretically hold all the cards — and a counter that tracks how many slots are actually in use. Cards zero through Count-minus-one are live. Everything past Count is garbage.
```
