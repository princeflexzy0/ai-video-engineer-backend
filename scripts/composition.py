import subprocess
import os

def compose_video(presenter_video_path, audio_path, output_path="final_video.mp4"):
    """Uses FFmpeg to overlay audio on presenter video"""
    try:
        command = [
            'ffmpeg',
            '-i', presenter_video_path,
            '-i', audio_path,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-map', '0:v:0',
            '-map', '1:a:0',
            '-shortest',
            '-y',
            output_path
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"FFmpeg error: {result.stderr}")
        
        print(f"✅ Video composed: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ Error composing video: {str(e)}")
        raise Exception(f"Video composition failed: {str(e)}")
