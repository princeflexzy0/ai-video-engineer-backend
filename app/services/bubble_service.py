"""Bubble.io API service"""
import requests
import logging
import os

logger = logging.getLogger(__name__)

class BubbleService:
    def __init__(self):
        self.mock_mode = os.getenv('MOCK_MODE', 'True') == 'True'
        self.api_key = os.getenv('BUBBLE_API_KEY')
        self.app_url = os.getenv('BUBBLE_APP_URL')
        self.headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
    
    def sync_metadata(self, video_data):
        """Sync video metadata to Bubble"""
        if self.mock_mode:
            logger.info(f"MOCK: Syncing metadata for {video_data.get('video_id')}")
            return {'success': True, 'mock': True}
        
        if not self.api_key or not self.app_url:
            logger.warning("Bubble API not configured")
            return {'success': False, 'error': 'Bubble API not configured'}
        
        try:
            endpoint = f"{self.app_url}/obj/video"
            payload = {
                'video_id': video_data.get('video_id'),
                'user_id': video_data.get('user_id'),
                'script': video_data.get('script'),
                'template': video_data.get('template'),
                'status': video_data.get('status'),
                'video_url': video_data.get('video_url'),
                'created_at': video_data.get('created_at')
            }
            response = requests.post(endpoint, json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            logger.info(f"Synced metadata for {video_data.get('video_id')}")
            return {'success': True, 'response': response.json()}
        except requests.exceptions.RequestException as e:
            logger.error(f"Bubble sync error: {e}")
            return {'success': False, 'error': str(e)}
