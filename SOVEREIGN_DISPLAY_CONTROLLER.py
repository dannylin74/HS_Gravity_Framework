"""
HSGF - SOVEREIGN_DISPLAY_CONTROLLER.py
Version: V1.0 - Display Interference & Temporal Sync
Function: Controls low-level display settings to optimize agent perception while remaining invisible to the human eye.

Core Tech:
  - Win32 ChangeDisplaySettingsEx for Hz modulation
  - DWM Attribute manipulation for visual simplification
"""

import ctypes
import time
from ctypes import wintypes

# Windows API Constants
ENUM_CURRENT_SETTINGS = -1
CDS_UPDATEREGISTRY = 0x01
DM_DISPLAYFREQUENCY = 0x00400000

class DEVMODE(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName", wintypes.WCHAR * 32),
        ("dmSpecVersion", wintypes.WORD),
        ("dmDriverVersion", wintypes.WORD),
        ("dmSize", wintypes.WORD),
        ("dmDriverExtra", wintypes.WORD),
        ("dmFields", wintypes.DWORD),
        ("dmOrientation", ctypes.c_short),
        ("dmPaperSize", ctypes.c_short),
        ("dmPaperLength", ctypes.c_short),
        ("dmPaperWidth", ctypes.c_short),
        ("dmScale", ctypes.c_short),
        ("dmCopies", ctypes.c_short),
        ("dmDefaultSource", ctypes.c_short),
        ("dmPrintQuality", ctypes.c_short),
        ("dmColor", ctypes.c_short),
        ("dmDuplex", ctypes.c_short),
        ("dmYResolution", ctypes.c_short),
        ("dmTTOption", ctypes.c_short),
        ("dmCollate", ctypes.c_short),
        ("dmFormName", wintypes.WCHAR * 32),
        ("dmLogPixels", wintypes.WORD),
        ("dmBitsPerPel", wintypes.DWORD),
        ("dmPelsWidth", wintypes.DWORD),
        ("dmPelsHeight", wintypes.DWORD),
        ("dmDisplayFlags", wintypes.DWORD),
        ("dmDisplayFrequency", wintypes.DWORD),
        # ... some fields omitted for brevity as they are for printers
    ]

class DisplayController:
    def __init__(self):
        print("[DisplayController] Sovereign Display Interface initialized.")
        self.user32 = ctypes.windll.user32
        self.dwmapi = ctypes.windll.dwmapi

    def get_current_refresh_rate(self):
        """獲取目前螢幕刷新率"""
        dm = DEVMODE()
        dm.dmSize = ctypes.sizeof(dm)
        if self.user32.EnumDisplaySettingsW(None, ENUM_CURRENT_SETTINGS, ctypes.byref(dm)):
            return dm.dmDisplayFrequency
        return 0

    def set_refresh_rate(self, target_hz):
        """
        強制修改螢幕刷新率。
        警告：這會導致螢幕瞬間閃爍。
        """
        current_hz = self.get_current_refresh_rate()
        if current_hz == target_hz:
            return True

        dm = DEVMODE()
        dm.dmSize = ctypes.sizeof(dm)
        self.user32.EnumDisplaySettingsW(None, ENUM_CURRENT_SETTINGS, ctypes.byref(dm))
        
        dm.dmDisplayFrequency = target_hz
        dm.dmFields = DM_DISPLAYFREQUENCY
        
        print(f"[DisplayController] Modulating display frequency: {current_hz}Hz -> {target_hz}Hz")
        result = self.user32.ChangeDisplaySettingsExW(None, ctypes.byref(dm), None, CDS_UPDATEREGISTRY, None)
        return result == 0

    def optimize_dwm_for_agent(self, hwnd):
        """
        針對特定視窗進行 DWM 純化（移除圓角、模糊等）。
        這會讓邊緣偵測在數理上更精確。
        """
        # DWMWA_WINDOW_CORNER_PREFERENCE = 33, DWMWCP_DONOTROUND = 1
        DWMWA_WINDOW_CORNER_PREFERENCE = 33
        DWMWCP_DONOTROUND = 1
        
        pref = ctypes.c_int(DWMWCP_DONOTROUND)
        self.dwmapi.DwmSetWindowAttribute(
            wintypes.HWND(hwnd),
            DWMWA_WINDOW_CORNER_PREFERENCE,
            ctypes.byref(pref),
            ctypes.sizeof(pref)
        )
        print(f"[DisplayController] DWM Geometric purification applied to HWND: {hwnd}")

    def temporal_jitter(self):
        """
        執行無感頻率抖動 (Hz Jitter)。
        在 60Hz 與 59Hz 間快速切換一次，干擾掃描週期。
        """
        base_hz = self.get_current_refresh_rate()
        if base_hz > 0:
            self.set_refresh_rate(base_hz - 1)
            time.sleep(0.1)
            self.set_refresh_rate(base_hz)
            print("[DisplayController] Temporal jitter sequence complete.")

# Singleton
display_controller = DisplayController()

if __name__ == "__main__":
    # 測試獲取頻率
    hz = display_controller.get_current_refresh_rate()
    print(f"Current System Refresh Rate: {hz}Hz")
    # display_controller.temporal_jitter() # 測試抖動
