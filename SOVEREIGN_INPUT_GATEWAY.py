"""
HSGF - SOVEREIGN_INPUT_GATEWAY.py
Version: V3.7 - Physics-based Stealth Input Protocol

Core Physics:
  - Gravity-well mouse movement: trajectory follows a physics spline toward target
  - Micro-jitter decay: tremor amplitude decays as cursor approaches target
  - Bio-timing: randomized delays simulate human muscle response patterns

Usage:
    from SOVEREIGN_INPUT_GATEWAY import stealth_input
    stealth_input.move_mouse_stealth(960, 540)
    stealth_input.click_stealth(960, 540)
    stealth_input.type_stealth("hello")
"""

import time
import random
import numpy as np
import pyautogui
from scipy import interpolate


class StealthInputGateway:
    def __init__(self):
        pyautogui.PAUSE = 0  # Remove default delay - we control timing precisely
        pyautogui.FAILSAFE = True  # Move mouse to top-left corner to abort
        print("[StealthInput] Physics-based Stealth Input Gateway initialized.")

    # ------------------------------------------------------------------
    # 1. GRAVITY-WELL MOUSE MOVEMENT
    # ------------------------------------------------------------------
    def move_mouse_stealth(self, target_x, target_y, duration=None):
        """
        Move the mouse cursor using a physics-based gravity-well trajectory.

        The cursor does not travel in a straight line. Instead, it follows a
        spline path with decaying micro-jitter - tremor is large at the start
        (far from target) and diminishes as the cursor falls into the gravity well.

        Args:
            target_x (int): Target X coordinate.
            target_y (int): Target Y coordinate.
            duration (float): Travel time in seconds. Auto-calculated if None.
        """
        if duration is None:
            duration = random.uniform(0.4, 0.8)

        start_x, start_y = pyautogui.position()
        dist = np.sqrt((target_x - start_x) ** 2 + (target_y - start_y) ** 2)

        # Generate control points along the gravity gradient
        cp_count = max(4, int(dist / 100))
        x_points = np.linspace(start_x, target_x, cp_count)
        y_points = np.linspace(start_y, target_y, cp_count)

        # Inject decaying micro-jitter (simulates human hand tremor)
        for i in range(1, len(x_points) - 1):
            decay = 1.0 - (i / len(x_points))  # Decay toward 0 near target
            x_points[i] += random.gauss(0, 10 * decay)
            y_points[i] += random.gauss(0, 10 * decay)

        # Fit a smooth spline through control points
        k = 3 if len(x_points) > 3 else 1
        tck, u = interpolate.splprep([x_points, y_points], k=k, s=2)
        u_new = np.linspace(0, 1, max(10, int(duration * 60)))
        out = interpolate.splev(u_new, tck)

        # Execute movement with bio-timing delays
        for px, py in zip(out[0], out[1]):
            pyautogui.moveTo(int(px), int(py))
            time.sleep(random.uniform(0.001, 0.005))

        print(f"[Gravity] Cursor reached gravity well: ({target_x}, {target_y})")

    # ------------------------------------------------------------------
    # 2. STEALTH CLICK
    # ------------------------------------------------------------------
    def click_stealth(self, x=None, y=None, button='left'):
        """
        Perform a human-like click with randomized position offset and press duration.

        Args:
            x (int): Target X. If None, clicks at current position.
            y (int): Target Y. If None, clicks at current position.
            button (str): 'left', 'right', or 'middle'.
        """
        if x is not None and y is not None:
            # Click a random pixel within +-2px of target (avoids always hitting center)
            self.move_mouse_stealth(
                x + random.randint(-2, 2),
                y + random.randint(-2, 2)
            )

        # Simulate biological press/release delay
        pyautogui.mouseDown(button=button)
        time.sleep(random.uniform(0.05, 0.15))
        pyautogui.mouseUp(button=button)
        print(f"[StealthInput] Click executed ({button}) at ({x}, {y})")

    # ------------------------------------------------------------------
    # 3. STEALTH TYPING
    # ------------------------------------------------------------------
    def type_stealth(self, text, wpm_range=(40, 80)):
        """
        Type text with randomized inter-key delays to simulate human typing speed.

        Args:
            text (str): Text to type.
            wpm_range (tuple): Min and max words per minute range.
        """
        # Convert WPM to seconds per character
        avg_wpm = random.uniform(*wpm_range)
        base_delay = 60.0 / (avg_wpm * 5)  # ~5 chars per word

        for char in text:
            pyautogui.write(char)
            # Add random variance to each keystroke timing
            time.sleep(base_delay * random.uniform(0.5, 1.8))

        print(f"[StealthInput] Typed {len(text)} characters at ~{avg_wpm:.0f} WPM.")


# Default singleton
stealth_input = StealthInputGateway()
