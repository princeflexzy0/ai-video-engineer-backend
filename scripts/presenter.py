import os
import requests
import time

def create_heygen_video(script, template_id="presenter1"):
    """Creates AI presenter video using HeyGen API"""
    try:
        api_key = os.getenv('HEYGEN_API_KEY')
        url = "https://api.heygen.com/v2/video/generate"
        
        headers = {
            "X-Api-Key": api_key,
            "Content-Type": "application/json"
        }
        
        avatars = {
            "presenter1": "avatar_id_1",
            "presenter2": "avatar_id_2",
            "presenter3": "avatar_id_3"
        }
        
        payload = {
            "video_inputs": [{
                "character": {
                    "type": "avatar",
                    "avatar_id": avatars.get(template_id, avatars["presenter1"]),
                    "avatar_style": "normal"
                },
                "voice": {
                    "type": "text",
                    "input_text": script,
                    "voice_id": "1bd001e7e50f421d891986aad5158bc8"
                },
                "background": {
                    "type": "color",
                    "value": "#FFFFFF"
                }
            }],
            "dimension": {
                "width": 1920,
                "height": 1080
            },
            "aspect_ratio": "16:9",
            "test": False
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        video_id = data.get('data', {}).get('video_id')
        
        if not video_id:
            raise Exception("No video ID returned from HeyGen")
        
        print(f"✅ HeyGen video initiated: {video_id}")
        
        status_url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
        
        for attempt in range(60):
            time.sleep(10)
            
            status_response = requests.get(status_url, headers=headers)
            status_data = status_response.json()
            
            status = status_data.get('data', {}).get('status')
            
            if status == 'completed':
                video_url = status_data.get('data', {}).get('video_url')
                print(f"✅ HeyGen video completed: {video_url}")
                return video_url
            elif status == 'failed':
                raise Exception("HeyGen video generation failed")
            
            print(f"⏳ HeyGen status: {status} (attempt {attempt + 1}/60)")
        
        raise Exception("HeyGen video generation timed out")
        
    except Exception as e:
        print(f"❌ Error creating HeyGen video: {str(e)}")
        raise Exception(f"HeyGen video creation failed: {str(e)}")
