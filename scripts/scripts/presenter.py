import requests
import os
import time

def generate_presenter(script, template_id='default', output_path='temp_presenter.mp4'):
    url = "https://api.heygen.com/v1/video/generate"
    headers = {"Authorization": f"Bearer {os.getenv('HEYGEN_API_KEY')}", "Content-Type": "application/json"}
    payload = {
        "script": script,
        "avatar_id": template_id,  # From HeyGen dashboard
        "background": "none"  # Transparent for overlay
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        video_id = response.json()['video_id']
        # Poll for ready (HeyGen async)
        while True:
            status_resp = requests.get(f"https://api.heygen.com/v1/video/{video_id}", headers=headers)
            if status_resp.json()['status'] == 'done':
                # Download
                dl_url = status_resp.json()['download_url']
                with open(output_path, 'wb') as f:
                    f.write(requests.get(dl_url).content)
                break
            time.sleep(10)
        return output_path
    raise Exception("HeyGen failed")