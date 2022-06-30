import ctypes
from ctypes import Structure, c_long, byref


PUL = ctypes.POINTER(ctypes.c_ulong)
ctypes.windll.user32.SetProcessDPIAware()

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def click(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)
    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up
def queryMousePosition():
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(byref(pt))
    return pt
    # return { "x": pt.x, "y": pt.y}/