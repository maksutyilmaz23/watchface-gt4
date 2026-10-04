import os
import math
from PIL import Image, ImageDraw

CANVAS_SIZE = (466, 466)
CENTER = (233, 233)
RADIUS = 220

# Renk Paleti (Rose Gold & Sunburst Kahve)
BG_CENTER = (95, 50, 35, 255)
BG_EDGE = (30, 15, 10, 255)
ROSE_GOLD = (212, 155, 128, 255)
ROSE_GOLD_LIGHT = (240, 195, 170, 255)
WHITE = (255, 255, 255, 220)

RAW_BG = "assets/raw/bg/seiko_presage_bg.png"
RAW_HOUR = "assets/raw/hands/seiko_hour.png"
RAW_MINUTE = "assets/raw/hands/seiko_minute.png"
RAW_SECOND = "assets/raw/hands/seiko_second.png"

os.makedirs("assets/raw/bg", exist_ok=True)
os.makedirs("assets/raw/hands", exist_ok=True)

def create_background():
    img = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Sunburst Kahve Degrade Arka Plan
    for r in range(RADIUS, 0, -1):
        factor = r / RADIUS
        red = int(BG_EDGE[0] * factor + BG_CENTER[0] * (1 - factor))
        green = int(BG_EDGE[1] * factor + BG_CENTER[1] * (1 - factor))
        blue = int(BG_EDGE[2] * factor + BG_CENTER[2] * (1 - factor))
        draw.ellipse([CENTER[0]-r, CENTER[1]-r, CENTER[0]+r, CENTER[1]+r], fill=(red, green, blue, 255))

    # Dakika Çizgileri ve 12 Saat İmleçleri
    for i in range(60):
        angle = math.radians(i * 6)
        if i % 5 == 0:
            r_in = RADIUS - 28
            r_out = RADIUS - 8
            x1 = CENTER[0] + r_in * math.sin(angle)
            y1 = CENTER[1] - r_in * math.cos(angle)
            x2 = CENTER[0] + r_out * math.sin(angle)
            y2 = CENTER[1] - r_out * math.cos(angle)
            draw.line([(x1, y1), (x2, y2)], fill=ROSE_GOLD, width=4)
        else:
            r_in = RADIUS - 14
            r_out = RADIUS - 8
            x1 = CENTER[0] + r_in * math.sin(angle)
            y1 = CENTER[1] - r_in * math.cos(angle)
            x2 = CENTER[0] + r_out * math.sin(angle)
            y2 = CENTER[1] - r_out * math.cos(angle)
            draw.line([(x1, y1), (x2, y2)], fill=WHITE, width=1)

    # Tarih Çerçevesi (Saat 3 Yönü)
    date_box = [CENTER[0] + 110, CENTER[1] - 16, CENTER[0] + 160, CENTER[1] + 16]
    draw.rectangle(date_box, outline=ROSE_GOLD, width=2, fill=(20, 10, 8, 255))

    # Logolar
    draw.text((CENTER[0], CENTER[1] - 75), "SEIKO", fill=ROSE_GOLD_LIGHT, anchor="mm")
    draw.text((CENTER[0], CENTER[1] + 65), "PRESAGE", fill=WHITE, anchor="mm")
    draw.text((CENTER[0], CENTER[1] + 80), "AUTOMATIC", fill=WHITE, anchor="mm")

    img.save(RAW_BG, "PNG")
    print(f"[+] Arka plan oluşturuldu: {RAW_BG}")

def create_hour_hand():
    img = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    points = [
        (CENTER[0], CENTER[1] - 110),
        (CENTER[0] + 8, CENTER[1] - 20),
        (CENTER[0], CENTER[1] + 20),
        (CENTER[0] - 8, CENTER[1] - 20)
    ]
    draw.polygon(points, fill=ROSE_GOLD, outline=ROSE_GOLD_LIGHT)
    img.save(RAW_HOUR, "PNG")
    print(f"[+] Akrep oluşturuldu: {RAW_HOUR}")

def create_minute_hand():
    img = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    points = [
        (CENTER[0], CENTER[1] - 175),
        (CENTER[0] + 6, CENTER[1] - 20),
        (CENTER[0], CENTER[1] + 25),
        (CENTER[0] - 6, CENTER[1] - 20)
    ]
    draw.polygon(points, fill=ROSE_GOLD, outline=ROSE_GOLD_LIGHT)
    img.save(RAW_MINUTE, "PNG")
    print(f"[+] Yelkovan oluşturuldu: {RAW_MINUTE}")

def create_second_hand():
    img = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.line([(CENTER[0], CENTER[1] + 45), (CENTER[0], CENTER[1] - 185)], fill=ROSE_GOLD_LIGHT, width=2)
    draw.polygon([(CENTER[0], CENTER[1] + 20), (CENTER[0] + 4, CENTER[1] + 30), (CENTER[0], CENTER[1] + 40), (CENTER[0] - 4, CENTER[1] + 30)], fill=ROSE_GOLD)
    draw.ellipse([CENTER[0]-5, CENTER[1]-5, CENTER[0]+5, CENTER[1]+5], fill=ROSE_GOLD_LIGHT)
    img.save(RAW_SECOND, "PNG")
    print(f"[+] Saniye ibresi oluşturuldu: {RAW_SECOND}")

if __name__ == "__main__":
    create_background()
    create_hour_hand()
    create_minute_hand()
    create_second_hand()
