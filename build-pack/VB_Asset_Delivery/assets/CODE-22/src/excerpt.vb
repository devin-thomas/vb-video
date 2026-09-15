    Sub GiveCardsToWinner(ByRef Pot() As Card, ByRef PotCount As Integer, ByRef Winner As Hand)
        Dim i As Integer

        For i = 0 To PotCount - 1
            AddCardToBottom(Winner, Pot(i))
        Next i

        PotCount = 0
    End Sub
