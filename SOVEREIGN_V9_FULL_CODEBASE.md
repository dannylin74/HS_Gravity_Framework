# HSGF V9.2.1 CORE CODEBASE - FULL REAL-TIME AUDIT

---
## 1. SOVEREIGN_SCHEMA.py (V6.0)
```python
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
    uncertainty: float = 0.0
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
    is_predicted: bool = False
    
    def get_entity_by_id(self, eid: int) -> Entity:
        for e in self.entities:
            if e.id == eid: return e
        return None

@dataclass
class SimulationRollout:
    steps: List[WorldState]
    confidence: float

@dataclass
class AgentAction:
    type: str
    params: Dict[str, Any]
    priority: int = 0
```

---
## 2. SOVEREIGN_VISION_STACK.py (V9-Lite REAL)
```python
import cv2
import numpy as np
import mmap
import time
from SOVEREIGN_SCHEMA import WorldState, Entity, Relation

class VisionStack:
    def __init__(self, mmf_name="SovereignNerveLink", width=1920, height=1080):
        self.width, self.height = width, height
        self.frame_size = width * height * 4
        self.header_size = 128
        self.total_size = self.header_size + self.frame_size
        
        from SOVEREIGN_CONFIG_LOADER import config
        res = config.get("vision_resolution")
        self.target_res = (res[0], res[1]) 
        self.scale_x = width / self.target_res[0]
        self.scale_y = height / self.target_res[1]
        self.entity_cap = config.get("entity_cap")

        try:
            self.mmf = mmap.mmap(-1, self.total_size, mmf_name)
            print(f"[HSGF_Vision] V9-Lite Linked to Nerve: {mmf_name}")
        except Exception as e:
            print(f"[HSGF_Vision] Link Failed: {e}")
            self.mmf = None

    def read_frame(self):
        if not self.mmf: return None
        self.mmf.seek(self.header_size)
        data = self.mmf.read(self.frame_size)
        frame = np.frombuffer(data, dtype=np.uint8).reshape((self.height, self.width, 4))
        return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    def find_elements(self, limit=5):
        from SOVEREIGN_SYMBOL_INTERPRETER import interpreter
        from SOVEREIGN_RELATION_ENGINE import relation_engine
        from SOVEREIGN_OBJECT_TRACKER import object_tracker
        
        raw = self.read_frame()
        if raw is None: return None
        
        small = cv2.resize(raw, self.target_res)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        detections = []
        for c in contours:
            area = cv2.contourArea(c)
            if 100 < area < 20000:
                M = cv2.moments(c)
                if M["m00"] > 0:
                    detections.append({
                        "pos": (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"])),
                        "symbol": interpreter.interpret(self.geometric_hash(c))
                    })

        tracked = object_tracker.update(detections)
        tracked = sorted(tracked, key=lambda x: x["age"], reverse=True)[:limit]
        entities = [Entity(id=o["id"], type=o["symbol"]["primary"], 
                           pos=(int(o["pos"][0]*self.scale_x), int(o["pos"][1]*self.scale_y)),
                           velocity=(o.get("velocity",(0,0))[0]*self.scale_x, o.get("velocity",(0,0))[1]*self.scale_y),
                           age=o["age"]) for o in tracked]
        return WorldState(time.time(), entities, [], (1920, 1080))
```

---
## 3. SOVEREIGN_DECISION_ENGINE.py (V9.2.1 REAL)
```python
class DecisionEngine:
    def run_loop(self):
        self.active = True
        while self.active:
            now = time.time()
            ent_cap = config.get("entity_cap")
            raw_world = vision_stack.find_elements(limit=ent_cap)
            
            if raw_world is None or not raw_world.entities:
                if now - self.last_summary_time > 3.0:
                    print(f"[{time.strftime('%H:%M:%S')}] [Heartbeat] Eyes open. Scanning...")
                    self.last_summary_time = now
                time.sleep(0.05); continue

            belief_world = memory_kernel.update_beliefs(raw_world, feedback=self.last_feedback)
            primary_goal = goal_system.get_primary_goal()
            focused_world = attention_kernel.focus(belief_world, primary_goal.type)
            
            summary_interval = config.get("summary_interval_seconds")
            if now - self.last_summary_time > summary_interval:
                summary = semantic_gateway.summarize(focused_world, primary_goal.type)
                print(f"\n--- [TACTICAL REPORT] ---\n{summary}\n-------------------------")
                self.last_summary_time = now

            sim_steps = config.get("simulation_steps")
            rollout = simulator.rollout(focused_world, steps=sim_steps)
            actions = v9_strategic_policy(focused_world, rollout, primary_goal)
            
            for action in sorted(actions, key=lambda x: x.priority, reverse=True):
                self.last_feedback = actuator.execute(action)

            time.sleep(1.0 / config.get("decision_hz"))
```

---
## 4. hiro_main.py (V1.1 Diagnostic)
```python
import sys, time
from SOVEREIGN_DECISION_ENGINE import decision_engine
from SOVEREIGN_CONFIG_LOADER import config

def launch_hiro():
    print("====================================================")
    print("      HIRO SOVEREIGN AGENT FRAMEWORK (V9.2.1)       ")
    print("====================================================")
    print(f"[Core] System HZ: {config.get('decision_hz')}Hz")
    print(f"[Core] Vision: {config.get('vision_resolution')}")
    print(f"[Diag] MMF Link: SovereignNerveLink ACTIVE")
    print("----------------------------------------------------")
    decision_engine.run_loop()
```
