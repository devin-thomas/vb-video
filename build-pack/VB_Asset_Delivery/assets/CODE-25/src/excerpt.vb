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
