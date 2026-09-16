# H06 — Narration script (recording copy)

Prepared 2026-09-15 from `War/SCRIPT.md` at its current revision. Only spoken text is here; visual cues and code blocks are removed. Code the narration refers to is on screen in the corresponding CODE card, so read the words, not the listings, unless a sentence quotes a token (those are kept inline).

**How to use:** record one file per section, named `H06-<section number>.wav`, into `assets/handoffs/H06/` (create it; it is not tracked yet). Keep a clean start and end on each file. Return the real durations; the chapter timestamps in the script metadata are estimates and will be replaced.

## Pronunciation and reading notes

- **Dim** — say the word: 'dim'
- **ByRef / ByVal** — 'by ref', 'by val'
- **MsgBox** — 'message box' or 'msg box' (either, be consistent)
- **vbc** — letters: 'v b c'
- **Kemeny and Kurtz** — KEM-uh-nee, KURTS
- **CompUSA** — 'Comp U S A'
- **Egghead, Babbage's** — as written; BAB-ij-iz
- **Metrowerks CodeWarrior** — MET-ro-works
- **ResEdit** — 'rez edit'
- **NeXT / NeXTSTEP** — 'next', 'next step'
- **Applesoft** — as written
- **VBRUN300.DLL** — 'v b run three hundred dot d l l'
- **Fisher–Yates** — FISH-er YATES
- **Sybase** — SY-base
- **PowerBuilder** — as written
- **QuickBASIC** — 'quick basic'
- **Jet engine** — as written
- **MFC** — letters
- **AWT** — letters
- **Rnd.Next(0, i + 1)** — 'random dot next of zero and i plus one' (or skip the code aloud; it is on screen)
- **Exit Sub / Do...Loop / Next Rank** — read the keywords as words: 'exit sub', 'do loop', 'next rank'

## Estimated running time

| Section | Title | Words | ~min at 150 wpm |
|---|---|---|---|
| 1 | COLD OPEN / HOOK | 199 | 1.3 |
| 2 | A VERY BRIEF HISTORY OF BASIC TO VISUAL BASIC | 548 | 3.7 |
| 3 | THE TOOLCHAIN — WHAT YOU ACTUALLY INSTALLED | 288 | 1.9 |
| 4 | HOW WE'RE DOING THIS TODAY | 277 | 1.8 |
| 5 | THE CARD GAME WAR — RULES IN 60 SECONDS | 240 | 1.6 |
| 6 | MODELING A CARD IN VB | 350 | 2.3 |
| 7 | BUILDING AND SHUFFLING THE DECK | 483 | 3.2 |
| 8 | THE PLAYER'S HAND — ARRAYS AS QUEUES | 378 | 2.5 |
| 9 | THE GAME LOOP | 292 | 1.9 |
| 10 | WAR! THE RECURSION WITHIN THE LOOP | 396 | 2.6 |
| 11 | RUNNING IT — FULL SIMULATION | 111 | 0.7 |
| 12 | WHEN THE CARDS RUN OUT | 392 | 2.6 |
| 13 | WHAT THIS CODE WOULD HAVE BECOME | 412 | 2.7 |
| 14 | VB vs. THE COMPETITION IN 1995 | 432 | 2.9 |
| 15 | WHAT IF YOU WERE ON A MAC? | 502 | 3.3 |
| 16 | WHY VB MATTERED (AND WHY IT DIED) | 534 | 3.6 |
| 17 | OUTRO | 215 | 1.4 |
| | **Total** | **6049** | **40** |

The script metadata estimates 45 minutes of chapters; narration alone at a relaxed pace is about the same, so allow for holds on code and captures.

## Section 1: COLD OPEN / HOOK

In 1995, there was a programming language that more people used than C, more people used than C++, more people used than Java — which had literally just been invented. It was the single most popular programming language on the planet, and it powered everything from corporate accounting software to shareware games your dad downloaded off a BBS.

That language was Visual Basic.

And today, almost nobody talks about it. If you're under 30 and you learned to program, you probably learned Python, or JavaScript, or maybe C++. You've probably never written a line of Visual Basic in your life. You might not even know what it is.

