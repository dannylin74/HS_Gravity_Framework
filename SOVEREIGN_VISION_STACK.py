"""
HSGF - SOVEREIGN_VISION_STACK.py
Version: V2.0 - Real Geometric Perception Engine

Core Capabilities:
  1. Screen capture with adaptive entropy gating
  2. Real geometric element detection via contour analysis
  3. Shannon entropy measurement for environment quality assessment
  4. Geometric hashing for element identification
"""

import cv2
import numpy as np
import pyautogui


class VisionStack:
    def __init__(self):
        print("[HSGF_Vision] Sovereign Vision Stack V2.0 initialized.")
        self.entropy_threshold = 4.5  # High entropy = noisy environment
        self.last_entropy = 0.0

    # ------------------------------------------------------------------
    # 1. SCREEN CAPTURE
    # ------------------------------------------------------------------
    def capture_and_process(self):
        """Capture screen and return (raw_frame, edge_frame)."""
        screenshot = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Adaptive preprocessing based on environment entropy
        self.last_entropy = self._calculate_entropy(gray)
        if self.last_entropy > self.entropy_threshold:
            # High entropy (noisy) - apply stronger smoothing first
            gray = cv2.GaussianBlur(gray, (7, 7), 0)
            print(f"[Vision] High entropy ({self.last_entropy:.2f}) - activating noise filter.")
        else:
            gray = cv2.GaussianBlur(gray, (3, 3), 0)

        edges = cv2.Canny(gray, 50, 150)
        return frame, edges

    # ------------------------------------------------------------------
    # 2. SHANNON ENTROPY (Environment Quality Sensor)
    # ------------------------------------------------------------------
    def _calculate_entropy(self, gray_frame):
        """
        Compute Shannon entropy of the grayscale frame.
        High entropy = chaotic/noisy environment.
        Low entropy  = clean/structured environment.
        """
        hist = cv2.calcHist([gray_frame], [0], None, [256], [0, 256])
        hist = hist / hist.sum()  # Normalize to probability distribution
        hist = hist[hist > 0]     # Remove zero entries
        entropy = -np.sum(hist * np.log2(hist))
        return float(entropy)

    # ------------------------------------------------------------------
    # 3. FIND ELEMENT (Real Geometric Detection)
    # ------------------------------------------------------------------
    def find_element(self, element_type, min_area=500, max_area=50000):
        """
        Detect geometric elements on screen using contour analysis.

        Args:
            element_type: Target type. Supported:
                          'LARGEST'      - find the largest shape
                          'CIRCLE'       - find the most circular shape
                          'RECTANGLE'    - find the most rectangular shape
                          'BRIGHT_REGION'- find the brightest region
            min_area: Minimum contour area to consider (filters noise).
            max_area: Maximum contour area (filters full-screen blobs).

        Returns:
            tuple: ((cx, cy), confidence)
                   (cx, cy)    = center of detected element
                   confidence  = detection confidence [0.0, 1.0]
                   Returns (None, 0.0) if nothing found.
        """
        frame, edges = self.capture_and_process()
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter by area
        valid = [c for c in contours if min_area < cv2.contourArea(c) < max_area]
        if not valid:
            return None, 0.0

        if element_type == "LARGEST":
            return self._find_largest(valid)

        elif element_type == "CIRCLE":
            return self._find_most_circular(valid)

        elif element_type == "RECTANGLE":
            return self._find_most_rectangular(valid)

        elif element_type == "BRIGHT_REGION":
            return self._find_brightest(frame)

        else:
            # Default: return centroid of largest contour
            return self._find_largest(valid)

    def _find_largest(self, contours):
        """Return centroid of the largest contour."""
        largest = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest)
        if M["m00"] == 0:
            return None, 0.0
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        area = cv2.contourArea(largest)
        confidence = min(area / 10000.0, 1.0)
        return (cx, cy), confidence

    def _find_most_circular(self, contours):
        """
        Find the most circle-like contour.
        Circularity = 4*pi*Area / Perimeter^2 (1.0 = perfect circle)
        """
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
            return None, 0.0

        M = cv2.moments(best)
        if M["m00"] == 0:
            return None, 0.0
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        return (cx, cy), round(best_score, 3)

    def _find_most_rectangular(self, contours):
        """
        Find the most rectangle-like contour.
        Uses approxPolyDP to check if shape has 4 vertices.
        """
        best, best_score = None, 0.0
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)
            if len(approx) == 4:
                area = cv2.contourArea(c)
                x, y, w, h = cv2.boundingRect(c)
                rect_area = w * h
                fill_ratio = area / rect_area if rect_area > 0 else 0
                if fill_ratio > best_score:
                    best_score = fill_ratio
                    best = c

        if best is None:
            return None, 0.0

        x, y, w, h = cv2.boundingRect(best)
        return (x + w // 2, y + h // 2), round(best_score, 3)

    def _find_brightest(self, frame):
        """Find the centroid of the brightest region on screen."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None, 0.0
        largest = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest)
        if M["m00"] == 0:
            return None, 0.0
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        return (cx, cy), 0.8

    # ------------------------------------------------------------------
    # 4. GEOMETRIC HASH (Element Fingerprinting)
    # ------------------------------------------------------------------
    def geometric_hash(self, contour):
        """
        Generate a simple geometric signature for a contour.
        Returns a dict with shape descriptors for element identification.
        """
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = round(w / h, 3) if h > 0 else 0
        circularity = round(4 * np.pi * area / (perimeter ** 2), 3) if perimeter > 0 else 0

        return {
            "area": int(area),
            "aspect_ratio": aspect_ratio,
            "circularity": circularity,
            "bbox": (x, y, w, h)
        }


# Default singleton
vision_stack = VisionStack()
