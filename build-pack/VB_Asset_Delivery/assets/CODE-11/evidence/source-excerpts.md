## ASSET_PLAN.md:37–37

```text
| 3 | Code blocks with VB syntax highlighting | HTML with `<pre>` + CSS color classes |
```

## Program.vb:44–49

```text
        BuildDeck(Deck)
        ShuffleDeck(Deck)

        Player1 = NewHand()
        Player2 = NewHand()
        DealCards(Deck, Player1, Player2)
```

## SCRIPT.md:388–399

```text
The main game loop is where everything comes together. Let's walk through `Sub Main`:

```vb
BuildDeck(Deck)
ShuffleDeck(Deck)

Player1 = NewHand()
Player2 = NewHand()
DealCards(Deck, Player1, Player2)
```

We build a deck, shuffle it, create two empty hands, and deal — alternating cards, one to Player 1, one to Player 2, until all 52 are distributed. Each player gets 26.
```