So I'm going to write something in it. Specifically, I'm going to build a complete simulation of the card game War — two computer players, a full deck of 52 cards, shuffling, dealing, comparing, and the whole "I declare war" mechanic — all in Visual Basic, written the way someone would have actually written it in 1995 or 1996.

And along the way, I'm going to explain what this language was, why it mattered, why millions of people loved it, and why Microsoft eventually put a bullet in it.

Let's go.

## Section 2: A VERY BRIEF HISTORY OF BASIC TO VISUAL BASIC

To understand Visual Basic, you need to understand BASIC. Capital B, capital A, capital everything — it's an acronym. Beginner's All-purpose Symbolic Instruction Code. It was invented in 1964 at Dartmouth College by John Kemeny and Thomas Kurtz, and its entire reason for existing was that programming was too hard.

In 1964, if you wanted to write a program, you were probably writing FORTRAN or COBOL or assembly language. You were probably punching cards. The learning curve was brutal. Kemeny and Kurtz wanted something that a college freshman with no technical background could sit down and start using. So they made BASIC.

And it worked. It worked incredibly well. Through the 1970s and 1980s, BASIC became the language that shipped with almost every home computer. Your Commodore 64 had BASIC. Your Apple II had Applesoft BASIC. Your TRS-80 had BASIC. When you turned on a home computer in 1982, you were usually staring at a BASIC prompt.

This is important because it means that an entire generation of programmers — the people who would go on to build the software industry — learned to code by writing things like:

BASIC was how you learned. It was the Python of its era, except it came pre-installed on your hardware.

Now, fast-forward to 1991. Microsoft has Windows 3.0, and Windows programming is a nightmare. If you want to write a Windows application in C, you need to understand message loops, window procedures, callback functions, resource files, the entire Win16 API. A "Hello World" window in C is 73 lines of code. It's not beginner-friendly. It's barely expert-friendly.

A guy named Alan Cooper had built a prototype of a drag-and-drop interface builder. He called it "Tripod." You could take a blank window and just... drop a button onto it. Drop a text box. Drop a label. And it would wire up the event handling for you. Microsoft saw this, bought it, married it to a BASIC dialect, and in May of 1991, Visual Basic 1.0 was born.

And it changed everything.

Here's what made Visual Basic revolutionary: in C, if you wanted a button that said "Click Me" and popped up a message, you were writing dozens of lines of boilerplate. In Visual Basic, you drew the button on the form with your mouse, double-clicked it, and typed:

That's it. Three lines. You hit F5, the program ran, the button worked. The gap between having an idea and seeing it work on screen was shorter than it had ever been in the history of programming.

VB 1.0 came out in 1991 for Windows 3.0. VB 2.0 in 1992. VB 3.0 in 1993 added database support through something called the Jet engine — yes, the same engine inside Microsoft Access. VB 4.0 in 1995 was the first version that could compile to 32-bit code for Windows 95. And that's right around the era we're talking about today — 1995, 1996. VB4 was the current version. Windows 95 was brand new and everyone was excited about the Start menu.

VB 5.0 would come in 1997 and VB 6.0 in 1998 — that last one became the version people remember most fondly. But the spirit of the language, the way you actually thought about problems and wrote code? That was all established by VB4.

## Section 3: THE TOOLCHAIN — WHAT YOU ACTUALLY INSTALLED

So what did it actually look like to set up a Visual Basic development environment in 1995?

You went to a store. A physical store — CompUSA, Egghead Software, maybe a Babbage's in the mall. You bought a box. Inside the box was either a set of 3.5-inch floppy disks or, if you were lucky and had a CD-ROM drive, a single disc. You ran the installer, it unpacked onto your hard drive, and you had an integrated development environment — an IDE — that looked like a Windows application.

This IDE had a few key pieces. On the left, you had a toolbox — a vertical strip of icons for things like buttons, text boxes, labels, picture boxes, timers, scroll bars. In the center was your form — a blank gray window that you designed visually. On the right was the properties panel, where you could set things like the caption on a button or the font size of a label. And then there was the code window, where you wrote your actual BASIC.

This was called "RAD" — Rapid Application Development. The whole point was speed. You weren't writing code to create a window. The IDE did that for you. You were writing code to respond to events — a button click, a timer tick, a key press.

