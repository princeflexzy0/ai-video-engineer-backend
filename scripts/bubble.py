import os
import requests
from datetime import datetime

def save_to_bubble(video_data):
    """Saves video metadata to Bubble.io database"""
    try:
        api_key = os.getenv('BUBBLE_API_KEY')
        app_url = os.getenv('BUBBLE_APP_URL')
        
        url = f"{app_url}/api/1.1/obj/video"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "video_id": video_data.get('id'),
            "user_id": video_data.get('userId'),
            "script": video_data.get('script'),
            "video_url": video_data.get('videoUrl'),
            "template": video_data.get('template'),
            "status": "completed",
            "created_date": datetime.utcnow().isoformat(),
            "duration": video_data.get('duration', 0)
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        print(f"✅ Saved to Bubble.io: {video_data.get('id')}")
        return response.json()
        
    except Exception as e:
        print(f"❌ Error saving to Bubble: {str(e)}")
        raise Exception(f"Bubble.io save failed: {str(e)}")
