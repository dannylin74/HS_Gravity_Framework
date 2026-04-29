"""
HSGF - SOVEREIGN_SYMBOL_INTERPRETER.py
Version: V4.1 - Adaptive Semantic Layer
Function: Translates raw geometric data (dict or float) into readable symbols.
"""

class SymbolInterpreter:
    def __init__(self):
        print("[Interpreter] V4.1 Adaptive Semantic Layer Initialized.")

    def interpret(self, geo):
        symbols = []
        primary = "UNKNOWN"
        confidence = 0.0
        
        # Adaptive input handling
        if isinstance(geo, (int, float)):
            circ = geo
            ar = 1.0
            solidity = 0.0
            area = 0
        else:
            circ = geo.get("circularity", 0)
            ar = geo.get("aspect_ratio", 1)
            solidity = geo.get("solidity", 0)
            area = geo.get("area", 0)

        # 1. Primary Classification
        if circ > 0.75:
            primary = "CIRCLE"
            confidence = circ
        elif ar > 3.0:
            primary = "LINE"
            confidence = min(ar / 5.0, 1.0)
        elif solidity > 0.9 and ar < 1.5:
            primary = "BLOCK"
            confidence = solidity
        
        # 2. Secondary Attributes
        if area > 10000:
            symbols.append("LARGE")
        elif area > 0 and area < 1500:
            symbols.append("SMALL")

        return {
            "primary": primary,
            "confidence": round(confidence, 2),
            "attributes": symbols
        }

# Singleton
interpreter = SymbolInterpreter()