Now, for today's project, we're not going to use any of that visual stuff. War is a console program — two CPUs playing cards against each other in a terminal. No forms, no buttons. But I want you to understand that the form designer was the reason people bought VB. The language itself was just one part of the package. The drag-and-drop GUI builder was the killer feature.

## Section 4: HOW WE'RE DOING THIS TODAY

Here's a small confession: you cannot legally install Visual Basic 4.0 today. Microsoft stopped selling it decades ago. There's no download. The license doesn't transfer. You could find it on abandonware sites, but I'm making a YouTube video, so let's stay on the right side of copyright law.

What you can do is use VB.NET — the modern descendant of Visual Basic, which ships with every copy of the .NET SDK. When you install .NET, you get a compiler called `vbc` — the Visual Basic compiler. It's the real thing. Microsoft still maintains it.

So we create a new console project:

And we get a `.vbproj` file and a `Program.vb` file. That's our canvas.

Now, the code I'm going to write uses modern VB.NET syntax, but I'm deliberately writing it in the old style. One module. One `Sub Main`. Structures instead of classes. Manual array management instead of generic collections. `Select Case` instead of pattern matching. `Do While...Loop` instead of LINQ. If you squint at this code, it should feel like something you'd see in a VB4 textbook from 1996.

Two important settings in the project file: `Option Explicit On` and `Option Strict On`. In classic VB, variables didn't need to be declared. You could just start using a variable called `x` and VB would create it for you on the spot as a Variant — a type that could hold anything. This was convenient and also the source of approximately ten million bugs, because if you misspelled a variable name, VB would just silently create a new empty variable instead of telling you something was wrong. `Option Explicit` forces you to declare everything. We're being responsible.

## Section 5: THE CARD GAME WAR — RULES IN 60 SECONDS

Before we write any code, let's make sure we all know how War works, because you might not have played it since you were eight. Or maybe you've never played it at all. It's a children's card game — no strategy, no decisions, pure luck — which makes it perfect for a computer simulation, because there are no choices to model.

Here are the rules:

One. Take a standard 52-card deck and shuffle it. Deal it evenly — 26 cards to each player, face down. Neither player looks at their cards.

Two. Each round, both players flip their top card face-up at the same time. Whoever played the higher card takes both cards and puts them at the bottom of their pile. Aces are high — they beat everything.

Three. If both players flip the same rank — two sevens, two kings, whatever — it's War. Each player places three cards face-down, then flips a fourth card face-up. Whoever's face-up card is higher takes the entire pot — all ten cards. If it's another tie, you do it again. War can chain.

Four. You keep playing until one player has all 52 cards. That player wins. If a player runs out of cards during a war, they lose.

That's it. No bluffing, no bidding, no trump suits. Just flip, compare, collect. A game a five-year-old can play — and a game that maps beautifully onto about 280 lines of code.

## Section 6: MODELING A CARD IN VB

Let's start building. The first question any card game has to answer is: how do you represent a card?

In C++ or C#, you'd probably make a class, or at least a struct. In 1995 Visual Basic, you'd use something called a User-Defined Type — a `Type` block. In VB.NET, the equivalent is `Structure`. Same idea: a container that groups related pieces of data together.

A card has two things: a rank and a suit. The rank is an integer from 2 to 14. Two through ten are obvious. Eleven is Jack, twelve is Queen, thirteen is King, and fourteen is Ace. Why not one for Ace? Because in War, Aces are high — they beat everything — and if Ace is 14, then comparing two cards is just comparing two integers. Higher number wins. No special cases needed.

The suit is a single character — S, H, D, or C. Spades, Hearts, Diamonds, Clubs. War doesn't actually care about suits. They're there purely so the output looks nice. When the program tells you "Player 1 plays the Ace of Spades," that's the suit doing its job. But the game logic never looks at it.

Now, let's talk about something that might look weird if you're coming from C# or C++: the keyword `Dim`.

`Dim` is how you declare a variable in Visual Basic. It stands for "Dimension" — as in, dimension an array, allocate space for this thing. That name goes all the way back to the original 1964 BASIC at Dartmouth. In the earliest versions, `DIM` was specifically for declaring the dimensions of arrays. Over time, it got repurposed to declare any variable. Fifty years later, VB programmers are still typing `Dim` and most of them have no idea they're invoking an abbreviation from 1964.

