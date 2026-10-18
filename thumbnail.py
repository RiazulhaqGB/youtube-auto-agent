from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

def generate_thumbnail(topic, output_path="thumbnail.jpg"):
    # Background image
    url = "https://source.unsplash.com/1280x720/?cricket,stadium"
    try:
        r = requests.get(url, timeout=10)
        img = Image.open(BytesIO(r.content)).convert("RGB")
    except:
        img = Image.new("RGB", (1280,720), (0,0,0))
    
    draw = ImageDraw.Draw(img)
    # Yellow text with red border style
    try:
        font = ImageFont.truetype("arial.ttf", 90)
    except:
        font = ImageFont.load_default()

    # Text with stroke (laal border, peela text)
    draw.text((50, 50), topic, fill="yellow", stroke_width=8, stroke_fill="red", font=font)
    
    img.save(output_path)
    print(f"Thumbnail saved: {output_path}")
    return output_path
