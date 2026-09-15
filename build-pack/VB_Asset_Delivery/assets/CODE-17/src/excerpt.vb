        Do
            ' A player who has run out of cards mid-war loses immediately.
            If Player1.Count = 0 Then
                Console.WriteLine("Player 1 has no cards left for the war - Player 2 takes the pot.")
                GiveCardsToWinner(Pot, PotCount, Player2)
                Exit Sub
            End If

            If Player2.Count = 0 Then
                Console.WriteLine("Player 2 has no cards left for the war - Player 1 takes the pot.")
                GiveCardsToWinner(Pot, PotCount, Player1)
                Exit Sub
            End If
