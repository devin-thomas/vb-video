    Function NewHand() As Hand
        Dim H As Hand
        ReDim H.Cards(HAND_CAPACITY - 1)
        H.Count = 0
        NewHand = H
    End Function
