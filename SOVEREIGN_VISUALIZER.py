"""
[戰術代號: SOVEREIGN_VISUALIZER.py]
[主權版本: V1.0 - Vision Debugger]
[功能: 實時渲染 HSGF 的引力場、拋物線與幾何骨架，用於 Demo 與除錯]
"""

import cv2
import numpy as np
from SOVEREIGN_VISION_STACK import vision_stack
from SOVEREIGN_SEMANTIC_DEDUCTOR import deductor

def start_visualization():
    print("👁️ [Visualizer] 正在開啟主權視界...")
    
    while True:
        # 1. 抓取螢幕與幾何骨架
        frame, edges = vision_stack.capture_and_process()
        
        # 2. 獲取當前演繹狀態
        # 模擬一個目標點 (例如螢幕中心)
        target = np.array([960, 540]) 
        
        # 3. 繪製視覺化圖層
        viz_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        # 繪製引力中心 (Target)
        cv2.circle(viz_frame, tuple(target), 20, (0, 255, 0), 2)
        cv2.putText(viz_frame, "GRAVITY_WELL", (target[0]+25, target[1]), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # 繪製拋物線趨勢 (從歷史中讀取)
        for symbol, data in deductor.temporal_history.items():
            pos = tuple(map(int, data["g"]))
            v = data["v_vec"]
            # 繪製速度向量
            cv2.arrowedLine(viz_frame, pos, (int(pos[0]+v[0]*10), int(pos[1]+v[1]*10)), (255, 0, 0), 2)
            
        # 4. 儲存畫面進行驗證 (代替彈出視窗)
        cv2.imwrite("debug_vision.jpg", viz_frame)
        print("📸 [Visualizer] 已捕獲主權視界並存至 debug_vision.jpg。請查看該檔案以驗證邏輯。")
        break # 執行一次即可

    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_visualization()
