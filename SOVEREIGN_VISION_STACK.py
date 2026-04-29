"""
HSGF - SOVEREIGN_VISION_STACK.py
Version: V9-Lite - Energy Sovereign (Optimized)
Function: High-performance perception with minimal CPU footprint via downsampling.
"""

import cv2
import numpy as np
import mmap
import time
import os
from SOVEREIGN_SCHEMA import WorldState, Entity, Relation

class VisionStack:
    def __init__(self, mmf_name="SovereignNerveLink", width=1920, height=1080):
        self.width = width
        self.height = height
        self.frame_size = width * height * 4
        self.header_size = 128
        self.total_size = self.header_size + self.frame_size
        
        # Performance Settings from Config
        from SOVEREIGN_CONFIG_LOADER import config
        res = config.get("vision_resolution")
        self.target_res = (res[0], res[1]) 
        self.scale_x = width / self.target_res[0]
        self.scale_y = height / self.target_res[1]
        self.entity_cap = config.get("entity_cap")

        try:
            self.mmf = mmap.mmap(-1, self.total_size, mmf_name)
            print(f"[HSGF_Vision] V9-Lite Linked to Nerve: {mmf_name} (Optimized Mode)")
        except Exception as e:
            print(f"[HSGF_Vision] Link Failed: {e}")
            self.mmf = None

    def read_frame(self):
        if not self.mmf: return None
        self.mmf.seek(self.header_size)
        data = self.mmf.read(self.frame_size)
        frame = np.frombuffer(data, dtype=np.uint8).reshape((self.height, self.width, 4))
        return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    def capture_and_process(self):
        raw = self.read_frame()
        if raw is None: return None, None
        
        # V9-Lite: Immediate downsampling
        small = cv2.resize(raw, self.target_res)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 50, 150)
        return small, edges

    def geometric_hash(self, contour):
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0: return 0
        circularity = 4 * np.pi * area / (perimeter**2)
        return round(circularity, 3)

    def find_elements(self, limit=5):
        from SOVEREIGN_SYMBOL_INTERPRETER import interpreter
        from SOVEREIGN_RELATION_ENGINE import relation_engine
        from SOVEREIGN_OBJECT_TRACKER import object_tracker
        
        frame, edges = self.capture_and_process()
        if frame is None: return None
        
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        detections = []
        for c in contours:
            area = cv2.contourArea(c)
            if 100 < area < 20000: # Adjusted for 640x360
                M = cv2.moments(c)
                if M["m00"] > 0:
                    detections.append({
                        "pos": (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"])),
                        "symbol": interpreter.interpret(self.geometric_hash(c))
                    })

        tracked = object_tracker.update(detections)
        tracked = sorted(tracked, key=lambda x: x["age"], reverse=True)[:limit]

        # Upscale entities back to original resolution
        entities = [
            Entity(
                id=obj["id"],
                type=obj["symbol"]["primary"],
                pos=(int(obj["pos"][0] * self.scale_x), int(obj["pos"][1] * self.scale_y)),
                velocity=(obj.get("velocity",(0,0))[0]*self.scale_x, obj.get("velocity",(0,0))[1]*self.scale_y),
                age=obj["age"],
                confidence=obj.get("confidence", 1.0)
            ) for obj in tracked
        ]

        raw_relations = relation_engine.build_topology(tracked)
        topology = [
            Relation(
                subject_id=rel["subject_id"],
                target_id=rel["target_id"],
                type=rel.get("type", "UNKNOWN"),
                distance=rel["distance"] * self.scale_x,
                tags=rel["tags"]
            ) for rel in raw_relations
        ]

        return WorldState(
            timestamp=time.time(),
            entities=entities,
            topology=topology,
            screen_resolution=(self.width, self.height)
        )

vision_stack = VisionStack()
