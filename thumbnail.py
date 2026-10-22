from PIL import Image, ImageDraw, ImageFont
import os, glob, random, textwrap, re

# --- CONFIG ---
W, H = 1280, 720
BORDER = 24

def find_urdu_font():
    possible = [
        "Jameel Noori Nastaleeq.ttf",
        "Jameel-Noori-Nastaleeq.ttf",
        "NotoNastaliqUrdu-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoNastaliqUrdu-Bold.ttf",
        "arial.ttf"
    ]
    for p in possible:
        if os.path.exists(p):
            return p
    return None

def wrap_urdu_text(text, max_chars=18):
    # Urdu ke liye chote tukre me todna
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        if len(cur + " " + w) <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines[:3]  # Max 3 lines

def fix_urdu_render(text):
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except:
        return text  # agar library nahi to waise hi

def generate_thumbnail(title_text):
    print(f"[THUMBNAIL] Topic: {title_text}", flush=True)
    font_path = find_urdu_font()
    print(f"[THUMBNAIL] Font: {font_path}", flush=True)

    # 1. Background image lo
    bg_files = glob.glob("images/*.jpg") + glob.glob("output/bg_*.jpg") + glob.glob("assets/*.jpg")
    if bg_files:
        bg = Image.open(random.choice(bg_files)).convert("RGB").resize((W, H))
    else:
        bg = Image.new("RGB", (W, H), (20, 10, 10))

    # 2. Dark + gradient taake text chamke
    dark = Image.new("RGB", (W, H), (0,0,0))
    bg = Image.blend(bg, dark, 0.55)
    
    draw = ImageDraw.Draw(bg)

    # 3. Fonts
    try:
        if font_path:
            big_font = ImageFont.truetype(font_path, 130)
            small_font = ImageFont.truetype(font_path, 90)
        else:
            big_font = ImageFont.load_default()
            small_font = big_font
    except Exception as e:
        print(f"Font load fail {e}", flush=True)
        big_font = ImageFont.load_default()
        small_font = big_font

    # 4. TEXT FIX - Wrap + Reshape
    title_text = title_text.strip().replace("  ", " ")[:50]
    lines = wrap_urdu_text(title_text, 20)
    fixed_lines = [fix_urdu_render(l) for l in lines]

    # 5. Draw text center me - Peela + Kaala Stroke
    y = 150
    for i, line in enumerate(fixed_lines):
        # Shadow pehle
        # Main text
        # Center align ke liye bbox nikalo
        bbox = draw.textbbox((0,0), line, font=big_font, stroke_width=14)
        text_w = bbox[2] - bbox[0]
        x = (W - text_w) // 2
        
        # Stroke wala viral text
        draw.text((x, y), line, font=big_font, fill="#FFEB00", 
                  stroke_width=16, stroke_fill="black")
        y += 160

    # 6. Red Border + Corner cuts (Viral look)
    final_img = Image.new("RGB", (W + BORDER*2, H + BORDER*2), "#FF0000")
    final_img.paste(bg, (BORDER, BORDER))
    
    draw_f = ImageDraw.Draw(final_img)
    # Upar ke kone par design
    draw_f.polygon([(0,0), (140,0), (0,140)], fill="#FF0000")
    draw_f.polygon([(W+BORDER*2,0), (W+BORDER*2-140,0), (W+BORDER*2,140)], fill="#FF0000")

    os.makedirs("output", exist_ok=True)
    out1 = "output/thumbnail.jpg"
    out2 = "output/final_thumbnail.jpg"
    out3 = "thumbnail.jpg"
    final_img.save(out1, quality=95)
    final_img.save(out2, quality=95)
    final_img.save(out3, quality=95)
    
    print(f"[THUMBNAIL] Saved: {out1}", flush=True)
    return out1

# Tumhare purane error ko khatam karne ke liye 3 naam
def create_thumbnail(t): return generate_thumbnail(t)
def make_thumbnail(t): return generate_thumbnail(t)
def create(t): return generate_thumbnail(t)
