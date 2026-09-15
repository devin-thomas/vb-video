' War.vb
' A simulation of the card game War between two computer players.
' Written in the style of classic Visual Basic (VB4/VB5, circa 1995-96):
' one Module, one Sub Main, plain procedural flow, no LINQ, no lambdas,
' User-Defined Types (Structures) and parallel logic instead of classes.

Option Explicit On
Option Strict On

Module Program

    ' A single playing card. Rank runs 2 through 14 (11=Jack, 12=Queen,
    ' 13=King, 14=Ace). Suit is kept only for the printout - War does not
    ' care about suits.
    Structure Card
        Dim Rank As Integer
        Dim Suit As Char
    End Structure

    ' A player's hand of cards, stored as a simple array acting as a queue.
    ' Cards(0) is the top of the deck (next card to be played).
    ' Count is how many of the array slots are actually in use.
    Structure Hand
        Dim Cards() As Card
        Dim Count As Integer
    End Structure

    Const HAND_CAPACITY As Integer = 52
    Const MAX_ROUNDS As Integer = 20000

    Sub Main()
        Dim Deck(51) As Card
        Dim Player1 As Hand
        Dim Player2 As Hand
        Dim RoundNumber As Integer
        Dim WarCount As Integer
        Dim TheWinner As Integer

        Console.WriteLine("=====================================")
        Console.WriteLine("   W A R   -   CPU vs CPU Simulator")
        Console.WriteLine("=====================================")
        Console.WriteLine()

        BuildDeck(Deck)
        ShuffleDeck(Deck)

        Player1 = NewHand()
        Player2 = NewHand()
        DealCards(Deck, Player1, Player2)

        Console.WriteLine("Cards dealt: Player 1 has " & Player1.Count & _
            ", Player 2 has " & Player2.Count & ".")
        Console.WriteLine()

        RoundNumber = 0
        WarCount = 0
        TheWinner = 0

        Do While Player1.Count > 0 And Player2.Count > 0
            RoundNumber = RoundNumber + 1

            If RoundNumber > MAX_ROUNDS Then
                Console.WriteLine()
                Console.WriteLine("No winner after " & MAX_ROUNDS & _
                    " rounds - calling it a draw (deck cycle detected).")
                TheWinner = 0
                Exit Do
            End If

            PlayRound(RoundNumber, Player1, Player2, WarCount)
        Loop

        Console.WriteLine()
        Console.WriteLine("=====================================")

        If Player1.Count = 0 And Player2.Count > 0 Then
            TheWinner = 2
        ElseIf Player2.Count = 0 And Player1.Count > 0 Then
            TheWinner = 1
        End If

        Select Case TheWinner
            Case 1
                Console.WriteLine("PLAYER 1 WINS THE WAR!")
            Case 2
                Console.WriteLine("PLAYER 2 WINS THE WAR!")
            Case Else
                Console.WriteLine("THE WAR ENDS IN A DRAW.")
        End Select

        Console.WriteLine("Total rounds played : " & RoundNumber)
        Console.WriteLine("Total wars fought    : " & WarCount)
        Console.WriteLine("=====================================")
    End Sub

    ' Fills a 52-card deck: ranks 2 through 14, four suits each.
    Sub BuildDeck(ByRef Deck() As Card)
        Dim Suits() As Char = {"S"c, "H"c, "D"c, "C"c}
        Dim Rank As Integer
        Dim SuitIndex As Integer
        Dim Index As Integer

        Index = 0
        For Rank = 2 To 14
            For SuitIndex = 0 To 3
                Deck(Index).Rank = Rank
                Deck(Index).Suit = Suits(SuitIndex)
                Index = Index + 1
            Next SuitIndex
        Next Rank
    End Sub

    ' Classic Fisher-Yates shuffle, done in place.
    Sub ShuffleDeck(ByRef Deck() As Card)
        Dim Rnd As New Random()
        Dim i As Integer
        Dim j As Integer
        Dim Temp As Card

        For i = 51 To 1 Step -1
            j = Rnd.Next(0, i + 1)
            Temp = Deck(i)
            Deck(i) = Deck(j)
            Deck(j) = Temp
        Next i
    End Sub

    Function NewHand() As Hand
        Dim H As Hand
        ReDim H.Cards(HAND_CAPACITY - 1)
        H.Count = 0
        NewHand = H
    End Function

    ' Deals the 52-card deck alternately into the two hands, 26 apiece.
    Sub DealCards(ByRef Deck() As Card, ByRef Player1 As Hand, ByRef Player2 As Hand)
        Dim i As Integer

        For i = 0 To 51
            If i Mod 2 = 0 Then
                AddCardToBottom(Player1, Deck(i))
            Else
                AddCardToBottom(Player2, Deck(i))
            End If
        Next i
    End Sub

    ' Adds a card to the bottom (end) of a hand's queue.
    Sub AddCardToBottom(ByRef H As Hand, ByVal C As Card)
        H.Cards(H.Count) = C
        H.Count = H.Count + 1
    End Sub

    ' Removes and returns the top card of a hand's queue, shifting the
    ' remaining cards up by one slot.
    Function DrawTopCard(ByRef H As Hand) As Card
        Dim Top As Card
        Dim i As Integer

        Top = H.Cards(0)
        For i = 1 To H.Count - 1
            H.Cards(i - 1) = H.Cards(i)
        Next i
        H.Count = H.Count - 1

        DrawTopCard = Top
    End Function

    Function RankName(ByVal Rank As Integer) As String
        Select Case Rank
            Case 11
                RankName = "Jack"
            Case 12
                RankName = "Queen"
            Case 13
                RankName = "King"
            Case 14
                RankName = "Ace"
            Case Else
                RankName = CStr(Rank)
        End Select
    End Function

    Function CardText(ByVal C As Card) As String
        Dim SuitName As String

        Select Case C.Suit
            Case "S"c
                SuitName = "Spades"
            Case "H"c
                SuitName = "Hearts"
            Case "D"c
                SuitName = "Diamonds"
            Case Else
                SuitName = "Clubs"
        End Select

        CardText = RankName(C.Rank) & " of " & SuitName
    End Function

    ' Plays a single round of War, including any chained wars that result
    ' from tied cards. All cards won during the round are appended to the
    ' bottom of the winner's hand, in the order they were played.
    Sub PlayRound(ByVal RoundNumber As Integer, ByRef Player1 As Hand, _
                  ByRef Player2 As Hand, ByRef WarCount As Integer)

        Dim Pot(HAND_CAPACITY * 2 - 1) As Card
        Dim PotCount As Integer
        Dim Card1 As Card
        Dim Card2 As Card
        Dim WarNumber As Integer
        Dim BurnCount As Integer
        Dim i As Integer

        PotCount = 0
        WarNumber = 0

        Console.Write("Round " & RoundNumber & ": ")

        Do
            ' A player who has run out of cards mid-war loses immediately.
            If Player1.Count = 0 Then
                Console.WriteLine("Player 1 has no cards left for the war - Player 2 takes the pot.")
                GiveCardsToWinner(Pot, PotCount, Player2)
                Exit Sub
            End If

            If Player2.Count = 0 Then
                Console.WriteLine("Player 2 has no cards left for the war - Player 1 takes the pot.")
                GiveCardsToWinner(Pot, PotCount, Player1)
                Exit Sub
            End If

            Card1 = DrawTopCard(Player1)
            Card2 = DrawTopCard(Player2)
            Pot(PotCount) = Card1 : PotCount = PotCount + 1
            Pot(PotCount) = Card2 : PotCount = PotCount + 1

            If WarNumber = 0 Then
                Console.WriteLine("Player 1 plays " & CardText(Card1) & _
                    ", Player 2 plays " & CardText(Card2) & ".")
            Else
                Console.WriteLine("        War card - Player 1 plays " & CardText(Card1) & _
                    ", Player 2 plays " & CardText(Card2) & ".")
            End If

            If Card1.Rank > Card2.Rank Then
                Console.WriteLine("        Player 1 wins the round (" & PotCount & " cards).")
                GiveCardsToWinner(Pot, PotCount, Player1)
                Exit Sub

            ElseIf Card2.Rank > Card1.Rank Then
                Console.WriteLine("        Player 2 wins the round (" & PotCount & " cards).")
                GiveCardsToWinner(Pot, PotCount, Player2)
                Exit Sub

            Else
                ' Tie: it's WAR. Each side burns up to 3 face-down cards,
                ' then both flip a new card to compare.
                WarNumber = WarNumber + 1
                WarCount = WarCount + 1
                Console.WriteLine("        ** WAR! ** (war number " & WarNumber & " this round)")

                BurnCount = Math.Min(3, Math.Min(Player1.Count, Player2.Count))
                For i = 1 To BurnCount
                    Pot(PotCount) = DrawTopCard(Player1) : PotCount = PotCount + 1
                    Pot(PotCount) = DrawTopCard(Player2) : PotCount = PotCount + 1
                Next i
            End If
        Loop
    End Sub

    ' Appends every card currently in the pot to the bottom of the
    ' winner's hand, then empties the pot.
    Sub GiveCardsToWinner(ByRef Pot() As Card, ByRef PotCount As Integer, ByRef Winner As Hand)
        Dim i As Integer

        For i = 0 To PotCount - 1
            AddCardToBottom(Winner, Pot(i))
        Next i

        PotCount = 0
    End Sub

End Module
