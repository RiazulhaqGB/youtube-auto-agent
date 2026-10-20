import asyncio
import edge_tts
import os

async def generate_voice_async(text, output_path="voice.mp3"):
    # Aapke liye BEST: Asad - gehra mardana Urdu
    voice = "ur-PK-AsadNeural"
    rate = "-10%"  # slow taake kahani jaisa lage
    pitch = "-2Hz"

    text = text.strip()
    if len(text) < 10:
        text = "Assalam o Alaikum dosto, aaj ki kahani aapki soch badal degi."

    print(f"Generating DEEP voice: {text[:80]}...", flush=True)
    
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_path)
    return output_path

def generate_voice(text, output_path="voice.mp3"):
    if os.path.exists(output_path):
        try: os.remove(output_path)
        except: pass
    
    asyncio.run(generate_voice_async(text, output_path))
    return output_path
