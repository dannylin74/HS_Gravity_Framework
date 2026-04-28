# [HSGF] Hiro Sovereign Gravity Framework V1.0

> **"Giving Machines the Instinct to Survive."**
> **"賦予機器生存的直覺。"**

---

## Overview | 概覽

**HSGF** is a physics-based visual perception and navigation engine for autonomous agents.

Instead of relying on heavy Vision-Language Models (VLMs), HSGF uses **mathematical physics** — gravity fields, parabolic trajectory prediction, and Shannon entropy gating — to navigate and interact with digital environments.

> When pixels fail, Physics takes over.

---

## Quick Start | 快速開始

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the demo
python demo.py

# 3. Check 'demo_output.jpg' to see the Gravity Field visualization
```

---

## Core Modules | 核心模組

| Module | Role |
|--------|------|
| `SOVEREIGN_VISION_STACK.py` | Screen capture, Canny edge detection, entropy gating, real contour-based element detection |
| `SOVEREIGN_SEMANTIC_DEDUCTOR.py` | Parabolic trajectory prediction, apex locking, adaptive viscosity damping |
| `SOVEREIGN_INPUT_GATEWAY.py` | Physics-based stealth mouse movement with gravity-well spline paths |
| `demo.py` | Full integration demo — run this first |

---

## Key Features | 核心特性

### 1. Mathematical Gravity Fields (數理引力場)
Navigation is not a set of IF-ELSE rules. Objects are drawn toward targets as if pulled by gravity — using potential field gradients.

### 2. Parabolic Trajectory Prediction (拋物線軌跡預判)
The system detects angular velocity (ω) changes across frames to predict movement apex **before it happens** — enabling proactive correction.

### 3. Shannon Entropy Gating (環境熵值感知)
```python
# Automatically adapts to environmental chaos
entropy = vision_stack._calculate_entropy(frame)
# High entropy → noise filter activated
# Low entropy  → clean geometric extraction
```

### 4. Adaptive Viscosity Damping (自適應阻尼)
Near the target, the system increases virtual friction to prevent overshoot — like a spacecraft performing orbital insertion.

### 5. Real Geometric Detection (真實幾何偵測)
```python
# Find actual on-screen elements — not hardcoded coordinates
pos, confidence = vision_stack.find_element("CIRCLE")
pos, confidence = vision_stack.find_element("RECTANGLE")
pos, confidence = vision_stack.find_element("LARGEST")
```

---

## Architecture | 系統架構

```
Screen Capture
      |
 [Entropy Gate] ← Shannon Entropy > threshold?
      |                    YES → Apply noise filter
      |
 [Edge Geometry] ← Canny edge detection
      |
 [find_element] ← Contour analysis + Geometric Hash
      |
 [Deductor] ← Parabolic arc + Apex locking + Damping
      |
 [Input Gateway] ← Gravity-well spline mouse movement
```

---

## Philosophy | 設計哲學

Most AI agents fail when pixels become noisy.
**HSGF does not trust pixels. It trusts Physics.**

- **Ultra-Lightweight**: No GPU required. Runs on 50MB RAM.
- **Zero Latency**: Real-time deduction at 60FPS+.
- **Sovereign & Local**: No Cloud API. Total privacy.

---

## Requirements | 環境需求

- Python 3.8+
- See `requirements.txt`

---

*Created by dannylin74 — Built on Physics, Not Pixels.*