Compare that to C#, where you'd write `int rank;` or `char suit;`. In VB, the type comes after the name: `Dim Rank As Integer`. It reads more like English: "Dimension a variable called Rank, as an Integer." That's very much a deliberate design choice — BASIC was always supposed to read like English.

## Section 7: BUILDING AND SHUFFLING THE DECK

Next, we need a deck. Fifty-two cards: thirteen ranks times four suits.

Two nested `For` loops. The outer loop walks through ranks 2 to 14. The inner loop walks through the four suits. We drop each card into the array at the current index and bump the index. After both loops finish, we have a perfectly ordered 52-card deck.

Let's pause and look at a few VB-specific things here.

First: `Sub`. Not `void`, not `function` — `Sub`. Short for "subroutine." In Visual Basic, there's a hard distinction between a `Sub`, which does something and doesn't return a value, and a `Function`, which does something and gives you back a result. In C-family languages, a function that returns nothing is just a function with a `void` return type. In VB, it's a completely different keyword.

Second: `ByRef`. See that in the parameter list? In VB, you had to explicitly say whether a parameter was passed by reference or by value. `ByRef` means the subroutine receives a pointer to the original — changes are visible to the caller. `ByVal` means it gets a copy. In classic VB4, the default was `ByRef` for everything, which was efficient but dangerous. It meant you could accidentally modify data the caller didn't expect you to touch.

Third: look at the `For` loop syntax. `For Rank = 2 To 14`. Then at the end: `Next Rank`. That `Next Rank` is closing the loop and telling you what variable is being incremented. If you're used to C-style `for (int i = 0; i < 14; i++)`, this is going to look almost quaint. But there's something kind of nice about it — when you have nested loops, each `Next` names its variable, so you can see at a glance which loop is ending.

Now, the shuffle:

This is a Fisher-Yates shuffle — the gold standard for producing an unbiased random permutation. You walk backwards through the array, and for each position, you swap it with a randomly chosen position at or before it. Every possible ordering of the deck is equally likely. This is the same algorithm you'd use in C++ or C# or Python or anything else. It's one of those algorithms that's just correct, and has been since 1938 when Fisher and Yates published it.

The VB-specific thing to notice here is `For i = 51 To 1 Step -1`. That `Step -1` is how you count backwards. C-family languages just use `i--` in the for-loop update. VB makes you spell it out: "step by negative one." Verbose, but unambiguous.

Also notice: every single variable is declared at the top of the subroutine with `Dim`. In classic VB, you couldn't declare variables in the middle of the code. Everything went at the top. It's like writing C89 — all declarations before any statements. C# and modern C++ let you declare variables wherever you want. VB was stricter about this.

## Section 8: THE PLAYER'S HAND — ARRAYS AS QUEUES

Here's where things get interesting from a data structures perspective. Each player has a hand of cards, and that hand needs to behave like a queue — first in, first out. When you win cards, they go to the bottom of your pile. When you play a card, it comes off the top.

In C#, you'd use `Queue<Card>` and call it a day. In C++, you'd use `std::queue`. In 1995 VB? You didn't have generic collections. You didn't even have a built-in queue. You had arrays, and you had `ReDim`, and that was about it.

So we fake it:

The hand is an array of 52 slots — the maximum possible, since you could theoretically hold all the cards — and a counter that tracks how many slots are actually in use. Cards zero through Count-minus-one are live. Everything past Count is garbage.

Adding a card to the bottom is simple — drop it at position Count and increment:

Drawing from the top is more expensive. You take the card at position zero, then shift everything else forward by one slot:

That shift is O(n) — every card in the hand moves one position. With a proper circular buffer or a linked list, you could do this in O(1). But we're writing 1995 VB. Nobody was thinking about algorithmic complexity when they had 26 cards in a hand. Computers were slower, but data sets were tiny. The whole game finishes in a few hundred to a couple of thousand rounds, and each round shifts at most 52 cards. A Pentium 75 could handle this without breaking a sweat.

Now, look at the `Function` return syntax:

