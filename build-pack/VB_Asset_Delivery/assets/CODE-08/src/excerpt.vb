    Sub AddCardToBottom(ByRef H As Hand, ByVal C As Card)
        H.Cards(H.Count) = C
        H.Count = H.Count + 1
    End Sub
