import asyncio
import os
import sys

VOICE_MALE_URDU = "ur-PK-AsadNeural"
VOICE_MALE_ENGLISH = "en-US-GuyNeural"

async def _try_edge(text, output_file):
    import edge_tts
    communicate = edge_tts.Communicate(text, VOICE_MALE_URDU, rate="-5%", pitch="+2Hz")
    await communicate.save(output_file)

def generate_voice(script_text, output_file="output/voice.mp3"):
    os.makedirs("output", exist_ok=True)
    if not output_file.startswith("output/"):
        output_file = "output/voice.mp3"

    # 1. Pehle Edge-TTS try karo (Best quality)
    try:
        print("Trying Edge-TTS AsadNeural...", flush=True)
        try:
            asyncio.run(_try_edge(script_text, output_file))
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_try_edge(script_text, output_file))
        
        # Check file bana ya nahi
        if os.path.exists(output_file) and os.path.getsize(output_file) > 1000:
            print(f"Edge Voice Success: {output_file}", flush=True)
            return output_file
        else:
            raise Exception("Edge file empty")
            
    except Exception as e:
        print(f"Edge-TTS Blocked on GitHub (403 Error): {e}", flush=True)
        print("Auto Fallback to gTTS Urdu...", flush=True)

        # 2. Fallback - gTTS (GitHub pe kabhi block nahi hota)
        try:
            from gtts import gTTS
            tts = gTTS(text=script_text, lang='ur', slow=False)
            tts.save(output_file)
            print(f"gTTS Urdu Voice Success: {output_file}", flush=True)
            return output_file
        except Exception as e2:
            print(f"gTTS ur fail, trying en: {e2}", flush=True)
            from gtts import gTTS
            tts = gTTS(text=script_text, lang='en', slow=False)
            tts.save(output_file)
            return output_file

if __name__ == "__main__":
    generate_voice("Pakistan ki team ne shandar karkardagi dikhayi hai")