This is one of the weirdest things in VB if you're coming from any other language. To return a value from a function, you assign to the function's own name. You don't write `return Top;` — you write `DrawTopCard = Top`, where `DrawTopCard` is the name of the function you're inside of. The function name acts as an implicit local variable that holds the return value.

This is pure old-school BASIC heritage. It's been this way since the 1960s. VB.NET also supports the `Return` keyword, but the assign-to-function-name style is the traditional way, and it's what you would have seen in the 90s.

## Section 9: THE GAME LOOP

The main game loop is where everything comes together. Let's walk through `Sub Main`:

We build a deck, shuffle it, create two empty hands, and deal — alternating cards, one to Player 1, one to Player 2, until all 52 are distributed. Each player gets 26.

Then the loop:

`Do While...Loop`. In C, that's `while (...) { }`. It keeps going as long as both players have at least one card. When either player hits zero, the loop ends and we have a winner.

The `MAX_ROUNDS` check is a safety valve. War is theoretically capable of cycling forever — the same cards going back and forth in a loop. In practice, with a random shuffle, games do end — my recorded runs took anywhere from 150 to 2,008 rounds. But just in case, we cap it at 20,000 rounds and call it a draw. In my testing, I've never actually hit the cap.

Notice the string concatenation operator: `&`. In C# and C++, you use `+` to glue strings together. In VB, you use `&`. The reason is that `+` in VB does different things depending on the types involved — it might add numbers or concatenate strings — and this ambiguity caused enough bugs that Microsoft recommended always using `&` for strings. It's one of those "we made it too easy and now we need a rule to prevent the easy thing from biting you" situations.

Also notice line continuation: the underscore `_` at the end of a line means "this statement continues on the next line." In C-family languages, a statement continues until you hit a semicolon. In VB, every line is its own statement by default — the underscore is the escape hatch when a line gets too long.

## Section 10: WAR! THE RECURSION WITHIN THE LOOP

The `PlayRound` subroutine is the heart of the game, and it's where the most interesting logic lives. It's also where the War mechanic — the thing the game is named after — actually happens.

Four parameters. The round number is passed `ByVal` because we just read it. The two hands and the war counter are `ByRef` because this subroutine modifies them.

Inside, there's a pot — an array that collects all the cards at stake this round:

The pot can theoretically hold every card in the game. In a normal round, it holds two cards. In a war, it holds ten. In a double war, eighteen. In theory, wars can chain indefinitely, though in practice it's extremely rare to go past three.

Then there's an inner `Do...Loop` — not a `Do While`, just `Do...Loop`, which is an infinite loop that we exit with `Exit Sub` when someone wins. Each iteration:

One — check if either player is out of cards. If you can't play, you lose, and the other player takes the pot.

Two — both players draw their top card. Both cards go into the pot.

Three — compare ranks.

If Player 1's rank is higher, Player 1 wins the pot. `Exit Sub`. If Player 2's rank is higher, Player 2 wins the pot. `Exit Sub`. If they're equal? War.

Each player burns up to three cards face-down — or fewer, if they don't have three left. Then the loop goes back to the top, draws again, and compares again. If it's another tie, another war. The pot keeps growing.

Notice this line:

That colon `:` is VB's statement separator — it puts two statements on one line. It's the equivalent of putting two lines on one line. Frowned upon by style guides, but convenient for cases like this where the two operations are conceptually atomic.

The `GiveCardsToWinner` subroutine at the end is simple — it walks the pot array and adds each card to the bottom of the winner's hand:

This is what determines the eventual outcome of the game. The order in which won cards get added to your hand affects what you'll play in future rounds, which affects who wins those rounds. War is deterministic after the shuffle — the outcome is sealed the moment the cards are dealt. There's no randomness during play. The only randomness is in the initial shuffle.

## Section 11: RUNNING IT — FULL SIMULATION

Let's run it.

A double war — Ace against Ace, then Queen against Queen, before an Ace finally beat a 2. Eighteen cards in the pot. That's a third of the entire deck changing hands in a single round.

Every run is different because the shuffle is random. Sometimes it's over in 150 rounds. Sometimes it takes more than 2,000. The number of wars varies too — ten in one game, sixty-nine in another. But it always terminates.

