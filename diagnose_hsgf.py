import cv2
import mss
import numpy as np
import sys

print("[DIAG] Step 1: Testing MSS Initialization...")
try:
    with mss.mss() as sct:
        print(f"[DIAG] Monitors found: {len(sct.monitors)}")
        for i, mon in enumerate(sct.monitors):
            print(f"  - Monitor {i}: {mon}")
        
        print("[DIAG] Step 2: Testing Screenshot Capture...")
        img = sct.grab(sct.monitors[0]) # 抓取全螢幕 (0 是所有螢幕合集)
        print(f"[DIAG] Capture success. Size: {img.size}")

except Exception as e:
    print(f"[ERROR] MSS Failed: {e}")
    sys.exit(1)

print("[DIAG] Step 3: Testing OpenCV Window...")
try:
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)
    cv2.namedWindow("DIAG_WINDOW", cv2.WINDOW_NORMAL)
    cv2.imshow("DIAG_WINDOW", frame)
    print("[DIAG] Window should be visible now. Press any key to exit.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("[DIAG] OpenCV Test Success.")
except Exception as e:
    print(f"[ERROR] OpenCV Failed: {e}")
