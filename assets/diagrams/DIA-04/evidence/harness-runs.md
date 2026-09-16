# DIA-04 revision 2 — harness runs for the authored example

The Bump / bump example on the canvas is an authored teaching example, not supplied code.
Its claimed outcome (ByVal leaves x at 5, ByRef makes x 6; the same for `int n` versus
`int& n` in C++) was executed on the production machine on 2026-09-16. The programs below
are exactly what ran; they live in the session scratchpad, not in this package. No network
access was used: the VB restore ran against an empty local package feed and needed nothing
beyond the installed SDK.

## VB.NET (.NET SDK 10.0.303, `dotnet run`)

`Bump.vbproj`: `Microsoft.NET.Sdk`, `OutputType` Exe, `TargetFramework` net10.0, `OptionStrict` On, `OptionExplicit` On.

```vb
Option Explicit On
Option Strict On

Module Program
    ' Authored teaching example for DIA-04 revision 2 (not supplied code).
    Sub BumpByVal(ByVal n As Integer)
        n = n + 1
    End Sub

    Sub BumpByRef(ByRef n As Integer)
        n = n + 1
    End Sub

    Sub Main()
        Dim x As Integer
        x = 5
        BumpByVal(x)
        Console.WriteLine("ByVal: x = 5, Bump(x), x is now " & x)
        x = 5
        BumpByRef(x)
        Console.WriteLine("ByRef: x = 5, Bump(x), x is now " & x)
    End Sub
End Module
```

Commands: `dotnet restore --source <empty folder>` then `dotnet run --no-restore`. Output:

```text
ByVal: x = 5, Bump(x), x is now 5
ByRef: x = 5, Bump(x), x is now 6
```

The canvas names both Subs `Bump`; the harness uses two names so one program can run both
paths. The parameter lists and bodies are otherwise identical to the canvas.

## C++ (g++ 16.2.0, MSYS2 UCRT64)

```cpp
// Authored teaching example for DIA-04 revision 2 (not supplied code).
#include <cstdio>
void bump_val(int n) {
    n = n + 1;
}
void bump_ref(int& n) {
    n = n + 1;
}
int main() {
    int x = 5;
    bump_val(x);
    std::printf("int n : x = 5, bump(x), x is now %d\n", x);
    x = 5;
    bump_ref(x);
    std::printf("int& n: x = 5, bump(x), x is now %d\n", x);
    return 0;
}
```

Command: `g++ -std=c++17 -Wall -o bump.exe bump.cpp && ./bump.exe` (no warnings). Output:

```text
int n : x = 5, bump(x), x is now 5
int& n: x = 5, bump(x), x is now 6
```

## What this does and does not settle

- It settles the Integer example as drawn: VB.NET `ByVal` / `ByRef` and C++ `int` / `int&`
  behave as the canvas shows for a single Integer / int.
- It says nothing about arrays, structures containing arrays, or classic VB4 defaults; the
  canvas makes no claim about those (R04a).
- The VB run is modern VB.NET. The video's subject is 1995-era VB; the `ByVal` / `ByRef`
  keywords and their meaning for an Integer parameter are the same, but this harness is not
  evidence about the historical default when neither keyword is written.
