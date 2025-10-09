"""Configuration settings for AI Video Engineer"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 10000))
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
    HEYGEN_API_KEY = os.getenv('HEYGEN_API_KEY')
    
    # Storage
    WASABI_ACCESS_KEY = os.getenv('WASABI_ACCESS_KEY')
    WASABI_SECRET_KEY = os.getenv('WASABI_SECRET_KEY')
    WASABI_BUCKET_NAME = os.getenv('WASABI_BUCKET_NAME')
    WASABI_REGION = os.getenv('WASABI_REGION', 'us-east-1')
    
    # Database
    BUBBLE_API_KEY = os.getenv('BUBBLE_API_KEY')
    BUBBLE_APP_URL = os.getenv('BUBBLE_APP_URL')
    
    # Mock mode for testing
    MOCK_MODE = os.getenv('MOCK_MODE', 'True') == 'True'
