import os
from openai import OpenAI

def polish_script(raw_script):
    """Uses OpenAI GPT-4 to enhance and polish the raw script"""
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional documentary scriptwriter. Transform the user's input into an engaging, well-structured documentary script. Keep it concise (2-3 minutes when read aloud). Use vivid descriptions and storytelling techniques."
                },
                {
                    "role": "user",
                    "content": f"Transform this into a professional documentary script:\n\n{raw_script}"
                }
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        polished = response.choices[0].message.content.strip()
        print(f"✅ Script polished: {len(polished)} characters")
        return polished
        
    except Exception as e:
        print(f"❌ Error polishing script: {str(e)}")
        raise Exception(f"Script polishing failed: {str(e)}")
