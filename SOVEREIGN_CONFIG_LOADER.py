"""
HSGF - SOVEREIGN_CONFIG_LOADER.py
Version: V1.0 - Adaptive Configuration
Function: Loads system parameters from config.yaml with fail-safe defaults.
"""

import yaml
import os

# Default fallback values
DEFAULT_CONFIG = {
    "vision_resolution": [640, 360],
    "entity_cap": 5,
    "decision_hz": 20,
    "simulation_steps": 10,
    "summary_interval_seconds": 3
}

class ConfigLoader:
    def __init__(self, config_path="config.yaml"):
        self.config = DEFAULT_CONFIG
        
        # Priority: Check local PROJECTS dir first, then AppData path
        local_path = os.path.join(os.path.dirname(__file__), config_path)
        appdata_path = r"C:\Users\09581\.gemini\antigravity\brain\50959907-e65b-40ef-b1f9-b3cebc823e42\config.yaml"
        
        target_path = local_path if os.path.exists(local_path) else appdata_path
        
        if os.path.exists(target_path):
            try:
                with open(target_path, 'r') as f:
                    user_config = yaml.safe_load(f)
                    if user_config:
                        self.config.update(user_config)
                        print(f"[Config] Successfully loaded configuration from: {target_path}")
            except Exception as e:
                print(f"[Config] Error loading YAML, using defaults: {e}")
        else:
            print(f"[Config] No config.yaml found at {target_path}. Using hardcoded defaults.")

    def get(self, key):
        return self.config.get(key, DEFAULT_CONFIG.get(key))

# Singleton
config = ConfigLoader()
