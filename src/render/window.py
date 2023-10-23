import win32api
import win32con
import win32gui


class Window:
    def __init__(self, title: str) -> None:
        self.title = title

        hinstance = win32api.GetModuleHandle()

        self.wnd_class = win32gui.WNDCLASS()
        self.wnd_class.lpszClassName = "SimpleWin32"
        self.wnd_class.hInstance = hinstance
        self.wnd_class.lpfnWndProc = self.window_proc
        self.wnd_class_atom = win32gui.RegisterClass(self.wnd_class)

        self.hwnd = win32gui.CreateWindow(
            self.wnd_class_atom,
            title,
            win32con.WS_OVERLAPPEDWINDOW,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            0,
            0,
            hinstance,
            None,
        )

        hdc = win32gui.GetDC(self.hwnd)
        self.hmdc = win32gui.CreateCompatibleDC(hdc)
        mbitmap = win32gui.CreateCompatibleBitmap(hdc, 1920, 1080)
        win32gui.SelectObject(self.hmdc, mbitmap)

    def update(self) -> None:
        win32gui.PumpWaitingMessages()

    def draw(self) -> None:
        win32gui.InvalidateRect(self.hwnd, None, False)
        win32gui.UpdateWindow(self.hwnd)

    def show(self) -> None:
        win32gui.ShowWindow(self.hwnd, win32con.SW_NORMAL)

    def fill(self, color: tuple[int, int, int]) -> None:
        brush = win32gui.CreateSolidBrush(win32api.RGB(color[0], color[1], color[2]))
        win32gui.FillRect(self.hmdc, (0, 0, 1920, 1080), brush)

    def draw_line(self, sx: int, sy: int, ex: int, ey: int) -> None:
        win32gui.MoveToEx(self.hmdc, sx, sy)
        win32gui.LineTo(self.hmdc, ex, ey)

    def draw_triangle(self, triangle, color: tuple[int, int, int]) -> None:
        color = win32api.RGB(color[0], color[1], color[2])
        pen = win32gui.CreatePen(win32con.PS_SOLID, 1, color)
        win32gui.SelectObject(self.hmdc, pen)
        win32gui.MoveToEx(self.hmdc, int(triangle[0][0]), int(triangle[0][1]))
        win32gui.LineTo(self.hmdc, int(triangle[1][0]), int(triangle[1][1]))
        win32gui.LineTo(self.hmdc, int(triangle[2][0]), int(triangle[2][1]))
        win32gui.LineTo(self.hmdc, int(triangle[0][0]), int(triangle[0][1]))

    def fill_triangle(self, triangle, color: tuple[int, int, int]) -> None:
        color = win32api.RGB(color[0], color[1], color[2])
        brush = win32gui.CreateSolidBrush(color)
        pen = win32gui.CreatePen(win32con.PS_SOLID, 1, color)
        win32gui.SelectObject(self.hmdc, brush)
        win32gui.SelectObject(self.hmdc, pen)
        win32gui.Polygon(self.hmdc, [(int(v[0]), int(v[1])) for v in triangle])

    def window_proc(self, hwnd: int, message: int, w_param: int, l_param: int) -> int:
        if message == win32con.WM_PAINT:
            hdc, paint_struct = win32gui.BeginPaint(hwnd)
            left, top, right, bottom = win32gui.GetClientRect(hwnd)

            win32gui.StretchBlt(
                hdc, 0, 0, right, bottom, self.hmdc, 0, 0, 1920, 1080, win32con.SRCCOPY
            )

            win32gui.EndPaint(hwnd, paint_struct)
            return 0
        elif message == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0
        else:
            return win32gui.DefWindowProc(hwnd, message, w_param, l_param)
