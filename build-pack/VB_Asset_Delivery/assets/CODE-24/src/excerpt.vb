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
