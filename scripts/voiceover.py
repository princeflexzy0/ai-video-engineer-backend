from elevenlabs.client import ElevenLabs
import os

client = ElevenLabs(api_key=os.getenv('ELEVENLABS_API_KEY'))

def generate_voiceover(script, output_path='temp_narration.mp3'):
    audio = client.generate(
        text=script,
        voice="Adam",  # Warm male; pick from docs
        model="eleven_monolingual_v1"
    )
    with open(output_path, "wb") as f:
        f.write(audio)
    return output_path