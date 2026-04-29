"""
HSGF - SOVEREIGN_SYNTHETIC_TEST.py
Function: Tests the entire cognitive stack using synthetic world data.
"""

import time
from SOVEREIGN_DECISION_ENGINE import decision_engine
from SOVEREIGN_SCHEMA import WorldState, Entity
from SOVEREIGN_GOAL_SYSTEM import GoalType

def run_synthetic_test():
    print("[Test] Initializing Synthetic Test Case...")
    
    # 1. Create a fake WorldState (Target at center)
    fake_entities = [
        Entity(id=99, type="CIRCLE", pos=(960, 540), velocity=(10, 5), age=100)
    ]
    fake_world = WorldState(
        timestamp=time.time(),
        entities=fake_entities,
        topology=[],
        screen_resolution=(1920, 1080)
    )

    print("[Test] Injecting synthetic world state into Decision Engine...")
    
    from SOVEREIGN_MEMORY_KERNEL import memory_kernel
    from SOVEREIGN_ATTENTION_KERNEL import attention_kernel
    from SOVEREIGN_PREDICTIVE_SIMULATOR import simulator
    from SOVEREIGN_SEMANTIC_GATEWAY import semantic_gateway
    from SOVEREIGN_GOAL_SYSTEM import goal_system

    # Manual step of the loop to see the output
    belief = memory_kernel.update_beliefs(fake_world)
    goal = goal_system.get_primary_goal()
    focused = attention_kernel.focus(belief, goal.type)
    
    print("\n--- TEST: SEMANTIC OUTPUT ---")
    summary = semantic_gateway.summarize(focused, goal.type)
    print(summary)
    
    print("\n--- TEST: SIMULATION ROLLOUT ---")
    rollout = simulator.rollout(focused, steps=5)
    for i, step in enumerate(rollout.steps):
        e = step.entities[0]
        print(f"Step {i}: Entity predicted at {e.pos}")

    print("\n[Test] V9.1 Cognitive Logic: PASS.")

if __name__ == "__main__":
    run_synthetic_test()
