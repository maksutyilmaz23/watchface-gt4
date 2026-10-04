import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

CANVAS_SIZE = (466, 466)
CENTER = (233, 233)
RADIUS = 218

RAW_BG = "assets/raw/bg/seiko_presage_bg.png"
RAW_HOUR = "assets/raw/hands/seiko_hour.png"
RAW_MINUTE = "assets/raw/hands/seiko_minute.png"
RAW_SECOND = "assets/raw/hands/seiko_second.png"

# Renkler
ROSE_GOLD = (222, 162, 134, 255)
ROSE_GOLD_DARK = (160, 105, 80, 255)
ROSE_GOLD_LIGHT = (248, 210, 190, 255)
SILVER_TEXT = (220, 220, 225, 240)
WHITE = (255, 255, 255, 255)

os.makedirs("assets/raw/bg", exist_ok=True)
os.makedirs("assets/raw/hands", exist_ok=True)

def create_textured_background():
    img = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    # 1. Temel Degrade Arka Plan (Sarımsı Kahveden Koyu Siyahımsı Kahveye)
    for r in range(RADIUS, 0, -1):
        f = r / RADIUS
        # Kenarlar koyu kahve/siyah, merkez amber kahve
        red = int(25 * f + 115 * (1 - f**1.5))
        green = int(12 * f + 60 * (1 - f**1.5))
        blue = int(8 * f + 30 * (1 - f**1.5))
        draw.ellipse([CENTER[0]-r, CENTER[1]-r, CENTER[0]+r, CENTER[1]+r], fill=(red, green, blue, 255))

    # 2. Birebir Cocktail Time Dokusu (Fraktal/Kristalize Efekt)
    texture = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    tex_draw = ImageDraw.Draw(texture)
    
    random.seed(42) # Sabit doku deseni
    for _ in range(3500):
        ang = random.uniform(0, 2 * math.pi)
        dist = random.uniform(0, RADIUS - 10)
        x = CENTER[0] + dist * math.cos(ang)
        y = CENTER[1] + dist * math.sin(ang)
        length = random.uniform(8, 35)
        ang_line = ang + random.uniform(-0.6, 0.6)
        x2 = x + length * math.cos(ang_line)
        y2 = y + length * math.sin(ang_line)
        
        alpha = int(random.uniform(15, 55) * (1 - (dist / RADIUS)**2))
        bright = random.choice([ROSE_GOLD_LIGHT, (170, 95, 55, alpha), (220, 140, 85, alpha)])
        tex_draw.line([(x, y), (x2, y2)], fill=bright, width=1)

    texture = texture.filter(GaussianBlur(0.8))
    img = Image.alpha_composite(img, texture)
    draw = ImageDraw.Draw(img)

    # 3. Dış Dairesel Dikey Dakika Çizgileri (Halka)
    r_track = RADIUS - 6
    for i in range(60):
        ang = math.radians(i * 6)
        if i % 5 == 0:
            x1 = CENTER[0] + (r_track - 10) * math.sin(ang)
            y1 = CENTER[1] - (r_track - 10) * math.cos(ang)
            x2 = CENTER[0] + r_track * math.sin(ang)
            y2 = CENTER[1] - r_track * math.cos(ang)
            draw.line([(x1, y1), (x2, y2)], fill=ROSE_GOLD_LIGHT, width=2)
        else:
            x1 = CENTER[0] + (r_track - 6) * math.sin(ang)
            y1 = CENTER[1] - (r_track - 6) * math.cos(ang)
            x2 = CENTER[0] + r_track * math.sin(ang)
            y2 = CENTER[1] - r_track * math.cos(ang)
            draw.line([(x1, y1), (x2, y2)], fill=(180, 140, 120, 180), width=1)

    # 4. Birebir 3D Rose Gold İndeksler (Kama/Arrowhead)
    def draw_index(angle_deg, is_12=False):
        ang = math.radians(angle_deg)
        r_out = RADIUS - 22
        r_in = RADIUS - 58 if not is_12 else RADIUS - 62
        w = 9 if not is_12 else 13
        
        # Merkez noktalar
        cx_out = CENTER[0] + r_out * math.sin(ang)
        cy_out = CENTER[1] - r_out * math.cos(ang)
        cx_in = CENTER[0] + r_in * math.sin(ang)
        cy_in = CENTER[1] - r_in * math.cos(ang)
        
        # Dik açılar (Sol ve Sağ Köşeler)
        perp = ang + math.pi/2
        lx = cx_out - (r_out - r_in)*0.4 * math.sin(ang) + (w/2) * math.cos(perp)
        ly = cy_out + (r_out - r_in)*0.4 * math.cos(ang) + (w/2) * math.sin(perp)
        rx = cx_out - (r_out - r_in)*0.4 * math.sin(ang) - (w/2) * math.cos(perp)
        ry = cy_out + (r_out - r_in)*0.4 * math.cos(ang) - (w/2) * math.sin(perp)
        
        # Sol Yüzey (Açık Rose Gold)
        draw.polygon([(cx_out, cy_out), (lx, ly), (cx_in, cy_in)], fill=ROSE_GOLD_LIGHT)
        # Sağ Yüzey (Gölgeli Rose Gold - 3D Efekti)
        draw.polygon([(cx_out, cy_out), (rx, ry), (cx_in, cy_in)], fill=ROSE_GOLD_DARK)

    for i in range(12):
        if i == 0:
            # 12 Yönü Çift Kama
            draw_index(356, is_12=True)
            draw_index(4, is_12=True)
        elif i == 4:
            # Saat 4.5 Yönündeki Dairesel Tarih Penceresi (İndeks Kısa)
            continue
        else:
            draw_index(i * 30)

    # 5. Dairesel Tarih Penceresi (Saat 4:30 Pozisyonu - Görseldeki Gibi)
    date_ang = math.radians(135) # 4:30 açısı
    date_r = RADIUS - 55
    dx = CENTER[0] + date_r * math.sin(date_ang)
    dy = CENTER[1] - date_r * math.cos(date_ang)
    
    # Siyah Arka Planlı Yuvarlak Çerçeve
    draw.ellipse([dx-15, dy-15, dx+15, dy+15], fill=(15, 10, 10, 255), outline=ROSE_GOLD, width=2)
    draw.text((dx, dy), "6", fill=WHITE, anchor="mm", font_size=16)

    # 6. Kabarık Metalik Logolar
    draw.text((CENTER[0], CENTER[1] - 70), "SEIKO", fill=SILVER_TEXT, anchor="mm", font_size=22)
    draw.text((CENTER[0], CENTER[1] + 65), "PRESAGE", fill=ROSE_GOLD_LIGHT, anchor="mm", font_size=13)
    draw.text((CENTER[0], CENTER[1] + 82), "AUTOMATIC", fill=(200, 200, 200, 200), anchor="mm", font_size=10)
    draw.text((CENTER[0], CENTER[1] + 175), "JAPAN 4R35...", fill=(150, 130, 120, 180), anchor="mm", font_size=8)

    img.save(RAW_BG, "PNG")
    print(f"[+] HD Birebir Arka Plan Oluşturuldu: {RAW_BG}")

