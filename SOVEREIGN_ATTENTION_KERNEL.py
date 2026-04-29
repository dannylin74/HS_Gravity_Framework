"""
HSGF - SOVEREIGN_ATTENTION_KERNEL.py
Version: V9.0 - Attention Mechanism
Function: Filters WorldState to prioritize entities relevant to the active goal.
"""

from SOVEREIGN_SCHEMA import WorldState
from SOVEREIGN_GOAL_SYSTEM import GoalType

class AttentionKernel:
    def __init__(self):
        print("[HSGF_Attention] V9.0 Attention Mechanism online.")

    def focus(self, world: WorldState, primary_goal_type: GoalType) -> WorldState:
        """
        Dynamically filters and re-ranks entities based on the agent's goal.
        """
        focused_entities = []
        
        for entity in world.entities:
            # 1. Survival Focus: Prioritize Danger symbols
            if primary_goal_type == GoalType.SURVIVAL:
                if entity.type == "DANGER" or entity.confidence < 0.5:
                    focused_entities.append(entity)
            
            # 2. Hunting Focus: Prioritize stable targets
            elif primary_goal_type == GoalType.TARGET_HUNT:
                if entity.type != "UNKNOWN":
                    focused_entities.append(entity)
            
            # Default fallback: keep top entities
            else:
                focused_entities.append(entity)

        # Update world state with focused views
        world.entities = focused_entities
        return world

# Singleton
attention_kernel = AttentionKernel()
