/* HELLO.C -- "Hello, Windows!" for Windows 3.x (Win16).
   A complete program.  Link with HELLO.DEF.              */

#include <windows.h>

long FAR PASCAL __export WndProc (HWND, UINT, UINT, LONG);

int PASCAL WinMain (HANDLE hInstance, HANDLE hPrevInstance,
                    LPSTR lpszCmdLine, int nCmdShow)
{
    static char szAppName[] = "Hello";
    HWND        hwnd;
    MSG         msg;
    WNDCLASS    wndclass;

    if (!hPrevInstance)             /* first instance registers the class */
    {
        wndclass.style         = CS_HREDRAW | CS_VREDRAW;
        wndclass.lpfnWndProc   = WndProc;
        wndclass.cbClsExtra    = 0;
        wndclass.cbWndExtra    = 0;
        wndclass.hInstance     = hInstance;
        wndclass.hIcon         = LoadIcon (NULL, IDI_APPLICATION);
        wndclass.hCursor       = LoadCursor (NULL, IDC_ARROW);
        wndclass.hbrBackground = GetStockObject (WHITE_BRUSH);
        wndclass.lpszMenuName  = NULL;
        wndclass.lpszClassName = szAppName;

        if (!RegisterClass (&wndclass))
            return FALSE;
    }

    hwnd = CreateWindow (szAppName,                    /* window class name */
                         "Hello, Windows!",            /* caption bar text  */
                         WS_OVERLAPPEDWINDOW,          /* window style      */
                         CW_USEDEFAULT, CW_USEDEFAULT, /* initial position  */
                         CW_USEDEFAULT, CW_USEDEFAULT, /* initial size      */
                         NULL,                         /* parent window     */
                         NULL,                         /* menu handle       */
                         hInstance,                    /* program instance  */
                         NULL);                        /* creation params   */

    ShowWindow (hwnd, nCmdShow);
    UpdateWindow (hwnd);

    while (GetMessage (&msg, NULL, 0, 0))    /* the message loop */
    {
        TranslateMessage (&msg);
        DispatchMessage (&msg);
    }
    return msg.wParam;
}

long FAR PASCAL __export WndProc (HWND hwnd, UINT message,
                                  UINT wParam, LONG lParam)
{
    HDC         hdc;
    PAINTSTRUCT ps;

    switch (message)
    {
    case WM_PAINT:
        hdc = BeginPaint (hwnd, &ps);
        TextOut (hdc, 10, 10, "Hello, Windows!", 15);
        EndPaint (hwnd, &ps);
        return 0;

    case WM_DESTROY:
        PostQuitMessage (0);
        return 0;
    }
    return DefWindowProc (hwnd, message, wParam, lParam);
}
