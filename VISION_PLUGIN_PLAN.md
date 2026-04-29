# Vision Plugin Plan & Multi‑Spectral Extension

## 目標
將 **SOVEREIGN_VISION_STACK** 轉變為可直接 **pip 安裝** 的外掛套件，並在未來支援 **多光譜 (RGB / Depth / IR / NIR)** 感測。

---

## 1️⃣ 套件化步驟 (setup.cfg / pyproject.toml)
```ini
[metadata]
name = hsgf-vision
version = 1.0.0
author = dannylin74
description = Sovereign physics‑based vision engine (RGB + multi‑spectral)
long_description = file: README.md
long_description_content_type = text/markdown
license = MIT
classifiers =
    Programming Language :: Python :: 3
    License :: OSI Approved :: MIT License
    Operating System :: OS Independent

[options]
packages = find:
package_dir =
    =src
python_requires = >=3.8
install_requires =
    opencv-python>=4.8.0
    numpy>=1.24.0
    pyautogui>=0.9.53

[options.extras_require]
opencv =
    opencv-contrib-python; platform_system == "Windows"

[options.packages.find]
where = src
```
> **說明**：`src/` 目錄下放所有模組 (`hsgf_vision/`)，`setup.cfg` 會自動收集。

---

## 2️⃣ 目錄結構（建議）
```
HS_Gravity_Framework/
│   README.md
│   requirements.txt
│   setup.cfg
│   pyproject.toml
│   LICENSE
│   ...
└───src/
    └───hsgf_vision/
        │   __init__.py       # expose VisionEngine
        │   vision_engine.py  # 包裝 VisionStack
        │   vision_stack.py   # 原 SOVEREIGN_VISION_STACK (已改名)
        │   vision_multispectral.py  # 多光譜前處理
        │   color_presets.py  # HSV 顏色表 (可自行擴充)
        └───tests/
                test_vision.py
                test_multispectral.py
```
---

## 3️⃣ 重要類別說明
### 3.1 `VisionEngine` (src/hsgf_vision/vision_engine.py)
```python
from .vision_stack import VisionStack
from .vision_multispectral import MultiSpectralProcessor

class VisionEngine:
    """High‑level façade for the vision stack.

    Parameters
    ----------
    modality: str, optional
        One of "rgb", "depth", "ir", "nir". Default = "rgb".
    frame_provider: Callable[[], np.ndarray] | None, optional
        Function that returns a raw frame. If ``None`` the default is
        ``pyautogui.screenshot()`` (converted to BGR). Allows users to feed
        a video stream, a depth camera, etc.
    """

    def __init__(self, modality: str = "rgb", frame_provider=None):
        self.processor = MultiSpectralProcessor(modality)
        self.stack = VisionStack()
        self.frame_provider = frame_provider

    def _capture(self):
        # Get raw frame (BGR) from provider or default screenshot
        if self.frame_provider is None:
            import pyautogui, numpy as np, cv2
            scr = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(scr), cv2.COLOR_RGB2BGR)
        else:
            frame = self.frame_provider()
        return frame

    def capture_and_process(self, roi=None):
        raw = self._capture()
        proc = self.processor.process(raw)          # -> 8‑bit gray
        return self.stack.capture_and_process(proc, roi)

    # 直接映射 VisionStack 中的核心方法
    def find_element(self, *a, **kw):
        return self.stack.find_element(*a, **kw)

    def get_local_entropy(self, cx, cy, radius=50):
        return self.stack.get_local_entropy(cx, cy, radius)
```
---

### 3.2 `MultiSpectralProcessor` (src/hsgf_vision/vision_multispectral.py)
```python
import cv2, numpy as np

class MultiSpectralProcessor:
    """Normalize various sensor modalities to an 8‑bit gray image.

    Supported modalities:
        - "rgb"   : standard colour image (BGR).
        - "depth" : uint16/float32 depth in meters.
        - "ir"    : thermal camera (single channel).
        - "nir"   : near‑infrared (single channel).
    """

    def __init__(self, modality: str = "rgb"):
        self.modality = modality.lower()
        if self.modality not in {"rgb", "depth", "ir", "nir"}:
            raise ValueError(f"Unsupported modality: {modality}")

    def process(self, frame: np.ndarray) -> np.ndarray:
        """Return an 8‑bit gray image ready for Canny/entropy.
        ``frame`` is expected in BGR order when modality == "rgb".
        """
        if self.modality == "rgb":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        elif self.modality == "depth":
            # Depth may be uint16 or float32 (meters). Normalise to 0‑255.
            depth = frame.astype(np.float32)
            if depth.max() == 0:
                gray = np.zeros_like(depth, dtype=np.uint8)
            else:
                norm = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX)
                gray = norm.astype(np.uint8)
        elif self.modality in {"ir", "nir"}:
            # Assume single‑channel already. Apply CLAHE for contrast.
            if len(frame.shape) == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            gray = clahe.apply(frame)
        else:
            raise RuntimeError("Unreachable modality branch")
        return gray
```
---

