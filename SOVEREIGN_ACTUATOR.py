"""
HSGF - SOVEREIGN_ACTUATOR.py
Version: V6.0 - Actuation Layer Abstraction
Function: Provides a clean interface for motor actions, decoupling Decision from SignalGateway.
"""

from SOVEREIGN_SIGNAL_GATEWAY import signal_gateway
from SOVEREIGN_SCHEMA import AgentAction

class SovereignActuator:
    def __init__(self):
        print("[HSGF_Actuator] Actuator Interface V6.0 online.")

    def execute(self, action: AgentAction) -> dict:
        """
        V8.1: Returns action summary for feedback loops.
        """
        atype = action.type
        p = action.params
        
        if atype == "MOUSE_MOVE":
            signal_gateway.mouse_move(int(p['x']), int(p['y']))
            return {"type": atype, "delta": (p['x'], p['y'])} # Simplified delta
        
        elif atype == "KEY_PRESS":
            signal_gateway.key_press(p['key'])
            return {"type": atype, "key": p['key']}
            
        elif atype == "CLICK":
            signal_gateway.mouse_click(p.get('button', 'left'))
            return {"type": atype, "button": p.get('button', 'left')}
        
        return {}

    def move_to(self, x: int, y: int) -> dict:
        return self.execute(AgentAction("MOUSE_MOVE", {"x": x, "y": y}))

    def trigger(self, key: str) -> dict:
        return self.execute(AgentAction("KEY_PRESS", {"key": key}))

# Singleton
actuator = SovereignActuator()
