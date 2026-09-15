/* hello.c -- a complete Windows 3.0 program that opens one window */
#include <windows.h>

long FAR PASCAL WndProc(HWND hWnd, unsigned iMessage, WORD wParam, LONG lParam)
{
    HDC         hDC;
    PAINTSTRUCT ps;

    switch (iMessage)
    {
        case WM_PAINT:
            hDC = BeginPaint(hWnd, &ps);
            TextOut(hDC, 20, 20, "Hello, World!", 13);
            EndPaint(hWnd, &ps);
            return 0L;

        case WM_DESTROY:
            PostQuitMessage(0);
            return 0L;
    }
    return DefWindowProc(hWnd, iMessage, wParam, lParam);
}

int PASCAL WinMain(HANDLE hInstance, HANDLE hPrevInstance,
                   LPSTR lpszCmdLine, int nCmdShow)
{
    static char szClassName[] = "HelloClass";
    WNDCLASS    wc;
    HWND        hWnd;
    MSG         msg;

    if (!hPrevInstance)
    {
        wc.style         = CS_HREDRAW | CS_VREDRAW;
        wc.lpfnWndProc   = WndProc;
        wc.cbClsExtra    = 0;
        wc.cbWndExtra    = 0;
        wc.hInstance     = hInstance;
        wc.hIcon         = LoadIcon(NULL, IDI_APPLICATION);
        wc.hCursor       = LoadCursor(NULL, IDC_ARROW);
        wc.hbrBackground = GetStockObject(WHITE_BRUSH);
        wc.lpszMenuName  = NULL;
        wc.lpszClassName = szClassName;

        if (!RegisterClass(&wc))
            return FALSE;
    }

    hWnd = CreateWindow(szClassName, "Hello, Windows",
                        WS_OVERLAPPEDWINDOW,
                        CW_USEDEFAULT, 0, CW_USEDEFAULT, 0,
                        NULL, NULL, hInstance, NULL);

    ShowWindow(hWnd, nCmdShow);
    UpdateWindow(hWnd);

    while (GetMessage(&msg, NULL, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    return msg.wParam;
}
