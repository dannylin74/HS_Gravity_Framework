"""
HSGF - SOVEREIGN_SCHEMA.py
Version: V6.0 - System Schemas
Function: Defines standardized data structures for the entire framework.
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any

@dataclass
class Entity:
    id: int
    type: str
    pos: Tuple[int, int]
    velocity: Tuple[float, float] = (0.0, 0.0)
    age: int = 0
    confidence: float = 1.0
    uncertainty: float = 0.0 # V8: New field for probabilistic tracking
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Relation:
    subject_id: int
    target_id: int
    type: str
    distance: float
    tags: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class WorldState:
    timestamp: float
    entities: List[Entity]
    topology: List[Relation]
    screen_resolution: Tuple[int, int]
    is_predicted: bool = False # V8: Distinguish between reality and simulation
    
    def get_entity_by_id(self, eid: int) -> Entity:
        for e in self.entities:
            if e.id == eid: return e
        return None

@dataclass
class SimulationRollout:
    """V8: Represents a sequence of future predicted states."""
    steps: List[WorldState]
    confidence: float

@dataclass
class AgentAction:
    type: str # 'MOUSE_MOVE', 'KEY_PRESS', 'CLICK'
    params: Dict[str, Any]
    priority: int = 0
