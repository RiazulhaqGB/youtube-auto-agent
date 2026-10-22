import os
import json
from google import genai
from google.genai import types

def generate_title_and_hashtags(script_path="final_script.txt", topic=""):
    """
    Script ke mutabiq viral title, description, hashtags - Pure Urdu Script
    """
    script_text = topic
    try:
        if os.path.exists(script_path):
            with open(script_path, 'r', encoding='utf-8') as f:
                script_text = f.read()[:3000]
        elif os.path.exists("script.txt"):
            with open("script.txt", 'r', encoding='utf-8') as f:
                script_text = f.read()[:3000]
        else:
            script_text = topic
        print(f"Title ke liye script/topic: {script_text[:100]}...", flush=True)
    except Exception as e:
        print(f"Script read error {e}", flush=True)
        script_text = topic

    if os.getenv("GEMINI_API_KEY"):
        try:
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            
            prompt = f"""
            You are World of Wisdom YouTube expert for Pakistan audience.
            Script/Topic: {script_text}

            Task: Create VIRAL YouTube Title + Description + Hashtags in PURE URDU SCRIPT (اردو رسم الخط) - NO Roman Urdu, NO English words.

            Rules:
            1. Title: 1 VIRAL title, 60 chars max, clickable, high CTR, script se 100% related ho. 
               - Har bar NAYA title banao, fix jumla "90% لوگ نہیں جانتے" ya "90% Log Nahi Jante" bilkul use mat karo.
               - Topic ke mutabiq creative title banao jaise: "بیوقوف مردوں کی 9 نشانیاں" ya "کامیاب زندگی کا راز"
            
            2. Description: 2 lines hook in pure Urdu + 3 bullet points + CTA (Like, Share, Subscribe ko Urdu me: پسند کریں، شیئر کریں، سبسکرائب کریں)
            
            3. Hashtags: 15 Viral Hashtags in Urdu script + English mix nahi, sirf Urdu aur trending PK
            Example: #دنیا_کی_باتیں #موٹیویشن #پاکستان
            
            4. Tags: 10 Tags comma separated in Urdu

            Return ONLY valid JSON like this:
            {{
              "title": "viral title here in Urdu",
              "description": "description here in Urdu...",
              "hashtags": "#tag1 #tag2 ...",
              "tags": "tag1, tag2, ..."
            }}
            Topic: {topic}
            """
            
            response = client.models.generate_content(
                model='gemini-flash-lite-latest',
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.95,
                    max_output_tokens=2000
                )
            )
            raw = response.text.strip().replace("```json","").replace("```","")
            data = json.loads(raw)
            
            title = data.get("title", topic)
            description = data.get("description", f"{topic}\n\nاس ویڈیو میں {topic} کے بارے میں تفصیل سے بات کی گئی ہے۔")
            hashtags = data.get("hashtags", "#دنیا_کی_باتیں #موٹیویشن #پاکستان")
            tags = data.get("tags", "موٹیویشن, دنیا کی باتیں, پاکستان")
            
            print(f"VIRAL TITLE: {title}", flush=True)
            print(f"HASHTAGS: {hashtags}", flush=True)
            
            os.makedirs("output", exist_ok=True)
            with open("output/title.txt", "w", encoding="utf-8") as f:
                f.write(title)
            with open("output/description.txt", "w", encoding="utf-8") as f:
                f.write(f"{description}\n\n{hashtags}")
            with open("output/hashtags.txt", "w", encoding="utf-8") as f:
                f.write(hashtags)
            with open("output/tags.txt", "w", encoding="utf-8") as f:
                f.write(tags)
            
            return title, description, hashtags, tags
            
        except Exception as e:
            print(f"Title gen error: {e}, backup use kar raha hu", flush=True)

    # Backup - Dynamic, not fixed
    backup_title = f"{topic}"
    backup_desc = f"{topic}\n\nآج کی اس ویڈیو میں ہم بات کریں گے {topic} کے بارے میں۔\n\nیہ ویڈیو آپ کی زندگی بدل سکتی ہے۔\n\nپسند کریں اور سبسکرائب ضرور کریں!\n\n#دنیا_کی_باتیں"
    backup_hashtags = "#دنیا_کی_باتیں #موٹیویشن #پاکستان #اسلامی #کامیابی #وائرل #اردو"
    backup_tags = f"{topic}, دنیا کی باتیں, موٹیویشن, پاکستان, وائرل"
    
    os.makedirs("output", exist_ok=True)
    with open("output/title.txt", "w", encoding="utf-8") as f:
        f.write(backup_title)
    with open("output/description.txt", "w", encoding="utf-8") as f:
        f.write(backup_desc)
    with open("output/hashtags.txt", "w", encoding="utf-8") as f:
        f.write(backup_hashtags)
    
    return backup_title, backup_desc, backup_hashtags, backup_tags

if __name__ == "__main__":
    t, d, h, tags = generate_title_and_hashtags(topic="بیوقوف مردوں کی نشانیاں")
    print(t)
    print(h)
