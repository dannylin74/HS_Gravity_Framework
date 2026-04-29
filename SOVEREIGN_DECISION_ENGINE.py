"""
HSGF - SOVEREIGN_DECISION_ENGINE.py
Version: V9.2 - Config-Aware Sovereign Agent
Function: Proactive intent-driven agent with dynamic performance tuning via YAML.
"""

import time
from SOVEREIGN_VISION_STACK import vision_stack
from SOVEREIGN_MEMORY_KERNEL import memory_kernel
from SOVEREIGN_PREDICTIVE_SIMULATOR import simulator
print("[DEBUG] Core Perception modules loaded.")

from SOVEREIGN_ACTUATOR import actuator
print("[DEBUG] Actuator online.")

from SOVEREIGN_GOAL_SYSTEM import goal_system, GoalType
from SOVEREIGN_ATTENTION_KERNEL import attention_kernel
from SOVEREIGN_SEMANTIC_GATEWAY import semantic_gateway
print("[DEBUG] Cognitive & Semantic modules loaded.")

from SOVEREIGN_CONFIG_LOADER import config
from SOVEREIGN_SCHEMA import WorldState, AgentAction, SimulationRollout

def v9_strategic_policy(world: WorldState, rollout: SimulationRollout, active_goal) -> list:
    """
    V9.0 Intent-Driven Policy:
    Selects actions that fulfill the active GOAL using focused perception.
    """
    actions = []
    entities = world.entities
    
    if not entities:
        return actions

    # 1. Goal-Based Target Selection
    if active_goal.type == GoalType.SURVIVAL:
        target = min(entities, key=lambda e: ((e.pos[0] - world.screen_resolution[0]/2)**2 + (e.pos[1] - world.screen_resolution[1]/2)**2)**0.5)
    else:
        target = max(entities, key=lambda e: (e.confidence * 100) + (e.age * 0.1))

    # 2. Predictive Execution (Look-ahead based on rollout)
    if rollout.steps:
        lookahead_idx = min(8, len(rollout.steps)-1)
        future_target = rollout.steps[lookahead_idx].get_entity_by_id(target.id)
        if future_target:
            actions.append(AgentAction("MOUSE_MOVE", {"x": int(future_target.pos[0]), "y": int(future_target.pos[1])}))

    # 3. Defensive Response
    if active_goal.type == GoalType.SURVIVAL:
        actions.append(AgentAction("KEY_PRESS", {"key": "space"}, priority=50))

    return actions

class DecisionEngine:
    def __init__(self):
        self.active = False
        self.last_action_time = 0
        self.last_summary_time = 0
        self.action_cooldown = 0.5 
        self.last_feedback = None
        print("[HSGF_Decision] Sovereign Decision Engine V9.2 (Dynamic Config) online.")

    def run_loop(self):
        print("[HSGF_Decision] V9.2 Sovereign Loop started.")
        self.active = True
        
        try:
            while self.active:
                now = time.time()
                # 1. OBSERVE (Limit from config)
                ent_cap = config.get("entity_cap")
                raw_world = vision_stack.find_elements(limit=ent_cap)
                
                if raw_world is None or not raw_world.entities:
                    if now - self.last_summary_time > 3.0:
                        print(f"[{time.strftime('%H:%M:%S')}] [Heartbeat] Eyes open. Scanning for targets...")
                        self.last_summary_time = now
                    time.sleep(0.05)
                    continue

                belief_world = memory_kernel.update_beliefs(raw_world, feedback=self.last_feedback)
                
                # 2. EVALUATE GOALS
                primary_goal = goal_system.get_primary_goal()
                
                # 3. APPLY ATTENTION
                focused_world = attention_kernel.focus(belief_world, primary_goal.type)
                
                # 4. SEMANTIC REPORTING (Frequency from config)
                summary_interval = config.get("summary_interval_seconds")
                if now - self.last_summary_time > summary_interval:
                    summary = semantic_gateway.summarize(focused_world, primary_goal.type)
                    print(f"\n--- [TACTICAL REPORT] ---\n{summary}\n-------------------------")
                    
                    # Persistent Status for Telegram Bot
                    status_data = {
                        "timestamp": now,
                        "summary": summary,
                        "entities_count": len(focused_world.entities),
                        "primary_goal": primary_goal.type.name
                    }
                    try:
                        import json
                        with open("hiro_status.json", "w", encoding="utf-8") as f:
                            json.dump(status_data, f, ensure_ascii=False, indent=2)
                    except:
                        pass

                    self.last_summary_time = now

                # 5. SIMULATE (Steps from config)
                sim_steps = config.get("simulation_steps")
                rollout = simulator.rollout(focused_world, steps=sim_steps)
                
                # 6. DECIDE & ACT
                actions = v9_strategic_policy(focused_world, rollout, primary_goal)
                
                for action in sorted(actions, key=lambda x: x.priority, reverse=True):
                    if action.type == "KEY_PRESS":
                        if now - self.last_action_time < self.action_cooldown:
                            continue
                        self.last_action_time = now
                    
                    self.last_feedback = actuator.execute(action)

                # Dynamic sleep based on HZ
                hz = config.get("decision_hz")
                time.sleep(1.0 / hz) 

        except KeyboardInterrupt:
            self.active = False
            print("[HSGF_Decision] Loop terminated.")

# Singleton
decision_engine = DecisionEngine()

if __name__ == "__main__":
    decision_engine.run_loop()