## 4️⃣ 範例腳本 (example_multispectral_plugin.py)
```python
"""Demo: 使用 hsgf‑vision 套件的多光譜模式"""

import cv2
import numpy as np
from hsgf_vision.vision_engine import VisionEngine

# ------------------------------------------------------------
# 1️⃣ RGB (螢幕截圖) – 預設模式
# ------------------------------------------------------------
engine_rgb = VisionEngine(modality="rgb")
pos, conf, h = engine_rgb.find_element("YELLOW_LINE")
print("[RGB] Yellow line →", pos, conf, h)

# ------------------------------------------------------------
# 2️⃣ Depth 模擬 – 使用本地的深度圖檔案 (png) 作為來源
# ------------------------------------------------------------
def depth_provider():
    # 假設您有一張深度圖 depth.png（uint16）在工作目錄
    depth_raw = cv2.imread('depth.png', cv2.IMREAD_UNCHANGED)
    # OpenCV 讀取的深度圖是單通道，直接回傳即可
    return depth_raw

engine_depth = VisionEngine(modality="depth", frame_provider=depth_provider)
pos2, conf2, h2 = engine_depth.find_element("LARGEST")
print("[Depth] Largest object →", pos2, conf2, h2)

# ------------------------------------------------------------
# 3️⃣ IR (熱成像) – 使用假想的熱影像檔案 ir.png
# ------------------------------------------------------------

def ir_provider():
    ir = cv2.imread('ir.png', cv2.IMREAD_GRAYSCALE)
    return ir

engine_ir = VisionEngine(modality="ir", frame_provider=ir_provider)
pos3, conf3, h3 = engine_ir.find_element("LARGEST")
print("[IR] Detected →", pos3, conf3, h3)

# ------------------------------------------------------------
# 4️⃣ Local entropy 示範 (以螢幕中心為例)
# ------------------------------------------------------------
entropy = engine_rgb.get_local_entropy(960, 540, radius=80)
print("[RGB] Local entropy (center) =", entropy)
```
> 把 `depth.png`、`ir.png` 放在同一目錄下即可執行。若您只有螢幕截圖，仍可使用 `modality='rgb'`（預設）。
---

## 5️⃣ 測試範例 (src/hsgf_vision/tests/test_multispectral.py)
```python
import numpy as np, cv2
import pytest
from hsgf_vision.vision_multispectral import MultiSpectralProcessor

@pytest.mark.parametrize("modality", ["rgb", "depth", "ir", "nir"])
def test_process_returns_uint8(modality):
    proc = MultiSpectralProcessor(modality)
    # 建立偽造影像
    if modality == "rgb":
        img = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
    elif modality == "depth":
        img = np.random.randint(0, 5000, (480, 640), dtype=np.uint16)  # 0‑5m
    else:  # ir / nir
        img = np.random.randint(0, 256, (480, 640), dtype=np.uint8)
    out = proc.process(img)
    assert out.shape == (480, 640)
    assert out.dtype == np.uint8
```
---

## 6️⃣ 發布與安裝說明
```bash
# 1️⃣ 在專案根目錄建立 virtualenv (可選)
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2️⃣ 安裝套件（開發模式）
pip install -e .

# 3️⃣ 執行範例
python examples/example_multispectral_plugin.py
```
---

## 7️⃣ 下一步（可在 Issue 中追蹤）
1. **CI**：在 `.github/workflows/ci.yml` 中加入 `pytest` 三平台測試。<br>2. **CONTRIBUTING.md** & **CODE_OF_CONDUCT.md**。<br>3. **發佈到 PyPI**：`python -m build && twine upload dist/*`。

---

**結語**：完成此檔案後，您只需要把 `src/` 目錄搬到原本的 `HS_Gravity_Framework` 專案裡，跑 `pip install -e .` 即可得到一個 **即插即用的視覺外掛**，同時支援未來的 **多光譜感測**。祝開發順利！
