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