def create_hd_hands():
    # Dauphine Akrep (3D Çift Kesim)
    img_h = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw_h = ImageDraw.Draw(img_h)
    
    # Sol Taraf
    draw_h.polygon([(CENTER[0], CENTER[1] - 120), (CENTER[0] - 10, CENTER[1] - 25), (CENTER[0], CENTER[1] + 22)], fill=ROSE_GOLD_LIGHT)
    # Sağ Taraf (Gölgeli)
    draw_h.polygon([(CENTER[0], CENTER[1] - 120), (CENTER[0] + 10, CENTER[1] - 25), (CENTER[0], CENTER[1] + 22)], fill=ROSE_GOLD_DARK)
    img_h.save(RAW_HOUR, "PNG")

    # Dauphine Yelkovan (3D Çift Kesim)
    img_m = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw_m = ImageDraw.Draw(img_m)
    
    draw_m.polygon([(CENTER[0], CENTER[1] - 182), (CENTER[0] - 8, CENTER[1] - 25), (CENTER[0], CENTER[1] + 28)], fill=ROSE_GOLD_LIGHT)
    draw_m.polygon([(CENTER[0], CENTER[1] - 182), (CENTER[0] + 8, CENTER[1] - 25), (CENTER[0], CENTER[1] + 28)], fill=ROSE_GOLD_DARK)
    img_m.save(RAW_MINUTE, "PNG")

    # İnce Rose Gold Saniye İbresi ve Karşı Ağırlık Halkası
    img_s = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw_s = ImageDraw.Draw(img_s)
    
    # İnce İbre Çizgisi
    draw_s.line([(CENTER[0], CENTER[1] + 45), (CENTER[0], CENTER[1] - 192)], fill=ROSE_GOLD_LIGHT, width=2)
    # Arka Dairesel Karşı Ağırlık
    draw_s.ellipse([CENTER[0]-7, CENTER[1]+20, CENTER[0]+7, CENTER[1]+34], outline=ROSE_GOLD_LIGHT, width=2)
    # Orta Kapak
    draw_s.ellipse([CENTER[0]-5, CENTER[1]-5, CENTER[0]+5, CENTER[1]+5], fill=ROSE_GOLD)
    img_s.save(RAW_SECOND, "PNG")

    print("[+] HD 3D İbreler Oluşturuldu.")

if __name__ == "__main__":
    from PIL.ImageFilter import GaussianBlur
    create_textured_background()
    create_hd_hands()
