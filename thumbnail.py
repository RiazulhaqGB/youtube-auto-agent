import os, requests, random
from PIL import Image, ImageDraw, ImageFont

# Urdu font ka link - ye auto download hoga
FONT_URL = "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoNastaliqUrdu/NotoNastaliqUrdu-Regular.ttf"
FONT_PATH = "NotoNastaliqUrdu.ttf"

def get_urdu_font(size=80):
    if not os.path.exists(FONT_PATH):
        try:
            print("Downloading Urdu font...", flush=True)
            r = requests.get(FONT_URL, timeout=30)
            open(FONT_PATH, "wb").write(r.content)
        except:
            pass
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()

def generate_thumbnail(title_text, image_paths=None):
    os.makedirs("output", exist_ok=True)
    output_path = "output/thumbnail.jpg"
    
    # 1. Background - agar video ki image mili to wahi use karo warna apna background
    bg = None
    if image_paths and len(image_paths) > 0 and os.path.exists(image_paths[0]):
        try:
            bg = Image.open(image_paths[0]).convert("RGB").resize((1280, 720))
        except:
            pass
    
    if bg is None:
        bg = Image.new("RGB", (1280, 720), (20, 10, 30))
    
    # 2. Dark overlay taake text chamke
    overlay = Image.new("RGBA", (1280, 720), (0, 0, 0, 140))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")
    
    draw = ImageDraw.Draw(bg)
    
    # 3. Title saaf karo - 2 lines me todo
    text = title_text.strip()[:80] # zyada lamba na ho
    # 2 hisso me tod do taake blue wale jaisa lage
    if len(text) > 25:
        mid = len(text)//2
        # space ke qareeb todo
        space_idx = text.rfind(' ', 0, mid+10)
        if space_idx != -1:
            line1 = text[:space_idx]
            line2 = text[space_idx+1:]
        else:
            line1 = text[:mid]
            line2 = text[mid:]
    else:
        line1 = text
        line2 = ""

    font_big = get_urdu_font(85)
    font_small = get_urdu_font(75)

    # 4. Text draw karo - White text + Black stroke (blue wale ki tarah viral style)
    # Center me
    def draw_centered_line(text_line, y, font):
        bbox = draw.textbbox((0,0), text_line, font=font)
        w = bbox[2] - bbox[0]
        x = (1280 - w) // 2
        # Black stroke
        for dx in [-3,-2,-1,0,1,2,3]:
            for dy in [-3,-2,-1,0,1,2,3]:
                draw.text((x+dx, y+dy), text_line, font=font, fill="black")
        draw.text((x, y), text_line, font=font, fill="white")

    if line2:
        draw_centered_line(line1, 220, font_big)
        draw_centered_line(line2, 350, font_small)
    else:
        draw_centered_line(line1, 290, font_big)

    # 5. Neeche chota brand text (optional)
    try:
        small_font = get_urdu_font(35)
        draw.text((30, 670), "World Trending Hub", font=small_font, fill=(255,255,255,180))
    except:
        pass

    bg.save(output_path, quality=95)
    print(f"Thumbnail Done: {output_path}", flush=True)
    return output_path