This is about 280 lines of Visual Basic. Not 280 lines of boilerplate and framework code — 280 lines that actually do something. That's the whole game. Build, shuffle, deal, play, win. Done.

## Section 12: WHEN THE CARDS RUN OUT

Rewind to that first run for a moment — 617 rounds, Player 1 wins. We saw the final scoreboard, but not the final play. Here's how the game actually ended:

Player 2 didn't just lose a round. Player 2 ran out of cards in the middle of a war.

Going into round 617, Player 2 had exactly 2 cards left — against Player 1's 50. Both played a 10: tie, war. Normally each player burns three cards face-down and flips a fourth. But Player 2 only had 1 card left after playing that 10. So what does the code do?

It doesn't demand three. It caps the burn at however many cards the shorter hand can spare. Player 2 had 1, so both players burned 1. After the burn, Player 2's hand was empty. The loop came back to the top, hit the empty-hand check, and that was it — Player 1 took the four-card pot and the game.

Panel 1: Player 2's hand — 2 cards. Player 1's hand — 50 cards. Panel 2: Both play a 10. 1 card left for Player 2, 49 for Player 1. Panel 3: Both burn 1. Zero cards left for Player 2. Panel 4: "Player 2 has no cards left for the war — Player 1 takes the pot."]**

And it happened again, in the opposite direction, purely by chance. The longest run — 2,008 rounds:

Same mechanic. Player 1 walked into round 2,008 holding 3 cards against 49. Both played an 8, leaving Player 1 with 2. Both burned 2. Player 1's hand was empty, and Player 2 took the six-card pot.

TERM-04: 2 cards → play 10 → burn 1 → empty → 4-card pot TERM-02: 3 cards → play 8 → burn 2 → empty → 6-card pot]**

This is a subtlety worth noticing. The rule isn't "you need three cards for a war or you forfeit." It's "burn what you have, and if there's nothing left to flip, you're done." A player down to two cards going into a war still gets a reduced burn — one card face-down, one card to compete with — and can still win it. They only lose if that flip ties again and the well is truly dry.

Two of our four recorded runs ended exactly this way. Nobody planned it. The shuffle decided.

## Section 13: WHAT THIS CODE WOULD HAVE BECOME

Okay, so we've built a console War simulator. In 1995, what would have happened next?

You would have put a GUI on it.

This is where Visual Basic's form designer would have come in. You'd open the IDE, draw a form the size of a card table, drop some `PictureBox` controls on it to represent the card positions, maybe load bitmap images of playing cards from a resource file, and wire up the game logic to a Timer control that advanced the game one round at a time. You'd add a "Deal" button, a "Watch" button, maybe a speed slider.

And this is how a lot of actual software got made in the mid-90s. People would start with the logic — get the algorithms working in a console or a simple form — and then layer the visual design on top. Visual Basic made that second step dramatically easier than anything else available.

The shareware scene of the 1990s was full of card games, board games, and puzzle games written in Visual Basic. Windows came bundled with Solitaire and Minesweeper (written in C), but the thousands of freeware and shareware alternatives that flooded BBS boards and early web sites? A huge number of those were VB apps.

You'd distribute your game by uploading it to a BBS or a shareware site. Users would download it, but they'd also need the VB runtime — a DLL file called something like `VBRUN300.DLL` that shipped separately from your program. If the user didn't already have it installed, your game wouldn't launch. So a lot of shareware authors would bundle the runtime with their download, which could turn a 200-kilobyte game into a megabyte-plus download. On a 14.4 modem, that's ten minutes or more of downloading. For a card game.

But people did it. And the games worked. And if you were a teenager in 1996 who wanted to make your own version of Solitaire or Hearts or Spades, Visual Basic was the fastest path from "I have an idea" to "my friends are playing my game."

This same code — the structures, the shuffle, the deck management — could be adapted for almost any card game. Poker hand evaluation is more complex, but the deck building and shuffling is identical. Blackjack would be simpler than War. Bridge or Hearts would need trick-taking logic, but the card representation is the same. This 280-line program is a seed that could grow into a lot of different things.

## Section 14: VB vs. THE COMPETITION IN 1995

