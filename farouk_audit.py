import os
import subprocess
import psutil
import ctypes
import win32gui
import win32process

def farouk_audit():
    print("禮 [FAROUK SYSTEM AUDIT] - 啟動環境透視 禮")
    print("-" * 50)

    # 1. 檢查 UAC 與 權限
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    print(f"[Audit] 管理者權限: {'YES' if is_admin else 'NO (可能導致攔截)'}")

    # 2. 檢查潛在的「阻斷者」
    blockers = ["Battle.net", "EasyAntiCheat", "BattlEye", "Vanguard", "Faceit", "SecurityHealthService"]
    print("[Audit] 正在掃描潛在的攔截進程...")
    found_blockers = []
    for proc in psutil.process_iter(['name']):
        for b in blockers:
            if b.lower() in proc.info['name'].lower():
                found_blockers.append(proc.info['name'])
    
    if found_blockers:
        print(f"[-] 警告：發現敏感進程：{list(set(found_blockers))}")
        print("    這些程序可能會攔截 GDI 或 DirectX 採樣。")
    else:
        print("[+] 未發現明顯的第三方攔截器。")

    # 3. 測試 DWM 狀態
    dwm_status = os.popen('tasklist /FI "IMAGENAME eq dwm.exe"').read()
    if "dwm.exe" in dwm_status:
        print("[+] DWM 合成器正常運作中。")
    else:
        print("[-] DWM 異常，這會導致顯示信號中斷。")

    # 4. 終極測試：視窗枚舉
    print("[Audit] 測試視窗枚舉權限...")
    try:
        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    # 檢查是否有受保護的視窗
                    pass
            return True
        win32gui.EnumWindows(callback, None)
        print("[+] 視窗枚舉正常。")
    except Exception as e:
        print(f"[-] 視窗枚舉被攔截: {e}")

    print("-" * 50)
    print("禮 [AUDIT COMPLETE] - 請回傳結果給 Hiro 進行路徑修正。")

if __name__ == "__main__":
    farouk_audit()
