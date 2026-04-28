"""
[戰術代號: SOVEREIGN_INPUT_GATEWAY.py]
[主權版本: V3.6 - Stealth Input Protocol]
[功能: 擬人化、反偵測的輸入對沖層。模擬人類行為模式，規避啟發式偵測。]
"""

import time
import random
import numpy as np
import pyautogui
from scipy import interpolate

class StealthInputGateway:
    def __init__(self):
        pyautogui.PAUSE = 0 # 移除預設延遲，由我們精確控制
        print("👤 [StealthInput] 潛行輸入協議已點火。動作擬人化已激活。")

    def move_mouse_stealth(self, target_x, target_y, duration=None):
        """
        [V3.7 物理引力場]: 模擬滑鼠在引力場中的運動
        """
        if duration is None:
            duration = random.uniform(0.4, 0.8)

        start_x, start_y = pyautogui.position()
        
        # 模擬引力場控制點 (Physics-based Control Points)
        # 這些點不再是隨機生成的，而是基於起始點到目標點的「引力梯度」
        dist = np.sqrt((target_x - start_x)**2 + (target_y - start_y)**2)
        cp_count = max(3, int(dist / 100))
        
        x_points = np.linspace(start_x, target_x, cp_count)
        y_points = np.linspace(start_y, target_y, cp_count)
        
        # 注入「肌肉顫抖」與「空間扭曲」 (Micro-jitter)
        for i in range(1, len(x_points) - 1):
            # 越靠近目標，引力越強，抖動越小 (物理衰減)
            decay = 1 - (i / len(x_points))
            x_points[i] += random.gauss(0, 10 * decay)
            y_points[i] += random.gauss(0, 10 * decay)
            
        # 使用 Scipy 生成物理平滑軌跡
        tck, u = interpolate.splprep([x_points, y_points], k=3 if len(x_points)>3 else 1, s=2)
        u_new = np.linspace(0, 1, int(duration * 60))
        out = interpolate.splev(u_new, tck)
        
        # 執行具備「慣性」與「加速度」的移動
        for px, py in zip(out[0], out[1]):
            pyautogui.moveTo(px, py)
            # 模擬肌肉延遲
            time.sleep(random.uniform(0.001, 0.005))
        
        print(f"🌌 [Gravity] 指標已跌入引力井: ({target_x}, {target_y})")

    def click_stealth(self, x=None, y=None, button='left'):
        """
        帶有微小隨機座標偏移與點擊時長的擬人化點擊
        """
        if x and y:
            # 點擊目標範圍內的隨機一個像素（防止總是點擊中心點）
            self.move_mouse_stealth(x + random.randint(-2, 2), y + random.randint(-2, 2))
        
        # --- [時空因果錨定]: 紀錄潛行點擊 ---
        try:
            from causal_nexus import karma
            karma.record_cause(
                target_file="SOVEREIGN_INPUT_GATEWAY",
                trigger_intent=f"STEALTH_CLICK: {button}",
                impact_level="LOW",
                causal_type="STEALTH_INPUT",
                pillar_anchor="P11" # 錨定至安全/潛行支柱
            )
        except: pass

        # 模擬「按下」與「彈起」之間的生物延遲
        pyautogui.mouseDown(button=button)
        time.sleep(random.uniform(0.05, 0.15))
        pyautogui.mouseUp(button=button)
        print(f"🖱️ [StealthInput] 執行擬人化點擊 ({button})")

    def type_stealth(self, text):
        """
        模擬人類打字速度波動
        """
        for char in text:
            pyautogui.write(char)
            # 每個字母間的間隔都是隨機的
            time.sleep(random.uniform(0.05, 0.2))
        print(f"⌨️ [StealthInput] 執行擬人化輸入: {len(text)} 字元")

# 單例模式
stealth_input = StealthInputGateway()
