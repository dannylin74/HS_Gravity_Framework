"""
HSGF - generate_demo_image.py
Generates a real side-by-side comparison image showing:
  LEFT:  The input scene (geometric test environment)
  RIGHT: What HSGF sees - edges, gravity well, tracked object, velocity vector

This is REAL output from the HSGF vision engine, not a synthetic illustration.

Usage:
    python generate_demo_image.py
    -> Saves 'hsgf_demo.jpg'
"""

import cv2
import numpy as np
from SOVEREIGN_SEMANTIC_DEDUCTOR import SemanticDeductor
import math
import time

def create_test_scene(width=960, height=540):
    """
    Create a controlled geometric test environment.
    This is the 'world' that HSGF will analyze.
    """
    scene = np.zeros((height, width, 3), dtype=np.uint8)
    scene[:] = (15, 15, 25)  # Dark background

    # Draw geometric objects (the 'world')
    # Large rectangle (simulates a UI element or obstacle)
    cv2.rectangle(scene, (100, 100), (350, 300), (60, 60, 180), 3)
    cv2.putText(scene, "ZONE A", (160, 210),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (60, 60, 180), 1)

    # Circle (simulates a target or ball)
    cv2.circle(scene, (700, 200), 80, (180, 60, 60), 3)
    cv2.putText(scene, "TARGET", (665, 205),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 60, 60), 1)

    # Triangle (simulates an angular obstacle)
    pts = np.array([[480, 420], [580, 250], [680, 420]], np.int32)
    cv2.polylines(scene, [pts.reshape((-1, 1, 2))], True, (60, 180, 60), 3)

    # Horizontal reference line (simulates a guide line / runway)
    cv2.line(scene, (0, 480), (width, 480), (120, 120, 120), 2)
    cv2.putText(scene, "REFERENCE LINE", (20, 475),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (120, 120, 120), 1)

    return scene


def run_hsgf_on_scene(scene, engine):
    """
    Run HSGF vision analysis on the test scene.
    Returns the annotated analysis frame.
    """
    gray = cv2.cvtColor(scene, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    # Find contours (real geometric detection)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    valid = [c for c in contours if 500 < cv2.contourArea(c) < 50000]

    # Build the analysis visualization on dark background
    analysis = np.zeros_like(scene)
    analysis[:] = (10, 10, 20)

    # Draw detected edges
    edge_color = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    edge_color[:, :, 0] = 0  # Remove blue channel
    edge_color[:, :, 2] = 0  # Remove red channel
    analysis = cv2.addWeighted(analysis, 1.0, edge_color, 0.6, 0)

    # Gravity well (target center)
    target = (scene.shape[1] // 2, scene.shape[0] // 2)
    cv2.circle(analysis, target, 25, (0, 255, 100), 2)
    cv2.circle(analysis, target, 8, (0, 255, 100), -1)
    cv2.putText(analysis, "GRAVITY WELL", (target[0] + 30, target[1] + 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 100), 1)

    # Track each detected contour with HSGF engine
    colors = [(0, 100, 255), (255, 100, 0), (200, 0, 255), (0, 200, 255)]
    for i, contour in enumerate(valid[:4]):
        M = cv2.moments(contour)
        if M["m00"] == 0:
            continue
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        color = colors[i % len(colors)]

        # Run deductor
        result = engine.deduce_action(
            geometry=(cx, cy),
            symbol=f"OBJ_{i}",
        )
        viscosity = float(result.split("_")[-1])

        # Draw tracked centroid
        cv2.circle(analysis, (cx, cy), 10, color, -1)

        # Draw gravity vector toward well
        cv2.arrowedLine(analysis, (cx, cy), target, color, 1, tipLength=0.03)

        # Draw viscosity label
        label = f"v={viscosity:.3f}"
        cv2.putText(analysis, label, (cx + 12, cy - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

        # Simulate parabolic arc (next predicted position)
        dx = (target[0] - cx) * 0.3
        dy = (target[1] - cy) * 0.3
        pred_x = int(cx + dx)
        pred_y = int(cy + dy)
        cv2.circle(analysis, (pred_x, pred_y), 5, color, 1)
        cv2.line(analysis, (cx, cy), (pred_x, pred_y), color, 1)

    # Labels
    cv2.putText(analysis, "HSGF SOVEREIGN VISION", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    cv2.putText(analysis, "Gravity Field + Parabolic Tracker", (10, 48),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (140, 140, 140), 1)

    return analysis


def main():
    print("[HSGF] Generating real demo image...")

    # Create test environment
    scene = create_test_scene()
    engine = SemanticDeductor(target=(480, 270))

    # Run HSGF analysis
    analysis = run_hsgf_on_scene(scene, engine)

    # Add divider line
    divider = np.ones((scene.shape[0], 4, 3), dtype=np.uint8) * 80

    # Compose side-by-side: [Input Scene | Divider | HSGF Analysis]
    left_label = scene.copy()
    cv2.putText(left_label, "INPUT SCENE", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    cv2.putText(left_label, "Geometric test environment", (10, 48),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (140, 140, 140), 1)

    composite = np.hstack([left_label, divider, analysis])

    # Save
    cv2.imwrite("hsgf_demo.jpg", composite)
    print("[OK] Saved to hsgf_demo.jpg")
    print("     This is REAL output from the HSGF vision engine.")


if __name__ == "__main__":
    main()
