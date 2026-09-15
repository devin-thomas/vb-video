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
