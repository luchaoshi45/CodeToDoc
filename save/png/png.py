from PIL import Image, ImageDraw, ImageFont
import os

def save_png(
    text,
    filename,
    font_path="/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    font_size=20,
    image_size=(800, 600),
    bg_color=(255,255,255),
    text_color=(0,0,0)
):
    if font_path and os.path.exists(font_path):
        font = ImageFont.truetype(font_path, font_size)
    else:
        raise FileNotFoundError(f"Font file not found: {font_path}")
    img = Image.new('RGB', image_size, color=bg_color)
    draw = ImageDraw.Draw(img)
    lines = text.split('\n')
    x, y = 10, 10
    for line in lines:
        draw.text((x, y), line, fill=text_color, font=font)
        y += font_size + 5
    img.save(filename)
