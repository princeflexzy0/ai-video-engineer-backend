import os
from elevenlabs import ElevenLabs, VoiceSettings

def generate_voiceover(script, output_path="temp_audio.mp3"):
    """Generates voiceover audio using ElevenLabs TTS"""
    try:
        client = ElevenLabs(api_key=os.getenv('ELEVENLABS_API_KEY'))
        
        audio = client.generate(
            text=script,
            voice="Rachel",
            model="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=0.5,
                similarity_boost=0.75,
                style=0.0,
                use_speaker_boost=True
            )
        )
        
        with open(output_path, 'wb') as f:
            for chunk in audio:
                f.write(chunk)
        
        print(f"✅ Voiceover generated: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ Error generating voiceover: {str(e)}")
        raise Exception(f"Voiceover generation failed: {str(e)}")
