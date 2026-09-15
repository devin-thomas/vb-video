        Do While Player1.Count > 0 And Player2.Count > 0
            RoundNumber = RoundNumber + 1

            If RoundNumber > MAX_ROUNDS Then
                Console.WriteLine()
                Console.WriteLine("No winner after " & MAX_ROUNDS & _
                    " rounds - calling it a draw (deck cycle detected).")
                TheWinner = 0
                Exit Do
            End If

            PlayRound(RoundNumber, Player1, Player2, WarCount)
        Loop