Visual Basic didn't exist in a vacuum. In 1995, if you wanted to build a Windows application, you had choices. Let's talk about what they were and why VB won the market.

**Visual C++ 4.0** was Microsoft's professional-grade tool. MFC — the Microsoft Foundation Classes — gave you a C++ framework for building Windows apps. It was powerful, fast, and absolutely miserable to learn. MFC was notorious for its deep class hierarchies, its reliance on macros, and its unforgiving error messages. Professional developers used it. Game studios used it. Nobody starting from scratch would choose MFC if they had another option.

**Borland Delphi** was the dark horse. Released in 1995, Delphi was basically "Visual Basic but for Object Pascal." It had the same kind of drag-and-drop form designer, the same RAD philosophy, but it compiled to native code from day one and its language — Object Pascal — was genuinely well-designed. A lot of experienced programmers preferred Delphi to VB. It was faster at runtime, it had a real object system with inheritance, and Borland's component model was arguably better than VB's.

Delphi never caught VB in market share, though. VB had Microsoft behind it, and Microsoft controlled the operating system. VB was the default. If you were a self-taught programmer or a small business writing internal tools, you used VB because everyone else used VB. The ecosystem was bigger — more books, more tutorials, more third-party components, more people on CompuServe forums who could answer your questions.

**PowerBuilder** was huge in the corporate database world. If you were building a line-of-business application that talked to an Oracle or Sybase database, PowerBuilder was the tool. It had a thing called DataWindows that made building data-entry forms almost trivially easy. But it was expensive, corporate, and basically invisible outside of IT departments.

And then there was **Java**, which Sun Microsystems unveiled in 1995 with the slogan "Write Once, Run Anywhere" and shipped as version 1.0 in January 1996. Java was the future — everyone knew it. But in 1995, Java was brand new, brutally slow, had almost no libraries, and its GUI toolkit — AWT — was so ugly it could make you cry. Java would eventually eat the world, but not yet. Not in 1995.

So Visual Basic sat in a sweet spot: easier than C++, more established than Delphi, cheaper than PowerBuilder, and more practical than Java. It wasn't the best tool for any single job, but it was a good enough tool for almost every job. And "good enough for almost everything" is a very powerful position to be in.

## Section 15: WHAT IF YOU WERE ON A MAC?

What if you wanted to build this same card game in 1995, but you were on a Mac?

First: you weren't using Visual Basic. Microsoft never actually shipped Visual Basic for the Mac. They had something called QuickBASIC for the Apple Macintosh — released in 1988, last updated in 1992 — but that was a plain BASIC compiler, not the visual, drag-and-drop environment that made VB special on Windows. And eventually Mac Office got VBA, the macro language inside Excel and Word, but that was for automating spreadsheets, not building standalone applications.

On a Mac in 1995, you'd probably be using **Metrowerks CodeWarrior**. This was the dominant development environment for the Mac from the mid-90s onward. It used C and C++ and compiled for both the old Motorola 68k chips and the newer PowerPC architecture. The Mac Toolbox API — the equivalent of the Windows API — was C-based, and CodeWarrior was how most Mac developers interacted with it.

Now, here's a misconception I want to address: Objective-C. Some people assume that Mac programming in the 90s meant Objective-C. It didn't. Objective-C was a NeXTSTEP language — it was the language of Steve Jobs's other company, NeXT, and the NeXTSTEP operating system. In 1995, NeXT was a niche software company — it had stopped making its famous workstations two years earlier — selling its operating system and developer tools to universities and Wall Street. Regular Mac developers weren't using Objective-C at all.

Objective-C wouldn't become a Mac language until 2001, when Apple released Mac OS X. OS X was built on NeXTSTEP's foundation, and it brought Objective-C with it. So if someone asks "would it have been harder in Objective-C in 1995?" — the question doesn't quite apply. You wouldn't have been using Objective-C unless you were on a NeXT workstation, and if you were on a NeXT workstation, you were probably doing more interesting things than a card game.

For a console card game like ours — no GUI, just logic and text output — the difficulty would have been roughly comparable. C is a harder language than BASIC, but the actual logic of building a deck, shuffling, and comparing cards is the same in any language. You'd use structs, arrays, and printf instead of structures, arrays, and Console.WriteLine. The algorithm doesn't change.

