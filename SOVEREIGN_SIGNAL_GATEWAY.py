"""
HSGF - SOVEREIGN_SIGNAL_GATEWAY.py
Version: V1.6 - Lazy-Loading Signal Gateway
Function: Handles low-level input signals with optimized startup time.
"""

class SignalGateway:
    def __init__(self):
        self._mouse = None
        self._keyboard = None
        self._pyautogui = None
        print("[SignalGateway] Sovereign Signal Gateway V1.6 (Lazy) Ready.")

    def _ensure_pyautogui(self):
        if self._pyautogui is None:
            import pyautogui
            pyautogui.FAILSAFE = False
            self._pyautogui = pyautogui

    def _ensure_pynput(self):
        if self._keyboard is None:
            import pynput
            self._keyboard = pynput.keyboard.Controller()
            self._mouse = pynput.mouse.Controller()

    def mouse_move(self, x: int, y: int):
        self._ensure_pyautogui()
        self._pyautogui.moveTo(x, y)

    def mouse_click(self, button='left'):
        self._ensure_pyautogui()
        self._pyautogui.click(button=button)

    def key_press(self, key: str):
        self._ensure_pyautogui()
        self._pyautogui.press(key)

# Singleton Export
signal_gateway = SignalGateway()
