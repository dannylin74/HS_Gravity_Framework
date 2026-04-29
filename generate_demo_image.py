"""
HSGF - generate_demo_image.py (REALITY EDITION)
Captures the ACTUAL screen and processes it through the HSGF V3.0 engine.
Shows exactly what the agent "sees" mathematically.
"""

import cv2
import numpy as np
import pyautogui
from SOVEREIGN_VISION_STACK import vision_stack
from SOVEREIGN_SEMANTIC_DEDUCTOR import SemanticDeductor

def generate_real_demo():
    print("[HSGF] Capturing real-world reality...")
    
    # 1. Capture Actual Screen
    screenshot = pyautogui.screenshot()
    raw_scene = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    h, w = raw_scene.shape[:2]
    
    # 2. Run Sovereign Analysis
    # We use the same logic the agent uses
    _, edges = vision_stack.capture_and_process()
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    valid = [c for c in contours if 500 < cv2.contourArea(c) < 50000]
    
    # 3. Create Mathematical Perception Frame
    analysis = np.zeros_like(raw_scene)
    analysis[:] = (15, 15, 25) # Agent's dark canvas
    
    # Draw Entropy Grid (The "feeling" of information density)
    gray = cv2.cvtColor(raw_scene, cv2.COLOR_BGR2GRAY)
    gs = 120 # Grid size
    for y in range(0, h, gs):
        for x in range(0, w, gs):
            roi = gray[y:y+gs, x:x+gs]
            if roi.size == 0: continue
            entropy = vision_stack._calculate_entropy(roi)
            # Normalize entropy for visualization (typically 0-7)
            alpha = min(entropy / 6.0, 1.0)
            color = (int(200 * alpha), int(50 * (1-alpha)), 30)
            cv2.rectangle(analysis, (x, y), (x+gs, y+gs), color, 1)
    
    # Draw Geometric Primitives & Hashes
    for i, c in enumerate(valid[:8]):
        M = cv2.moments(c)
        if M["m00"] == 0: continue
        cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
        ghash = vision_stack.geometric_hash(c)
        
        # Draw the detected "Symbol"
        cv2.drawContours(analysis, [c], -1, (0, 255, 100), 1)
        cv2.drawMarker(analysis, (cx, cy), (0, 255, 100), cv2.MARKER_CROSS, 15, 1)
        
        # Numeric Data for the Agent
        cv2.putText(analysis, f"SYM_{i}: ({cx},{cy})", (cx + 10, cy - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        cv2.putText(analysis, f"GH:{ghash['circularity']:.2f}", (cx + 10, cy + 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 100), 1)

    # 4. Compose Side-by-Side Comparison
    # Resize for manageable GitHub display if necessary (optional)
    display_w = 960
    display_h = int(h * (display_w / w))
    
    raw_small = cv2.resize(raw_scene, (display_w, display_h))
    analysis_small = cv2.resize(analysis, (display_w, display_h))
    
    header = np.zeros((80, display_w * 2 + 4, 3), dtype=np.uint8)
    cv2.putText(header, "RAW REALITY", (display_w//2 - 80, 50), 
                cv2.FONT_HERSHEY_DUPLEX, 0.8, (200, 200, 200), 1)
    cv2.putText(header, "SOVEREIGN MATHEMATICAL PERCEPTION", (display_w + display_w//2 - 200, 50), 
                cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 255), 1)
    
    divider = np.ones((display_h, 4, 3), dtype=np.uint8) * 60
    composite = np.hstack([raw_small, divider, analysis_small])
    final = np.vstack([header, composite])
    
    cv2.imwrite("hsgf_demo.jpg", final)
    print(f"[SUCCESS] Real-world demo generated: hsgf_demo.jpg ({w}x{h} source)")

if __name__ == "__main__":
    generate_real_demo()
