import asyncio
import edge_tts
import os
import re

async def generate_voice_async(text, output_path="voice.mp3"):
    voice = "hi-IN-MadhurNeural"
    rate = "-8%"
    pitch = "+0Hz"

    text = text.strip()

    # ACCENT FIX - Ye lafz Roman Urdu se Hindi/Urdu accent me badlo
    accent_map = {
        "bohat": "bahut",
        "bohot": "bahut",
        "zindagi": "jindagi",
        "khuwab": "khwaab",
        "khawab": "khwaab",
        "paise": "paisa",
        "aisi": "aesi",
        "waisi": "vaesi",
        "zyada": "jyada",
        "khushi": "khushi",
        "kamyabi": "kamyabi",
        "dost": "dost",
        "meh": "main",
        "hu": "hun"
    }
    
    lower_text = text.lower()
    for wrong, correct in accent_map.items():
        lower_text = re.sub(r'\b' + wrong + r'\b', correct, lower_text)
    
    text = lower_text

    # Extra spaces aur pause saaf
    text = re.sub(r'\s+', ' ', text)
    text = text.replace(" ,", ",").replace(" .", ".")

    if len(text) < 10:
        text = "Assalam o Alaikum dosto, aaj ki kahani bahut khaas hai."

    print(f"Accent Fixed Voice: {text[:80]}...", flush=True)
    
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_path)
    return output_path

def generate_voice(text, output_path="voice.mp3"):
    if os.path.exists(output_path):
        try: os.remove(output_path)
        except: pass
    asyncio.run(generate_voice_async(text, output_path))
    return output_path
