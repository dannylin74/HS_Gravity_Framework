"""
HSGF - SOVEREIGN_OBJECT_TRACKER.py
Version: V4.5 - Temporal Identity + Velocity System
Function: 
  - Persistent object identity (Matching ID)
  - Velocity and Speed estimation
  - Movement trajectory continuity
"""

import math
import time

class ObjectTracker:
    def __init__(self, max_distance=100, max_lost=5):
        print("[ObjectTracker] V4.5 Temporal Engine Online.")
        self.next_id = 0
        self.tracks = {}  # id -> {pos, symbol, last_seen, lost, age, velocity, speed}
        self.max_distance = max_distance
        self.max_lost = max_lost

    def update(self, current_detections):
        """
        Updates tracks with current frame detections.
        """
        updated_tracks = {}
        used_ids = set()

        # 1. Match current detections to existing tracks
        for det in current_detections:
            best_id = None
            best_dist = float("inf")

            for tid, track in self.tracks.items():
                if tid in used_ids: continue
                
                dist = self._calculate_distance(det["pos"], track["pos"])
                if dist < best_dist and dist < self.max_distance:
                    best_dist = dist
                    best_id = tid

            if best_id is not None:
                # MATCH FOUND: Update track
                prev_track = self.tracks[best_id]
                vx = det["pos"][0] - prev_track["pos"][0]
                vy = det["pos"][1] - prev_track["pos"][1]
                speed = math.sqrt(vx*vx + vy*vy)

                updated_tracks[best_id] = {
                    "id": best_id,
                    "pos": det["pos"],
                    "symbol": det["symbol"],
                    "velocity": (vx, vy),
                    "speed": round(speed, 2),
                    "lost": 0,
                    "age": prev_track["age"] + 1,
                    "last_seen": time.time()
                }
                used_ids.add(best_id)
            else:
                # NEW OBJECT: Assign new ID
                new_id = self.next_id
                self.next_id += 1
                updated_tracks[new_id] = {
                    "id": new_id,
                    "pos": det["pos"],
                    "symbol": det["symbol"],
                    "velocity": (0, 0),
                    "speed": 0.0,
                    "lost": 0,
                    "age": 1,
                    "last_seen": time.time()
                }

        # 2. Maintain lost tracks (Persistence + Prediction)
        for tid, track in self.tracks.items():
            if tid not in updated_tracks:
                track["lost"] += 1
                if track["lost"] <= self.max_lost:
                    # LINEAR EXTRAPOLATION: Predict next position based on velocity
                    vx, vy = track.get("velocity", (0, 0))
                    track["pos"] = (track["pos"][0] + vx, track["pos"][1] + vy)
                    
                    # Reduce confidence over time while lost
                    if "confidence" in track["symbol"]:
                        track["symbol"]["confidence"] = max(0, track["symbol"]["confidence"] - 0.1)
                        
                    updated_tracks[tid] = track

        self.tracks = updated_tracks
        return list(self.tracks.values())

    def _calculate_distance(self, p1, p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# Singleton
object_tracker = ObjectTracker()
