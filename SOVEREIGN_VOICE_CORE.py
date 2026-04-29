"""
HSGF - SOVEREIGN_VOICE_CORE.py
Version: V1.0 - Vocal Chord Interface
Function: Provides localized text-to-speech feedback for the agent.
"""

import pyttsx3
import threading

class VoiceCore:
    def __init__(self):
        self.engine = pyttsx3.init()
        # Set property
        self.engine.setProperty('rate', 180)    # Speed
        self.engine.setProperty('volume', 0.9)  # Volume
        print("[Voice] Sovereign Voice Core V1.0 Online.")

    def _say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def speak(self, text):
        """Non-blocking speech."""
        threading.Thread(target=self._say, args=(text,), daemon=True).start()

# Singleton
voice_core = VoiceCore()

if __name__ == "__main__":
    voice_core.speak("Sovereign Agent System Online. Hiro is ready.")
    import time
    time.sleep(3)
