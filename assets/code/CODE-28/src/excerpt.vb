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
