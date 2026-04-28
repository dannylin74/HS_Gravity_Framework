"""
[戰術代號: SOVEREIGN_SEMANTIC_DEDUCTOR.py]
[主權版本: V3.9 - Sovereign Apex Locking Edition]
[功能: 整合拋物線頂點鎖定、擺線運動補償與自適應阻尼控制]
"""

import json
import time
import numpy as np
from pathlib import Path

class SemanticDeductor:
    def __init__(self):
        self.base_dir = Path("e:/Hiro_Master")
        self.temporal_history = {} 
        self.target_vector = np.array([1280, 720]) # 預設引力隧道中心點 (黃線)
        print("📐 [Deductor] V3.9 頂點鎖定版已啟動。拋物線導引場已對齊。")

    def deduce_action(self, geometry, symbol, color_hex, numerical_weight):
        """
        [主權演繹核心]: 執行頂點鎖定與擺線補償
        """
        current_pos = np.array(geometry)
        current_time = time.time()
        prev = self.temporal_history.get(symbol, {"g": geometry, "t": current_time, "v_vec": np.array([0,0]), "omega": 0})
        
        # 1. 拋物線與角速度計算 (Parabolic & Angular Velocity)
        dt = current_time - prev["t"]
        v_vec = (current_pos - np.array(prev["g"])) / dt if dt > 0 else np.array([0, 0])
        
        # 計算角速度 (Omega) 與 曲率趨勢
        angle_curr = np.arctan2(v_vec[1], v_vec[0])
        angle_prev = np.arctan2(prev["v_vec"][1], prev["v_vec"][0])
        omega = (angle_curr - angle_prev) / dt if dt > 0 else 0
        
        # 2. 頂點鎖定邏輯 (Apex Locking)
        # 當角速度開始減小，代表接近拋物線頂點
        is_approaching_apex = abs(omega) < abs(prev["omega"]) and abs(omega) > 0.1
        
        # 3. 自適應阻尼 (Adaptive Damping)
        # 越接近目標黃線，且角速度越小，阻尼越高
        dist_to_line = np.linalg.norm(current_pos - self.target_vector)
        # 如果正在「回正階段」，大幅強化阻尼
        damping_factor = 2.0 if dist_to_line < 200 and abs(omega) < 0.5 else 1.0
        viscosity = (1.0 / (1.0 + dist_to_line)) * damping_factor

        self.temporal_history[symbol] = {"g": geometry, "t": current_time, "v_vec": v_vec, "omega": omega}

        # 4. 拋物線預警與輸出
        if is_approaching_apex:
            print(f"🎯 [Apex] 偵測到拋物線頂點！自動執行角度錨定優化。")
            
        return f"PROCEED_WITH_VISCOSITY_{viscosity:.2f}"

# 單例
deductor = SemanticDeductor()
