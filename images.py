import os
import requests
import random
import time
import urllib.parse

def get_prompts_from_topic(topic):
    topic_lower = topic.lower()
    
    # Topic se samajh ke prompt banao
    if "jinnat" in topic_lower or "jinn" in topic_lower:
        return [
            "dark mysterious Islamic jinn in desert night, cinematic, horror atmosphere",
            "ancient Islamic manuscript about jinns, old book, candle light",
            "eerie Islamic graveyard at night, foggy, mysterious lights"
        ]
    elif "qayamat" in topic_lower or "nishani" in topic_lower:
        return [
            "Islamic Day of Judgement, dramatic sky, Kaaba, cinematic",
            "earthquake apocalyptic Islamic scene, dramatic clouds",
            "old Islamic signs of Qayamat book, ancient Arabic text"
        ]
    elif "rizq" in topic_lower or "barkat" in topic_lower or "wazifa" in topic_lower:
        return [
            "Muslim man praying with open hands, rizq, barakah, light from sky, cinematic",
            "Islamic wealth barakah, gold coins with Islamic pattern, beautiful light",
            "Quran open on table, praying hands, peaceful Islamic home"
        ]
    elif "dabao" in topic_lower or "zehni" in topic_lower:
        return [
            "stressed Muslim man holding head, anxiety, dark room, cinematic",
            "peaceful Islamic meditation, Muslim praying, calm, light",
            "brain with stress vs peace concept, Islamic style"
        ]
    else:
        # General Islamic motivational
        clean_topic = topic.replace("-", "").strip()
        return [
            f"{clean_topic}, Islamic motivational, cinematic, highly detailed",
            f"Muslim man thinking deeply about {clean_topic}, mosque background",
            f"Islamic illustration of {clean_topic}, beautiful light, spiritual"
        ]

def generate_images(topic, num_images=5):
    os.makedirs("images", exist_ok=True)
    image_paths = []
    
    prompts = get_prompts_from_topic(topic)
    # Agar 5 images chahiye to prompts ko repeat karo
    while len(prompts) < num_images:
        prompts += prompts
    prompts = prompts[:num_images]

    print(f"Topic: {topic}", flush=True)
    print(f"Prompts: {prompts}", flush=True)

    for i, prompt in enumerate(prompts):
        try:
            # Pollination AI - Free and topic ke mutabiq
            encoded_prompt = urllib.parse.quote(prompt)
            # Random seed taake har bar nayi image aaye
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&seed={random.randint(1,100000)}"
            
            print(f"Image {i+1} download kar raha hu: {prompt[:50]}...", flush=True)
            r = requests.get(url, timeout=60)
            
            if r.status_code == 200 and len(r.content) > 10000:
                path = f"images/img_{i}.jpg"
                with open(path, "wb") as f:
                    f.write(r.content)
                image_paths.append(path)
                print(f"Image {i+1} Done!", flush=True)
            else:
                print(f"Image {i+1} fail, Picsum backup use kar raha hu", flush=True)
                raise Exception("Pollination fail")

        except Exception as e:
            print(f"Backup image le raha hu: {e}", flush=True)
            # Backup - Picsum kabhi fail nahi hota
            try:
                url = f"https://picsum.photos/1280/720?random={random.randint(1,100000)}"
                r = requests.get(url, timeout=15)
                path = f"images/img_{i}.jpg"
                with open(path, "wb") as f:
                    f.write(r.content)
                image_paths.append(path)
            except:
                pass
        
        time.sleep(2)
    
    if not image_paths:
        raise Exception("Koi image download nahi hui!")
        
    print(f"Total {len(image_paths)} images script ke mutabiq ready!", flush=True)
    return image_paths
