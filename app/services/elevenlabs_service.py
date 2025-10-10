"""ElevenLabs service for voice synthesis"""
import os
import logging

logger = logging.getLogger(__name__)

class ElevenLabsService:
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        self.mock_mode = os.getenv('MOCK_MODE', 'True') == 'True'
        self.voice_id = os.getenv('ELEVENLABS_VOICE_ID', 'default')
    
    def generate_voiceover(self, text, voice_id=None):
        """Generate voiceover from text"""
        if self.mock_mode:
            logger.info("MOCK: Generating voiceover")
            return "mock_audio.mp3"
        
        try:
            from elevenlabs import generate, save
            audio = generate(text=text, voice=voice_id or self.voice_id, api_key=self.api_key)
            filename = f"voiceover_{os.urandom(8).hex()}.mp3"
            save(audio, filename)
            return filename
        except Exception as e:
            logger.error(f"ElevenLabs error: {e}")
            return None
