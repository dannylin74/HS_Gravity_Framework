"""
HSGF - SOVEREIGN_SEMANTIC_GATEWAY.py
Version: V9.2 - Advanced Textual Interface
Function: Generates high-fidelity textual answers and strategic summaries.
"""

from SOVEREIGN_SCHEMA import WorldState
from SOVEREIGN_GOAL_SYSTEM import GoalType

class SemanticGateway:
    def __init__(self):
        print("[HSGF_Gateway] Sovereign Textual Interface V9.2 Online.")

    def get_tactical_answer(self, world: WorldState, primary_goal_type: GoalType) -> str:
        """
        Generates a human-readable text answer about the current state.
        """
        if not world.entities:
            return "Status: Scanning AO. No significant entities found."

        # Analyze situation
        has_danger = any(e.type == "DANGER" for e in world.entities)
        target = world.entities[0] if world.entities else None
        
        # Build conversational response
        msg = f"Report: Operating under [{primary_goal_type.name}] protocol. "
        
        if target:
            msg += f"Currently focusing on Entity[{target.id}] ({target.type}) at {target.pos}. "
        
        if has_danger:
            msg += "Alert: Hostile patterns detected. Evasive logic active."
        else:
            msg += "Note: Clear trajectory maintained. No immediate threats."

        return msg

    def summarize(self, world: WorldState, primary_goal_type: GoalType) -> str:
        """Standard summary for LLM ingestion."""
        # (Existing summary logic can stay or be unified here)
        return self.get_tactical_answer(world, primary_goal_type)

# Singleton
semantic_gateway = SemanticGateway()
