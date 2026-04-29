"""
HSGF - SOVEREIGN_GOAL_SYSTEM.py
Version: V9.0 - Goal Arbitration System
Function: Manages competing objectives and dynamic priorities for the agent.
"""

from dataclasses import dataclass
from enum import Enum

class GoalType(Enum):
    SURVIVAL = 100    # Highest priority
    TARGET_HUNT = 50  # Medium priority
    EXPLORATION = 10  # Low priority

@dataclass
class Goal:
    type: GoalType
    weight: float
    status: str = "PENDING"

class GoalSystem:
    def __init__(self):
        self.active_goals = [
            Goal(GoalType.SURVIVAL, 1.0),
            Goal(GoalType.TARGET_HUNT, 0.8)
        ]
        print("[HSGF_Goal] Sovereign Goal System V9.0 active.")

    def get_primary_goal(self) -> Goal:
        # Sort goals by Type Priority * Dynamic Weight
        return sorted(self.active_goals, key=lambda g: g.type.value * g.weight, reverse=True)[0]

# Singleton
goal_system = GoalSystem()
