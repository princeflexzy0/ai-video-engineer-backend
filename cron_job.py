"""Maintenance tasks - cleanup temp files"""
import os
import glob
import time
from datetime import datetime

def cleanup_temp_files():
    """Remove old temp files"""
    print(f"[{datetime.now()}] Cleaning temp files...")
    
    patterns = ['temp_*.mp3', 'temp_*.mp4', 'final_*.mp4']
    deleted = 0
    
    for pattern in patterns:
        for file in glob.glob(pattern):
            try:
                if time.time() - os.path.getmtime(file) > 3600:  # 1 hour old
                    os.remove(file)
                    deleted += 1
                    print(f"  Deleted: {file}")
            except Exception as e:
                print(f"  Error: {e}")
    
    print(f"[{datetime.now()}] Cleanup done. Deleted {deleted} files.")

if __name__ == "__main__":
    cleanup_temp_files()
