"""
HSGF - SOVEREIGN_RELATION_ENGINE.py
Version: V4.0 - Spatial Relation Logic
Function: Calculates topological relationships between objects.
"""

import math

class RelationEngine:
    def __init__(self):
        # Operational Thresholds (The "Operating Rules")
        self.PROXIMITY_VERY_CLOSE = 100
        self.PROXIMITY_NEAR       = 300
        self.DIRECTION_THRESHOLD  = 50
        print("[HSGF_Relation] V4.8 Persistent-ID Topology Engine Active.")

    def build_topology(self, objects):
        """
        Builds a stable relationship map based on persistent Object IDs.
        """
        relations = []

        for i, a in enumerate(objects):
            sid = a["id"]  # Use Persistent ID
            for j, b in enumerate(objects):
                if i >= j: continue 
                tid = b["id"] # Use Persistent ID

                dx = a["pos"][0] - b["pos"][0]
                dy = a["pos"][1] - b["pos"][1]
                dist = (dx**2 + dy**2)**0.5

                # 1. Base Proximity Data
                proximity = "FAR"
                if dist < self.PROXIMITY_VERY_CLOSE: proximity = "VERY_CLOSE"
                elif dist < self.PROXIMITY_NEAR:     proximity = "NEAR"

                rel_base = {
                    "distance": round(dist, 1),
                    "proximity": proximity,
                    "subject_type": a["symbol"]["primary"],
                    "target_type": b["symbol"]["primary"],
                    "subject_id": sid,
                    "target_id": tid,
                    "tags": [proximity] # Semantic Compression starts here
                }

                # 2. Symmetric Positional Relations (A relative to B)
                if abs(dx) > self.DIRECTION_THRESHOLD:
                    rel_base["tags"].append("RIGHT_OF" if dx > 0 else "LEFT_OF")

                if abs(dy) > self.DIRECTION_THRESHOLD:
                    rel_base["tags"].append("BELOW" if dy > 0 else "ABOVE")

                # 3. Dedicated Proximity Tag (Only if very close)
                if dist < self.PROXIMITY_VERY_CLOSE:
                    rel_base["tags"].append("NEAR_TO")

                relations.append(rel_base)

        return relations

# Singleton
relation_engine = RelationEngine()
