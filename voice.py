import asyncio
import edge_tts
import os

async def generate_voice_async(text, output_path="voice.mp3"):
    # BEST Urdu voices
    voice = "ur-PK-UzmaNeural"  # ladki ki saaf Urdu awaaz
    # voice = "ur-PK-AsadNeural" # agar larke ki chahiye to ye lagao

    # text saaf karo
    text = text.strip()
    if len(text) < 5:
        text = "Assalam o Alaikum, aaj ki kahani shuru karte hain."
    
    print(f"Generating voice: {text[:50]}...", flush=True)
    
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    print(f"Voice saved: {output_path}", flush=True)
    return output_path

def generate_voice(text, output_path="voice.mp3"):
    try:
        # purani file delete
        if os.path.exists(output_path):
            os.remove(output_path)
    except:
        pass
    
    asyncio.run(generate_voice_async(text, output_path))
    
    if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
        print("Voice OK!", flush=True)
        return output_path
    else:
        raise Exception("Voice file not created!")

if __name__ == "__main__":
    generate_voice("Ye test hai, ab awaaz bilkul saaf aayegi!")
