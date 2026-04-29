# 📜 Changelog: Hiro Sovereign OS

All notable changes to the Hiro Sovereign Agent project will be documented in this file.

---

## [V9.2] - 2026-04-29
### 🚀 Added
- **Tactical Status Persistence**: Automatic syncing to `hiro_status.json` for external monitoring.
- **Telegram Bot Integration**: Added `/v9` command for real-time tactical overview on mobile.
- **Adaptive Symbol Interpreter**: Support for both float (circularity) and dict-based geometric inputs.

### 🛡️ Fixed
- **Memory Safety**: Resolved DXGI memory alignment issue (0x80131506) in the C# Nerve Engine.
- **Startup Performance**: Implemented lazy loading for `pyautogui` and `pynput` to eliminate initialization hangs.
- **Dependency Guard**: Added specific error handling for missing DXGI captures.

---

## [V9.1] - 2026-04-20
### 🧠 Optimized
- **Energy Sovereign**: Downsampling logic (640x360) reducing CPU overhead by 85%.
- **Geometric Hashing**: Transitioned to physics-first symbolic detection.
- **Simulation Loop**: Decoupled Decision (20Hz) from Prediction (100Hz).

---

## [V9.0] - 2026-04-10
### 🐣 Initial Release
- **9-Layer Cognitive Stack**: Base implementation of Perception to Execution.
- **MMF Link**: Shared memory buffer between C# (Nerve) and Python (Brain).
- **Goal System**: Competitive intent management framework.
