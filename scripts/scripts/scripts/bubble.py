import requests

def bubble_log(video_url, user_id, video_id):
    api_url = "https://your-bubble-app.bubbleapps.io/api/1.1/obj/video"
    headers = {"Authorization": f"Bearer {os.getenv('BUBBLE_API_KEY')}"}
    payload = {"url": video_url, "user": user_id, "title": video_id, "created_by": user_id}
    requests.post(api_url, json=payload, headers=headers)