import os, requests, random, time, urllib.parse

def get_prompts_from_topic(topic):
    tl = topic.lower()
    # Ab har topic ka prompt banega, sirf Islamic nahi
    base = f"{topic}, trending, viral, highly detailed, 8k, cinematic"
    if "jinn" in tl: return [f"{base}, dark mysterious night", f"{base}, old book candle", f"{base}, foggy graveyard"]
    if "ai" in tl or "technology" in tl: return [f"{base}, futuristic tech, AI robot", f"{base}, modern city hologram", f"{base}, computer chips glowing"]
    if "news" in tl or "war" in tl: return [f"{base}, world map dramatic, news background", f"{base}, cinematic breaking news", f"{base}, global crisis"]
    return [f"{base}, motivational", f"{topic} illustration, beautiful light", f"{topic} concept art, ultra realistic"]

def generate_images(topic, num_images=6):
    os.makedirs("images", exist_ok=True)
    paths=[]
    prompts=get_prompts_from_topic(topic)
    while len(prompts) < num_images: prompts+=prompts
    prompts=prompts[:num_images]
    for i,p in enumerate(prompts):
        try:
            url=f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}?width=1280&height=720&nologo=true&seed={random.randint(1,99999)}"
            r=requests.get(url,timeout=60)
            if r.status_code==200 and len(r.content)>10000:
                path=f"images/img_{i}.jpg"
                open(path,"wb").write(r.content)
                paths.append(path)
        except: pass
        time.sleep(1.5)
    if not paths: raise Exception("Image fail")
    return paths
