import os, requests, random, time, urllib.parse

def get_prompts_from_topic(topic):
    tl = topic.lower()
    base = f"{topic}, trending, viral, highly detailed, cinematic"
    return [f"{base} 1", f"{base} 2", f"{base} 3", f"{base} 4", f"{base} 5", f"{base} 6"]

def generate_images(topic, num_images=6):
    os.makedirs("images", exist_ok=True)
    paths = []
    prompts = get_prompts_from_topic(topic)
    
    for i, p in enumerate(prompts[:num_images]):
        path = f"images/img_{i}.jpg"
        ok = False
        
        # 1. Try Pollinations
        try:
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}?width=1280&height=720&nologo=true&seed={random.randint(1,99999)}"
            print(f"Image {i+1} try Pollinations...", flush=True)
            r = requests.get(url, timeout=30)
            if r.status_code == 200 and len(r.content) > 5000:
                open(path, "wb").write(r.content)
                paths.append(path)
                ok = True
                print(f"Image {i+1} OK Pollinations", flush=True)
        except Exception as e:
            print(f"Pollinations fail {e}", flush=True)

        # 2. Agar fail to Picsum backup - ye kabhi fail nahi hota
        if not ok:
            try:
                print(f"Image {i+1} backup Picsum...", flush=True)
                url = f"https://picsum.photos/1280/720?random={random.randint(1,100000)}"
                r = requests.get(url, timeout=15)
                if r.status_code == 200:
                    open(path, "wb").write(r.content)
                    paths.append(path)
                    print(f"Image {i+1} OK Backup", flush=True)
            except Exception as e:
                print(f"Backup bhi fail {e}", flush=True)
        
        time.sleep(1)

    # 3. Last safety - agar 1 bhi image nahi bani to khali color image banao taake video rukey nahi
    if not paths:
        print("Koi image nahi bani, dummy image bana raha hu...", flush=True)
        from PIL import Image
        for i in range(3):
            img = Image.new('RGB', (1280,720), color=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            path = f"images/img_{i}.jpg"
            img.save(path)
            paths.append(path)
    
    print(f"Total {len(paths)} images ready!", flush=True)
    return paths
