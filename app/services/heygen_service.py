"""HeyGen service for avatar video generation"""
import os
import logging

logger = logging.getLogger(__name__)

class HeyGenService:
    def __init__(self):
        self.api_key = os.getenv('HEYGEN_API_KEY')
        self.mock_mode = os.getenv('MOCK_MODE', 'True') == 'True'
    
    def create_avatar_video(self, audio_url, avatar_id='default'):
        """Create avatar video from audio"""
        if self.mock_mode:
            logger.info("MOCK: Creating avatar video")
            return "mock_avatar_video.mp4"
        
        # TODO: Implement real HeyGen API call
        return None
