import asyncio
import edge_tts
import os

async def generate_voice_async(text, output_path="voice.mp3"):
    # Madhur - Roman Urdu ke liye No.1, accent saaf
    voice = "hi-IN-MadhurNeural"
    rate = "-12%"  # halka slow, kahani jaisa
    pitch = "-1Hz"

    text = text.strip()
    # Roman Urdu ko Hindi style me saaf karo taake accent sahi aaye
    text = text.replace("kh", "kh").replace("gh", "gh")
    
    if len(text) < 10:
        text = "Assalam o Alaikum dosto, aaj ki kahani bahut khaas hai."

    print(f"Madhur Voice: {text[:80]}...", flush=True)
    
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_path)
    return output_path

def generate_voice(text, output_path="voice.mp3"):
    if os.path.exists(output_path):
        try: os.remove(output_path)
        except: pass
    asyncio.run(generate_voice_async(text, output_path))
    return output_path
