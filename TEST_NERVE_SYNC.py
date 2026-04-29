import time
import cv2
from SOVEREIGN_VISION_STACK import vision_stack

def test_sync():
    print("[TEST] Starting Nerve-Sync Validation...")
    
    # Let it warm up
    time.sleep(1)
    
    start_time = time.time()
    frames = 0
    
    try:
        while frames < 100:
            # V4.7 logic: Capture -> Process (Contour analysis)
            result = vision_stack.find_elements(limit=5)
            
            objects = result["objects"]
            if frames % 20 == 0:
                print(f"[Frame {frames}] Objects Detected: {len(objects)}")
                for obj in objects:
                    print(f"  - ID: {obj['id']} | Type: {obj['symbol']['primary']} | Pos: {obj['pos']}")
            
            frames += 1
            
        end_time = time.time()
        fps = frames / (end_time - start_time)
        print(f"\n[SUCCESS] Nerve-Sync Benchmark: {fps:.2f} Full-Perception-Cycles/Sec")
        print("Note: This includes full contour analysis and semantic interpretation per frame.")
        
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    test_sync()
