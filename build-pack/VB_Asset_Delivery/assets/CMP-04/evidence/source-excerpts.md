## ASSET_PLAN.md:38–38

```text
| 4 | Side-by-side C# vs VB comparisons (4+) | HTML two-column layout |
```

## SCRIPT.md:290–303

```text
    For i = 51 To 1 Step -1
        j = Rnd.Next(0, i + 1)
        Temp = Deck(i)
        Deck(i) = Deck(j)
        Deck(j) = Temp
    Next i
End Sub
```

This is a Fisher-Yates shuffle — the gold standard for producing an unbiased random permutation. You walk backwards through the array, and for each position, you swap it with a randomly chosen position at or before it. Every possible ordering of the deck is equally likely. This is the same algorithm you'd use in C++ or C# or Python or anything else. It's one of those algorithms that's just correct, and has been since 1938 when Fisher and Yates published it.

**[VISUAL: Animation of the shuffle — an array of numbered cards, each step highlighting the swap. The array goes from ordered to shuffled.]**

The VB-specific thing to notice here is `For i = 51 To 1 Step -1`. That `Step -1` is how you count backwards. C-family languages just use `i--` in the for-loop update. VB makes you spell it out: "step by negative one." Verbose, but unambiguous.
```
