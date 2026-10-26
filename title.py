import os, json
from google import genai
from google.genai import types

def generate_title_and_hashtags(script_path, topic, channel_name="World Trending Hub"):
    os.makedirs("output", exist_ok=True) # <-- YE LINE SAB SE ZAROORI HAI, isi se error khatam hoga
    
    txt=topic
    if os.path.exists(script_path):
        try:
            txt=open(script_path,encoding="utf-8").read()[:3000]
        except: pass
    
    client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prompt=f"""You are {channel_name} expert. Topic: {topic}, Script: {txt}
    Create VIRAL Title in PURE URDU SCRIPT. 
    1. Title 55 chars max, CTR high, har bar NAYA, "90% log nahi jante" wala jumla kabhi use mat karna.
    2. Description 2 lines hook + 3 points + CTA Urdu me.
    3. 12 Hashtags mix Urdu+Trending.
    4. 10 Tags.
    Return ONLY valid JSON like {{ "title": "...", "description": "...", "hashtags": "...", "tags": "..." }}"""
    
    try:
        response=client.models.generate_content(model='gemini-flash-lite-latest', contents=prompt, config=types.GenerateContentConfig(temperature=0.95))
        raw=response.text.replace("```json","").replace("```","").strip()
        data=json.loads(raw)
        title=data.get("title", topic)
        desc=data.get("description", topic)
        hashtags=data.get("hashtags", "#وائرل")
        tags=data.get("tags", topic)
    except Exception as e:
        print(f"Title AI fail {e}, backup use", flush=True)
        title=topic
        desc=f"{topic} par aaj ki video"
        hashtags="#وائرل #پاکستان #WorldTrendingHub"
        tags=topic

    open("output/title.txt","w",encoding="utf-8").write(title)
    open("output/description.txt","w",encoding="utf-8").write(f"{desc}\n\n{hashtags}")
    open("output/hashtags.txt","w",encoding="utf-8").write(hashtags)
    open("output/tags.txt","w",encoding="utf-8").write(tags)
    print(f"TITLE FIXED OK: {title}", flush=True)
    return title, desc, hashtags, tags
