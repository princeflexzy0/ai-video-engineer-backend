"""Application configuration"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    MOCK_MODE = os.getenv('MOCK_MODE', 'True') == 'True'
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
    ELEVENLABS_VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID', 'default')
    HEYGEN_API_KEY = os.getenv('HEYGEN_API_KEY')
    HEYGEN_AVATAR_ID = os.getenv('HEYGEN_AVATAR_ID', 'default')
    WASABI_ACCESS_KEY = os.getenv('WASABI_ACCESS_KEY')
    WASABI_SECRET_KEY = os.getenv('WASABI_SECRET_KEY')
    WASABI_BUCKET_NAME = os.getenv('WASABI_BUCKET_NAME', 'ai-videos')
    WASABI_REGION = os.getenv('WASABI_REGION', 'us-east-1')
    WASABI_ENDPOINT = os.getenv('WASABI_ENDPOINT', 'https://s3.wasabisys.com')
    BUBBLE_API_KEY = os.getenv('BUBBLE_API_KEY')
    BUBBLE_APP_URL = os.getenv('BUBBLE_APP_URL')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