Where VB had the massive advantage was in the next step — putting a GUI on it. In VB, that was an afternoon of dragging controls onto a form. On the Mac with CodeWarrior, you'd be writing Carbon or Toolbox API calls, managing window records, handling update events, and doing your own drawing into grafPorts. It was not an afternoon. It was a week, minimum, for someone who knew what they were doing.

That's the real story of Visual Basic's dominance: not that it could do things other tools couldn't, but that it made the common case — put a window on the screen with some buttons and make them do stuff — dramatically faster than anything else.

## Section 16: WHY VB MATTERED (AND WHY IT DIED)

Visual Basic mattered because it democratized programming.

That's not hyperbole. Before VB, writing a Windows application was a professional skill that required significant training. After VB, a motivated person with a $100 software purchase and a library book could build something real in a weekend. Accountants wrote tools to automate their spreadsheets. Teachers built quiz applications. Small business owners made inventory trackers. None of these people would have called themselves programmers. They were people with problems who discovered that Visual Basic was good enough to solve them.

The language was readable in a way that C-based languages aren't. `If PlayerScore > HighScore Then` reads like an English sentence. `For Each Item In Collection` tells you exactly what it's doing. You didn't need to know what a pointer was. You didn't need to manage memory. You didn't need to understand header files or linking or preprocessor directives. You just wrote what you meant, and it worked.

Microsoft estimated that by the late 1990s, there were more lines of Visual Basic code in production than any other language. VB6, released in 1998, became one of the most beloved development tools ever made. There are VB6 applications still running today in banks, hospitals, manufacturing plants, and government offices. Software that was written a quarter century ago, still doing its job, and nobody wants to touch it because rewriting it would be expensive and risky.

And then Microsoft killed it.

Well — they didn't kill it outright. What they did was announce, around 2000, that Visual Basic would become VB.NET — and then ship it in 2002 as a completely new language that shared the name but was fundamentally different under the hood. VB.NET ran on the .NET framework, used the Common Language Runtime, and had a different syntax, different semantics, different everything. Code from VB6 did not run in VB.NET. The migration tools were... let's say "aspirational."

The VB community was furious. They'd been promised that VB was a platform they could build careers on, and now Microsoft was telling them to start over. Many VB6 developers moved to VB.NET and eventually adapted. Many moved to C# instead, figuring that if they had to learn a new .NET language, they might as well learn the one Microsoft clearly favored. And some just... stayed on VB6. Some are still there.

In 2005, as Microsoft ended mainstream support for VB6, a group of developers and MVPs organized an actual petition to keep unmanaged Visual Basic alive.

VB.NET still exists today — it's the language we wrote this card game in. But it's a niche within a niche. Microsoft has officially stated that they will not add new language features to VB.NET; it will continue to compile and run, but it's in maintenance mode. C# gets all the new toys. VB.NET gets security patches.

The language that taught a generation to program is, for all practical purposes, finished.

But the ideas it pioneered — visual form designers, event-driven programming, RAD tools, components you can drop onto a surface and configure through properties — those ideas won completely. Every modern UI framework, from React to SwiftUI to Flutter, carries DNA that traces back to Alan Cooper's prototype and Microsoft's Visual Basic.

## Section 17: OUTRO

So that's Visual Basic. A language born from the idea that programming should be accessible. A tool that put software development within reach of people who'd never taken a computer science class. A product that dominated the 1990s and then got swept aside by its own successor.

And in about 280 lines, we used it to build something that works: a complete card game, with real deck management, a proper shuffle algorithm, and a game loop that handles every edge case — including wars that chain three and four levels deep.

If you want to try it yourself, the code is straightforward. Install the .NET SDK — it's free — run `dotnet new console -lang VB`, and start typing. The language will feel strange if you're used to curly braces and semicolons. But give it a few minutes, and you might start to see what millions of people saw in it thirty years ago.

It's readable. It's obvious. And it works.

Thanks for watching. If you enjoyed this, consider subscribing — I've got more of these retro language deep-dives planned. And if you were around in 1995 and you actually wrote VB4 code, leave a comment and tell me what I got wrong. I want to hear about it.

See you in the next one.
