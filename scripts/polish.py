from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def polish_script(raw_script):
    prompt = f"Polish this educational nature/travel script into conversational, voiceover-friendly narration (shorten to 300-500 words, engaging tone): {raw_script}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Cheap/fast
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content