import os
import json

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except:
    GEMINI_AVAILABLE = False

def generate_title_and_hashtags(topic=""):
    script_text = topic
    try:
        if os.path.exists("final_script.txt"):
            with open("final_script.txt", 'r', encoding='utf-8') as f:
                script_text = f.read()[:3000]
        print(f"Title ke liye topic: {topic}", flush=True)
    except Exception as e:
        print(f"Read error {e}", flush=True)

    if GEMINI_AVAILABLE and os.getenv("GEMINI_API_KEY"):
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"""
            Topic: {topic}
            Script: {script_text[:2000]}
            
            Create viral YouTube Title (Roman Urdu, 60 chars, high CTR), Description (Roman Urdu 2 lines + bullets), 15 Hashtags, 10 tags.
            Return ONLY JSON: {{"title": "...", "description": "...", "hashtags": "#a #b", "tags": "a, b"}}
            """
            response = model.generate_content(prompt)
            raw = response.text.strip().replace("```json","").replace("```","")
            data = json.loads(raw)
            
            title = data.get("title", topic)
            desc = data.get("description", topic)
            hashtags = data.get("hashtags", "#worldofwisdom #viral #pakistan")
            tags = data.get("tags", "world of wisdom")
            
            os.makedirs("output", exist_ok=True)
            with open("output/title.txt", "w", encoding="utf-8") as f: f.write(title)
            with open("output/description.txt", "w", encoding="utf-8") as f: f.write(f"{desc}\n\n{hashtags}")
            with open("output/hashtags.txt", "w", encoding="utf-8") as f: f.write(hashtags)
            
            print(f"VIRAL TITLE: {title}", flush=True)
            return title, desc, hashtags, tags
        except Exception as e:
            print(f"Title gen fail {e}", flush=True)

    backup_title = f"{topic} | Jo 90% Log Nahi Jante"
    backup_desc = f"{topic} - Is video me mukammal haqeeqat janiye. Like Share Subscribe!"
    backup_hashtags = "#worldofwisdom #motivation #pakistan #viral #trending #islamic #kamyabi #wisdom"
    backup_tags = f"{topic}, world of wisdom, viral"
    
    os.makedirs("output", exist_ok=True)
    with open("output/title.txt", "w", encoding="utf-8") as f: f.write(backup_title)
    return backup_title, backup_desc, backup_hashtags, backup_tags
