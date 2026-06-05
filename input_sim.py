import ctypes
from ctypes import wintypes
import time

user32 = ctypes.windll.user32

# Win32 Constants
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040

KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008

# Win32 Structures
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_ulonglong if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_ulong)
    ]

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_ulonglong if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_ulong)
    ]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD)
    ]

class INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT)
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("value", INPUT_UNION)
    ]

# Simulation helpers
def send_mouse_down(button):
    inputs = (INPUT * 1)()
    inputs[0].type = INPUT_MOUSE
    if button == "left":
        inputs[0].value.mi.dwFlags = MOUSEEVENTF_LEFTDOWN
    elif button == "right":
        inputs[0].value.mi.dwFlags = MOUSEEVENTF_RIGHTDOWN
    elif button == "middle":
        inputs[0].value.mi.dwFlags = MOUSEEVENTF_MIDDLEDOWN
    user32.SendInput(1, ctypes.byref(inputs), ctypes.sizeof(INPUT))

def send_mouse_up(button):
    inputs = (INPUT * 1)()
    inputs[0].type = INPUT_MOUSE
    if button == "left":
        inputs[0].value.mi.dwFlags = MOUSEEVENTF_LEFTUP
    elif button == "right":
        inputs[0].value.mi.dwFlags = MOUSEEVENTF_RIGHTUP
    elif button == "middle":
        inputs[0].value.mi.dwFlags = MOUSEEVENTF_MIDDLEUP
    user32.SendInput(1, ctypes.byref(inputs), ctypes.sizeof(INPUT))

def send_key_down(vk_code):
    scancode = user32.MapVirtualKeyW(vk_code, 0)
    inputs = (INPUT * 1)()
    inputs[0].type = INPUT_KEYBOARD
    inputs[0].value.ki.wScan = scancode
    inputs[0].value.ki.dwFlags = KEYEVENTF_SCANCODE
    user32.SendInput(1, ctypes.byref(inputs), ctypes.sizeof(INPUT))

def send_key_up(vk_code):
    scancode = user32.MapVirtualKeyW(vk_code, 0)
    inputs = (INPUT * 1)()
    inputs[0].type = INPUT_KEYBOARD
    inputs[0].value.ki.wScan = scancode
    inputs[0].value.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP
    user32.SendInput(1, ctypes.byref(inputs), ctypes.sizeof(INPUT))

def perform_click(button, double=False, interval_sec=0.1):
    if double:
        send_mouse_down(button)
        time.sleep(0.002)
        send_mouse_up(button)
        time.sleep(0.010)
        send_mouse_down(button)
        time.sleep(0.002)
        send_mouse_up(button)
    else:
        send_mouse_down(button)
        # Dynamic hold time
        hold_time = min(interval_sec * 0.2, 0.002)
        time.sleep(hold_time)
        send_mouse_up(button)

def perform_key_press(vk_code, interval_sec=0.1):
    if vk_code > 0:
        send_key_down(vk_code)
        # Dynamic hold time
        hold_time = min(interval_sec * 0.2, 0.005)
        time.sleep(hold_time)
        send_key_up(vk_code)
