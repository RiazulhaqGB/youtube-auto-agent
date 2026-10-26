import os, json
from google import genai
from google.genai import types
def generate_title_and_hashtags(script_path, topic, channel_name="World Trending Hub"):
    txt=topic
    if os.path.exists(script_path):
        txt=open(script_path,encoding="utf-8").read()[:3000]
    client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prompt=f"""You are {channel_name} expert. Topic: {topic}, Script: {txt}
    Create VIRAL Title in PURE URDU SCRIPT. 
    1. Title 55 chars max, CTR high, har bar NAYA, "90% log nahi jante" wala jumla kabhi use mat karna.
    2. Description 2 lines hook + 3 points + CTA Urdu me.
    3. 12 Hashtags mix Urdu+Trending.
    4. 10 Tags.
    Return JSON {{title, description, hashtags, tags}}"""
    response=client.models.generate_content(model='gemini-flash-lite-latest', contents=prompt, config=types.GenerateContentConfig(temperature=0.95))
    raw=response.text.replace("```json","").replace("```","").strip()
    data=json.loads(raw)
    title=data["title"]; desc=data["description"]; hashtags=data["hashtags"]; tags=data["tags"]
    open("output/title.txt","w",encoding="utf-8").write(title)
    open("output/description.txt","w",encoding="utf-8").write(f"{desc}\n\n{hashtags}")
    return title, desc, hashtags, tags
