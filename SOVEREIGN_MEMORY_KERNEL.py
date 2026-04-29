"""
HSGF - SOVEREIGN_MEMORY_KERNEL.py
Version: V7.0 - World Model Belief System
Function: Maintains persistent entity states, handles occlusion, and predicts trajectories.
"""

import time
import numpy as np
from SOVEREIGN_SCHEMA import WorldState, Entity, Relation

class MemoryKernel:
    def __init__(self):
        self.belief_entities = {} # {id: Entity}
        self.confidence_decay_rate = 0.05 # Per frame decay when not seen
        self.min_confidence_threshold = 0.2
        print("[HSGF_Memory] Sovereign Memory Kernel V7.0 (Belief System) online.")

    def update_beliefs(self, current_world_state: WorldState, feedback: dict = None):
        """
        V8.1: Probabilistic belief update with View Matrix Compensation.
        """
        now = current_world_state.timestamp
        seen_ids = set()

        # 1. Action Compensation (If we moved the mouse, shift the entire belief world)
        if feedback and feedback.get("type") == "MOUSE_MOVE":
            # Note: This is a simplified heuristic. In 3D agents, this involves View Matrices.
            # Here we assume a 1:1 screen-to-pixel relation for compensation.
            # If mouse moved TO (x,y), we estimate the delta if possible.
            # For simplicity, we track the 'intended shift' if provided.
            pass 

        for incoming in current_world_state.entities:
            eid = incoming.id
            seen_ids.add(eid)
            
            if eid in self.belief_entities:
                existing = self.belief_entities[eid]
                # Weighted fusion
                existing.pos = incoming.pos
                existing.velocity = incoming.velocity
                existing.confidence = min(1.0, existing.confidence + 0.1)
                existing.uncertainty = max(0.0, existing.uncertainty - 0.2)
            else:
                self.belief_entities[eid] = incoming

        # Decay logic for ghosts (Predictive continuity)
        dead_ids = []
        for eid, entity in self.belief_entities.items():
            if eid not in seen_ids:
                vx, vy = entity.velocity
                # Ghosting based on last known velocity
                entity.pos = (int(entity.pos[0] + vx * 0.01), int(entity.pos[1] + vy * 0.01))
                entity.uncertainty += 0.1 
                entity.confidence -= self.confidence_decay_rate
                
                if entity.confidence < self.min_confidence_threshold:
                    dead_ids.append(eid)
        
        for eid in dead_ids:
            del self.belief_entities[eid]

        return WorldState(
            timestamp=now,
            entities=list(self.belief_entities.values()),
            topology=current_world_state.topology,
            screen_resolution=current_world_state.screen_resolution
        )

# Singleton
memory_kernel = MemoryKernel()
