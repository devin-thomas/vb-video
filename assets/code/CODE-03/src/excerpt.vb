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
