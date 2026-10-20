import os
import json

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except:
    GEMINI_AVAILABLE = False

def generate_title_and_hashtags(script_path="final_script.txt", topic=""):
    """
    Script ke mutabiq viral title, description, hashtags
    """
    # 1. Script padho
    script_text = topic
    try:
        if os.path.exists(script_path):
            with open(script_path, 'r', encoding='utf-8') as f:
                script_text = f.read()[:3000] # Pehle 3000 chars kaafi hain
        elif os.path.exists("script.txt"):
            with open("script.txt", 'r', encoding='utf-8') as f:
                script_text = f.read()[:3000]
        else:
            # Agar file nahi to topic hi use karo
            script_text = topic
            
        print(f"Title ke liye script/topic: {script_text[:100]}...", flush=True)
    except Exception as e:
        print(f"Script read error {e}", flush=True)
        script_text = topic

    # 2. Gemini se viral title + hashtags
    if GEMINI_AVAILABLE and os.getenv("GEMINI_API_KEY"):
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            You are World of Wisdom YouTube expert for Pakistan audience.
            
            Script/Topic: {script_text}
            
            Task:
            1. Create 1 VIRAL YouTube Title in Roman Urdu (60 chars max, clickable, high CTR)
            Example: Bewaqoof Mardon Ki 9 Nishaniyan | 90% Log Ye Galti Karte Hain
            
            2. Create 1 SEO Description in Roman Urdu (2 lines + 3 bullet points + call to action)
            
            3. Create 15 Viral Hashtags: 5 Roman Urdu + 5 English + 5 Trending PK
            Example: #bewaqoofmard #kamyabzindagi #motivation #worldofwisdom #pakistan
            
            4. Create 10 Tags for YouTube (comma separated)
            
            Return ONLY valid JSON like this:
            {{
              "title": "viral title here",
              "description": "description here...",
              "hashtags": "#tag1 #tag2 ...",
              "tags": "tag1, tag2, ..."
            }}
            
            Topic must match script: {topic}
            """
            
            response = model.generate_content(prompt)
            raw = response.text.strip().replace("```json","").replace("```","")
            
            data = json.loads(raw)
            
            title = data.get("title", topic)
            description = data.get("description", f"{topic}\n\nIs video me {topic} ke bare me tafseel se baat ki gayi hai.\n\nLike, Share, Subscribe zaroor karen!")
            hashtags = data.get("hashtags", "#worldofwisdom #motivation #pakistan")
            tags = data.get("tags", "motivation, world of wisdom, pakistan")
            
            print(f"VIRAL TITLE: {title}", flush=True)
            print(f"HASHTAGS: {hashtags}", flush=True)
            
            # Files me save karo taake YouTube upload me use ho
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

    # Backup - Agar Gemini fail
    backup_title = f"{topic} | Jo 90% Log Nahi Jante"
    backup_desc = f"{topic}\n\nAaj ki is video me hum baat karenge {topic} ke bare me.\n\nYe video aapki zindagi badal sakti hai.\n\nLike aur Subscribe zaroor karen!\n\n#worldofwisdom"
    backup_hashtags = "#worldofwisdom #motivation #pakistan #islamic #kamyabi #bewaqoofmard #viral #trending #urdu #wisdom"
    backup_tags = f"{topic}, world of wisdom, motivation, pakistan, viral"
    
    os.makedirs("output", exist_ok=True)
    with open("output/title.txt", "w", encoding="utf-8") as f:
        f.write(backup_title)
    with open("output/description.txt", "w", encoding="utf-8") as f:
        f.write(backup_desc)
    with open("output/hashtags.txt", "w", encoding="utf-8") as f:
        f.write(backup_hashtags)
    
    return backup_title, backup_desc, backup_hashtags, backup_tags

if __name__ == "__main__":
    # Test
    t, d, h, tags = generate_title_and_hashtags(topic="Bewaqoof Mardon Ki Nishaniyan")
    print(t)
    print(h)
