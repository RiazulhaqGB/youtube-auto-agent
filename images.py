import os
import requests
import random
import time

def generate_images(topic, num_images=5):
    os.makedirs("images", exist_ok=True)
    image_paths = []
    
    # Free image source - Picsum (never fails)
    for i in range(num_images):
        try:
            url = f"https://picsum.photos/1280/720?random={random.randint(1,10000)}"
            r = requests.get(url, timeout=15)
            path = f"images/img_{i}.jpg"
            with open(path, "wb") as f:
                f.write(r.content)
            image_paths.append(path)
            print(f"Image {i+1} downloaded", flush=True)
            time.sleep(1)
        except Exception as e:
            print(f"Image {i} failed: {e}", flush=True)
    
    if not image_paths:
        raise Exception("No images downloaded!")
        
    return image_paths
