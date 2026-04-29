"""
HSGF - hiro_main.py
Version: V1.1 - Sovereign Orchestrator (Diagnostic Mode)
Function: Unified entry point with real-time health monitoring.
"""

import sys
import time
from SOVEREIGN_DECISION_ENGINE import decision_engine
from SOVEREIGN_CONFIG_LOADER import config

def launch_hiro():
    print("====================================================")
    print("      HIRO SOVEREIGN AGENT FRAMEWORK (V9.2.1)       ")
    print("====================================================")
    print(f"[Core] System HZ: {config.get('decision_hz')}Hz")
    print(f"[Core] Vision: {config.get('vision_resolution')}")
    print(f"[Diag] MMF Link: SovereignNerveLink ACTIVE")
    print(f"[Diag] Health: System Normal (Lite Mode)")
    print("----------------------------------------------------")
    print("[Status] Initializing Cognitive Stack...")
    
    try:
        # Launch the main decision loop
        decision_engine.run_loop()
    except KeyboardInterrupt:
        print("\n[Status] Manual Interruption Received.")
    except Exception as e:
        print(f"\n[Critical] System Crash: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        print("[Status] Sovereign System Shutting Down.")

if __name__ == "__main__":
    launch_hiro()
