"""
[戰術代號: SOVEREIGN_VISION_STACK.py]
[主權版本: V3.5 - Multi-layered Vision Stack]
[功能: 整合符號視覺、像素匹配與語義理解的三層次感官系統]
"""

import time
import cv2
import numpy as np
import pyautogui
from SOVEREIGN_SYMBOLIC_EYE import symbolic_eye
from SOVEREIGN_VISION_EYE import vision_eye # 雲端/本地 VLM

class SovereignVisionStack:
    def __init__(self):
        print("👁️ [VisionStack] 多層次視覺系統已就緒。")

    def find_element(self, target_name, hint_image=None):
        """
        [主權感知切換]: 自動遞進式檢索目標
        """
        # --- Level 1: 數位原生感知 (Digital Native / Symbolic) ---
        print(f"[*] [Layer_1] 嘗試數位直感: {target_name}")
        symbol = symbolic_eye.find_symbol_by_name(target_name)
        
        if symbol:
            print(f"✅ [Layer_1] 數位命中: {symbol['name']}")
            return symbol['pos'], "DIGITAL_NATIVE"

        # --- [切換觸發]: 當數位路徑失效，自動激活備案 ---
        print(f"⚠️ [Perception_Switch] 數位路徑盲區，啟動視覺備案...")
        
        # 紀錄因果斷裂與感知升級
        try:
            from causal_nexus import karma
            karma.record_cause(
                target_file="SOVEREIGN_VISION_STACK",
                trigger_intent=f"PERCEPTION_ESCALATION: {target_name}",
                impact_level="MEDIUM",
                causal_type="SENSOR_SWITCH",
                pillar_anchor="P27"
            )
        except: pass

        # --- Level 2: 視覺模擬 (Visual Simulation / VLM) ---
        # 如果有提供模板圖片，優先嘗試 OpenCV
        if hint_image:
            print(f"[*] [Layer_2] 執行像素級對沖...")
            pos = self._opencv_match(hint_image)
            if pos: return pos, "PIXEL_MATCH"

        # 最終手段：語義視覺
        print(f"[*] [Layer_3] 執行語義深度解讀 (VLM)...")
        vlm_res = vision_eye.capture_and_analyze(f"在螢幕上找到 {target_name} 並給出座標。")
        
        if "coordinates" in vlm_res:
            # 轉換為實體座標 (假設 VLM 回傳的是 0-1000 的標準化座標)
            screen_w, screen_h = pyautogui.size()
            x = int(vlm_res["coordinates"][0] * screen_w / 1000)
            y = int(vlm_res["coordinates"][1] * screen_h / 1000)
            return (x, y), "VISUAL_SEMANTIC"

        return None, "VISION_COLLAPSE"

    def _opencv_match(self, template_path):
        """簡單的 OpenCV 模板匹配實作"""
        try:
            screen = np.array(pyautogui.screenshot())
            screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
            template = cv2.imread(template_path)
            res = cv2.matchTemplate(screen, template, cv2.match.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            
            if max_val > 0.8: # 置信度閾值
                h, w = template.shape[:2]
                return (max_loc[0] + w//2, max_loc[1] + h//2)
        except:
            pass
        return None

# 單例模式
vision_stack = SovereignVisionStack()
