import os
import requests
import base64
from pydub import AudioSegment

def tiktok_api(text, voice="en_us_002"):
    apis = [
        ("https://tiktok-tts.weilnet.workers.dev/api/generation", {"text": text, "voice": voice}),
        ("https://tiktok-tts.weilnet.workers.dev/api/generation", {"text": text, "voice": "en_male_narration"}),
    ]
    for url, payload in apis:
        try:
            r = requests.post(url, json=payload, timeout=30)
            if r.status_code == 200 and 'data' in r.json():
                return base64.b64decode(r.json()['data'])
        except Exception as e:
            print(f"TikTok API fail: {e}", flush=True)
            continue
    return None

def generate_voice(script_text, output_file="output/voice.mp3"):
    os.makedirs("output", exist_ok=True)
    script_text = script_text.replace("...", ".").strip()
    
    chunks = [script_text[i:i+2000] for i in range(0, len(script_text), 2000)]
    print(f"Daily Voice: {len(chunks)} parts", flush=True)
    
    temp_files = []
    for i, chunk in enumerate(chunks):
        temp_path = f"output/temp_{i}.mp3"
        audio_bytes = tiktok_api(chunk, "en_us_002")
        
        if audio_bytes:
            with open(temp_path, "wb") as f:
                f.write(audio_bytes)
            print(f"Part {i+1} TikTok Done", flush=True)
        else:
            print(f"Part {i+1} gTTS backup", flush=True)
            from gtts import gTTS
            tts = gTTS(text=chunk, lang='ur', tld='com', slow=False)
            tts.save(temp_path)
        
        temp_files.append(temp_path)

    final = AudioSegment.empty()
    for f in temp_files:
        try:
            final += AudioSegment.from_file(f)
        except:
            pass
    
    final.export(output_file, format="mp3")
    
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)
    
    mins = len(final) / 1000 / 60
    print(f"FINAL VOICE READY: {mins:.2f} min", flush=True)
    return output_file
