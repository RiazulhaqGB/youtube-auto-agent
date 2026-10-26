import asyncio, os
import edge_tts

# یہی وہ آواز ہے جو آپ نے بھیجی ہے - گہری اور بھاری
VOICE = "ur-PK-AsadNeural" 

async def _make_deep_voice(text, output_path):
    # rate -10% سے آواز گہری اور ٹک ٹاک جیسی ہو جاتی ہے
    # pitch -10Hz سے مزید بھاری
    communicate = edge_tts.Communicate(
        text, 
        VOICE, 
        rate="-8%", 
        pitch="-5Hz"
    )
    await communicate.save(output_path)

def generate_voiceover(text, output_path="output/voice.mp3"):
    os.makedirs("output", exist_ok=True)
    text = text.strip()
    if len(text) > 3500:
        text = text[:3500]
    
    print("TikTok wali gehri awaz bana raha hun...", flush=True)
    asyncio.run(_make_deep_voice(text, output_path))
    return output_path
