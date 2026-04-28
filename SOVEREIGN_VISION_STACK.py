"""
HSGF - SOVEREIGN_VISION_STACK.py
Version: V3.0 - Full Sovereign Perception Engine

Improvements in V3.0:
  1. Local entropy (ROI-based) replaces global entropy
  2. geometric_hash() integrated into find_element return value
  3. HSV color channel detection (e.g., YELLOW_LINE, RED_ZONE)

Core Capabilities:
  - Screen capture with adaptive local entropy gating
  - Real geometric element detection via contour analysis
  - Geometric hashing for element fingerprinting
  - HSV color-based target detection
"""

import cv2
import numpy as np
import pyautogui


# HSV color range presets (H, S, V - min/max)
COLOR_PRESETS = {
    "YELLOW":   ([20, 80, 80],   [35, 255, 255]),
    "RED":      ([0, 120, 70],   [10, 255, 255]),
    "GREEN":    ([40, 60, 60],   [80, 255, 255]),
    "BLUE":     ([100, 80, 50],  [130, 255, 255]),
    "WHITE":    ([0, 0, 180],    [180, 30, 255]),
    "ORANGE":   ([10, 100, 100], [20, 255, 255]),
}


class VisionStack:
    def __init__(self):
        print("[HSGF_Vision] Sovereign Vision Stack V3.0 initialized.")
        self.entropy_threshold = 4.5

    # ------------------------------------------------------------------
    # 1. SCREEN CAPTURE
    # ------------------------------------------------------------------
    def capture_and_process(self, roi=None):
        """
        Capture screen and return (raw_frame, edge_frame).

        Args:
            roi: Optional (x, y, w, h) region of interest for local processing.
                 If None, processes full screen.
        """
        screenshot = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Local entropy: use ROI if provided, else full frame
        entropy_region = self._crop_roi(gray, roi) if roi else gray
        entropy = self._calculate_entropy(entropy_region)

        if entropy > self.entropy_threshold:
            gray = cv2.GaussianBlur(gray, (7, 7), 0)
            print(f"[Vision] High local entropy ({entropy:.2f}) - noise filter active.")
        else:
            gray = cv2.GaussianBlur(gray, (3, 3), 0)

        edges = cv2.Canny(gray, 50, 150)
        return frame, edges

    def _crop_roi(self, frame, roi):
        """Crop frame to region of interest (x, y, w, h)."""
        x, y, w, h = roi
        return frame[y:y+h, x:x+w]

    # ------------------------------------------------------------------
    # 2. LOCAL SHANNON ENTROPY
    # ------------------------------------------------------------------
    def _calculate_entropy(self, gray_region):
        """
        Compute Shannon entropy of a grayscale region.

        Local entropy is more meaningful than global:
        - A dark tarmac with one bright reflection = locally high entropy
        - A globally "average" frame may hide dangerous local chaos

        Returns:
            float: Entropy value. Higher = more chaotic/noisy.
        """
        hist = cv2.calcHist([gray_region], [0], None, [256], [0, 256])
        hist = hist / hist.sum()
        hist = hist[hist > 0]
        return float(-np.sum(hist * np.log2(hist)))

    def get_local_entropy(self, cx, cy, radius=50):
        """
        Calculate entropy around a specific point on screen.
        Useful for the agent to assess local environment quality.

        Args:
            cx, cy: Center point of interest.
            radius: Region radius in pixels.

        Returns:
            float: Local entropy value.
        """
        screenshot = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        roi = (max(0, cx-radius), max(0, cy-radius), radius*2, radius*2)
        region = self._crop_roi(gray, roi)
        return self._calculate_entropy(region)

    # ------------------------------------------------------------------
    # 3. GEOMETRIC HASH
    # ------------------------------------------------------------------
    def geometric_hash(self, contour):
        """
        Generate a geometric fingerprint for a contour.
        Used for element identification and classification.

        Returns:
            dict: {area, aspect_ratio, circularity, solidity, bbox}
        """
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        x, y, w, h = cv2.boundingRect(contour)
        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)

        aspect_ratio  = round(w / h, 3) if h > 0 else 0
        circularity   = round(4 * np.pi * area / (perimeter ** 2), 3) if perimeter > 0 else 0
        solidity      = round(area / hull_area, 3) if hull_area > 0 else 0

        return {
            "area":         int(area),
            "aspect_ratio": aspect_ratio,
            "circularity":  circularity,
            "solidity":     solidity,  # 1.0 = convex shape, <1.0 = concave/complex
            "bbox":         (x, y, w, h),
        }

    # ------------------------------------------------------------------
    # 4. FIND ELEMENT (Real Detection + Hash Return)
    # ------------------------------------------------------------------
    def find_element(self, element_type, min_area=500, max_area=50000, roi=None):
        """
        Detect geometric elements on screen using contour analysis.

        Args:
            element_type: Detection strategy:
                'LARGEST'       - largest contour by area
                'CIRCLE'        - most circular contour
                'RECTANGLE'     - most rectangular contour (4 vertices)
                'BRIGHT_REGION' - brightest region on screen
                'YELLOW_LINE'   - yellow color channel detection
                'RED_ZONE'      - red color channel detection
                'GREEN_TARGET'  - green color channel detection
                'BLUE_MARKER'   - blue color channel detection
                'WHITE_LINE'    - white color channel detection
            min_area: Minimum contour area to consider.
            max_area: Maximum contour area.
            roi: Optional (x, y, w, h) to restrict search area.

        Returns:
            tuple: ((cx, cy), confidence, geo_hash)
                   geo_hash is a dict with shape descriptors.
                   Returns (None, 0.0, {}) if nothing found.
        """
        # Color-based detection
        color_map = {
            "YELLOW_LINE":   "YELLOW",
            "RED_ZONE":      "RED",
            "GREEN_TARGET":  "GREEN",
            "BLUE_MARKER":   "BLUE",
            "WHITE_LINE":    "WHITE",
            "ORANGE_CONE":   "ORANGE",
        }
        if element_type in color_map:
            return self._find_by_color(color_map[element_type], min_area)

        # Geometry-based detection
        frame, edges = self.capture_and_process(roi=roi)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        valid = [c for c in contours if min_area < cv2.contourArea(c) < max_area]

        if not valid:
            return None, 0.0, {}

        if element_type == "LARGEST":
            return self._find_largest(valid)
        elif element_type == "CIRCLE":
            return self._find_most_circular(valid)
        elif element_type == "RECTANGLE":
            return self._find_most_rectangular(valid)
        elif element_type == "BRIGHT_REGION":
            return self._find_brightest(frame)
        else:
            return self._find_largest(valid)

    # Internal geometry detectors (now return geo_hash)
    def _find_largest(self, contours):
        largest = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest)
        if M["m00"] == 0:
            return None, 0.0, {}
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        confidence = min(cv2.contourArea(largest) / 10000.0, 1.0)
        return (cx, cy), round(confidence, 3), self.geometric_hash(largest)

    def _find_most_circular(self, contours):
        best, best_score = None, 0.0
        for c in contours:
            area = cv2.contourArea(c)
            perimeter = cv2.arcLength(c, True)
            if perimeter == 0:
                continue
            circularity = 4 * np.pi * area / (perimeter ** 2)
            if circularity > best_score:
                best_score = circularity
                best = c
        if best is None:
            return None, 0.0, {}
        M = cv2.moments(best)
        if M["m00"] == 0:
            return None, 0.0, {}
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        return (cx, cy), round(best_score, 3), self.geometric_hash(best)

    def _find_most_rectangular(self, contours):
        best, best_score = None, 0.0
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)
            if len(approx) == 4:
                area = cv2.contourArea(c)
                x, y, w, h = cv2.boundingRect(c)
                fill_ratio = area / (w * h) if w * h > 0 else 0
                if fill_ratio > best_score:
                    best_score = fill_ratio
                    best = c
        if best is None:
            return None, 0.0, {}
        x, y, w, h = cv2.boundingRect(best)
        return (x + w // 2, y + h // 2), round(best_score, 3), self.geometric_hash(best)

    def _find_brightest(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None, 0.0, {}
        largest = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest)
        if M["m00"] == 0:
            return None, 0.0, {}
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        return (cx, cy), 0.8, self.geometric_hash(largest)

    # ------------------------------------------------------------------
    # 5. COLOR-BASED DETECTION (HSV channel)
    # ------------------------------------------------------------------
    def _find_by_color(self, color_name, min_area=500):
        """
        Detect elements by HSV color range.
        Useful for finding runway yellow lines, red zones, etc.

        Args:
            color_name: Key in COLOR_PRESETS.
            min_area: Minimum blob area.

        Returns:
            tuple: ((cx, cy), confidence, geo_hash)
        """
        if color_name not in COLOR_PRESETS:
            print(f"[Vision] Unknown color '{color_name}'. Available: {list(COLOR_PRESETS.keys())}")
            return None, 0.0, {}

        screenshot = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower, upper = COLOR_PRESETS[color_name]
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))

        # Special case: red wraps around hue=180
        if color_name == "RED":
            lower2, upper2 = [170, 120, 70], [180, 255, 255]
            mask2 = cv2.inRange(hsv, np.array(lower2), np.array(upper2))
            mask = cv2.bitwise_or(mask, mask2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        valid = [c for c in contours if cv2.contourArea(c) > min_area]

        if not valid:
            return None, 0.0, {}

        largest = max(valid, key=cv2.contourArea)
        M = cv2.moments(largest)
        if M["m00"] == 0:
            return None, 0.0, {}

        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        confidence = min(cv2.contourArea(largest) / 5000.0, 1.0)

        return (cx, cy), round(confidence, 3), self.geometric_hash(largest)


# Default singleton
vision_stack = VisionStack()
