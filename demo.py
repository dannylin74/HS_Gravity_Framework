"""
HSGF Quick Demo - Run this to see the Gravity Engine in action.

Usage:
    python demo.py

What you will see:
    - Real-time screen capture with edge detection
    - A simulated moving object tracked across frames
    - Parabolic apex detection printed to console
    - Viscosity (damping) coefficient computed per frame
    - Output saved as 'demo_output.jpg'
"""

import cv2
import numpy as np
import pyautogui
import time
import math
from SOVEREIGN_SEMANTIC_DEDUCTOR import SemanticDeductor


def run_demo():
    print("=" * 50)
    print("  HSGF - Hiro Sovereign Gravity Framework")
    print("  Demo: Gravity Field + Parabolic Tracker")
    print("=" * 50)

    # Initialize gravity engine with screen center as the gravity well
    screen_w, screen_h = pyautogui.size()
    target = (screen_w // 2, screen_h // 2)
    engine = SemanticDeductor(target=target)

    print(f"\n[*] Gravity well set at screen center: {target}")
    print("[*] Capturing 10 frames and tracking a simulated object...\n")

    output_frame = None

    for i in range(10):
        # Capture screen
        screenshot = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Simulate a moving object (circular path around screen center)
        t = i / 10.0 * 2 * math.pi
        obj_x = int(screen_w // 2 + 300 * math.cos(t))
        obj_y = int(screen_h // 2 + 200 * math.sin(t))
        obj_pos = (obj_x, obj_y)

        # Run gravity engine
        result = engine.deduce_action(
            geometry=obj_pos,
            symbol="DEMO_OBJECT",
            color_hex="#FF0000",
            numerical_weight=1.0
        )
        print(f"  Frame {i+1:02d} | Position: {obj_pos} | {result}")

        # Build visualization frame from edge detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        output_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Draw gravity well
        cv2.circle(output_frame, target, 30, (0, 255, 0), 2)
        cv2.putText(output_frame, "GRAVITY WELL", (target[0] + 35, target[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

        # Draw tracked object
        cv2.circle(output_frame, obj_pos, 15, (0, 0, 255), -1)
        cv2.putText(output_frame, "TRACKED", (obj_pos[0] + 20, obj_pos[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # Draw gravity vector (arrow from object toward well)
        cv2.arrowedLine(output_frame, obj_pos, target, (255, 128, 0), 2)

        time.sleep(0.1)

    # Save final visualization
    cv2.imwrite("demo_output.jpg", output_frame)
    print("\n[OK] Demo complete! Output saved to 'demo_output.jpg'")
    print("     Open the image to see the Gravity Field visualization.")


if __name__ == "__main__":
    run_demo()
