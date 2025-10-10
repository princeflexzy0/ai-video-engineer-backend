"""OpenAI service for script polishing"""
import os
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.mock_mode = os.getenv('MOCK_MODE', 'True') == 'True'
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')
    
    def polish_script(self, script):
        """Polish script using GPT-4"""
        if self.mock_mode:
            logger.info("MOCK: Polishing script")
            return f"[POLISHED] {script}"
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional video script writer. Polish the script for clarity and engagement."},
                    {"role": "user", "content": script}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return script
