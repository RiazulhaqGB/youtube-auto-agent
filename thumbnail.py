import os
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

FONT_PATH = "NotoNastaliqUrdu.ttf"

def get_urdu_font(size=80):
    # Agar file nahi hai to saaf error dega
    if not os.path.exists(FONT_PATH):
        print(f"FONT FILE NOT FOUND: {FONT_PATH} repo me upload karo!", flush=True)
        print(f"Current files: {os.listdir('.')}", flush=True)
        raise FileNotFoundError(f"{FONT_PATH} missing. Upload font file to repo root.")
    
    try:
        print(f"Loading font: {FONT_PATH} size {size}", flush=True)
        return ImageFont.truetype(FONT_PATH, size)
    except Exception as e:
        print(f"Font load error: {e}", flush=True)
        raise e

def fix_urdu(text):
    try:
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except Exception as e:
        print(f"Reshape error: {e}", flush=True)
        return text

def generate_thumbnail(title_text, image_paths=None):
    os.makedirs("output", exist_ok=True)
    output_path = "output/thumbnail.jpg"
    bg = None
    if image_paths and len(image_paths) > 0 and os.path.exists(image_paths[0]):
        try:
            bg = Image.open(image_paths[0]).convert("RGB").resize((1280, 720))
        except:
            pass
    if bg is None:
        bg = Image.new("RGB", (1280, 720), (20, 10, 30))
    
    overlay = Image.new("RGBA", (1280, 720), (0, 0, 0, 140))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(bg)
    
    text = title_text.strip()[:80]
    if len(text) > 25:
        mid = len(text)//2
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

    line1 = fix_urdu(line1)
    line2 = fix_urdu(line2)

    font_big = get_urdu_font(85)
    font_small = get_urdu_font(75)

    def draw_centered_line(text_line, y, font):
        if not text_line.strip():
            return
        bbox = draw.textbbox((0,0), text_line, font=font, stroke_width=8)
        w = bbox[2] - bbox[0]
        x = (1280 - w) // 2
        draw.text((x, y), text_line, font=font, fill="white", stroke_width=8, stroke_fill="black")

    if line2:
        draw_centered_line(line1, 220, font_big)
        draw_centered_line(line2, 350, font_small)
    else:
        draw_centered_line(line1, 290, font_big)

    try:
        small_font = get_urdu_font(35)
        draw.text((30, 670), "World Trending Hub", font=small_font, fill=(255,255,255))
    except:
        pass

    bg.save(output_path, quality=95)
    print(f"Thumbnail Done: {output_path}", flush=True)
    return output_path
