import ctypes
from ctypes import wintypes
import threading

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

class GlobalHotkeyManager:
    def __init__(self, callback):
        self.callback = callback
        self.vk = 0x75  # F6 by default
        self.thread = None
        self.thread_id = None
        self.lock = threading.Lock()

    def _run(self, vk):
        self.thread_id = kernel32.GetCurrentThreadId()
        HOTKEY_ID = 1
        MOD_NOREPEAT = 0x4000
        
        # Try to register
        if not user32.RegisterHotKey(None, HOTKEY_ID, MOD_NOREPEAT, vk):
            # Print to stdout, GUI will handle failure
            print(f"Failed to register hotkey for VK {vk}")
            return
            
        try:
            msg = wintypes.MSG()
            while True:
                res = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
                if res <= 0:  # WM_QUIT or error
                    break
                if msg.message == 0x0312:  # WM_HOTKEY
                    if msg.wParam == HOTKEY_ID:
                        # Invoke callback in a thread-safe way
                        self.callback()
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
        finally:
            user32.UnregisterHotKey(None, HOTKEY_ID)

    def set_hotkey(self, vk):
        with self.lock:
            # Stop existing thread
            if self.thread_id is not None:
                WM_QUIT = 0x0012
                user32.PostThreadMessageW(self.thread_id, WM_QUIT, 0, 0)
                self.thread_id = None
                
            self.vk = vk
            if vk > 0:
                self.thread = threading.Thread(target=self._run, args=(vk,), daemon=True)
                self.thread.start()

    def stop(self):
        self.set_hotkey(0)
