import mmap
import struct
import sys

def diagnose():
    print("[DIAG] Attempting to connect to HSGF_MirrorWorld_Buffer...")
    try:
        # Try to map only the header first (32 bytes)
        mmf = mmap.mmap(-1, 32, tagname="HSGF_MirrorWorld_Buffer", access=mmap.ACCESS_READ)
        print("[DIAG] Connection SUCCESS. Reading header...")
        
        header_data = mmf.read(32)
        print(f"[DIAG] Raw Header Hex: {header_data.hex()}")
        
        # Unpack: <IIIqi (W, H, Buf, Idx, Ready)
        data = struct.unpack("<IIIqi", header_data[:24])
        print(f"[DIAG] Parsed: Width={data[0]}, Height={data[1]}, ActiveBuf={data[2]}, FrameIdx={data[3]}, Ready={data[4]}")
        
        mmf.close()
    except Exception as e:
        print(f"[DIAG] Connection FAILED: {e}")
        print("[DIAG] Is the C# SovereignPerception.exe running?")

if __name__ == "__main__":
    diagnose()
