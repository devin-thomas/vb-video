                WarNumber = WarNumber + 1
                WarCount = WarCount + 1
                Console.WriteLine("        ** WAR! ** (war number " & WarNumber & " this round)")

                BurnCount = Math.Min(3, Math.Min(Player1.Count, Player2.Count))
                For i = 1 To BurnCount
                    Pot(PotCount) = DrawTopCard(Player1) : PotCount = PotCount + 1
                    Pot(PotCount) = DrawTopCard(Player2) : PotCount = PotCount + 1
                Next i
