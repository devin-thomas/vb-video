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
