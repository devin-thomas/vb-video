' Visual Basic 4 · Option Explicit off
Dim Nintendo As Integer
Nintendo = 1985
Nintendont = Nintendo + 1   ' typo: creates a NEW empty variable
Print Nintendo              ' still 1985

' with Option Explicit On:
' Nintendont = Nintendo + 1  → Variable not defined: Nintendont
