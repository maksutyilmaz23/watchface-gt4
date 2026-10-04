import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

# 466x466 Huawei Watch GT4 Standart Çözünürlüğü
CANVAS_SIZE = (466, 466)
CENTER = (233, 233)
RADIUS = 218

# Çıktı Yolları
RAW_BG = "assets/raw/bg/seiko_presage_bg.png"
RAW_HOUR = "assets/raw/hands/seiko_hour.png"
RAW_MINUTE = "assets/raw/hands/seiko_minute.png"
RAW_SECOND = "assets/raw/hands/seiko_second.png"

# Orijinal Fotoğraf Renk Paleti
ROSE_GOLD_LIGHT = (248, 198, 172, 255)  # Işık alan rose-gold
ROSE_GOLD_DARK  = (148, 92, 68, 255)    # Gölgeli rose-gold
SILVER_LOGO     = (238, 238, 242, 245)  # SEIKO kabarık gümüş logo
AMBER_CENTER    = (138, 62, 28, 255)    # Arka plan açık amber kahve
DARK_EDGE       = (16, 7, 5, 255)       # Arka plan kenar siyah/kahve

os.makedirs("assets/raw/bg", exist_ok=True)
os.makedirs("assets/raw/hands", exist_ok=True)

def generate_premium_background():
    SCALE = 4
    SW, SH = CANVAS_SIZE[0] * SCALE, CANVAS_SIZE[1] * SCALE
    SCENTER = (CENTER[0] * SCALE, CENTER[1] * SCALE)
    SRADIUS = RADIUS * SCALE

    img = Image.new("RGBA", (SW, SH), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    # Arka Plan Gradyanı (Amber - Siyah Kahve)
    for r in range(SRADIUS, 0, -1):
        f = (r / SRADIUS) ** 1.6
        r_c = int(AMBER_CENTER[0] * (1 - f) + DARK_EDGE[0] * f)
        g_c = int(AMBER_CENTER[1] * (1 - f) + DARK_EDGE[1] * f)
        b_c = int(AMBER_CENTER[2] * (1 - f) + DARK_EDGE[2] * f)
        draw.ellipse([SCENTER[0]-r, SCENTER[1]-r, SCENTER[0]+r, SCENTER[1]+r], fill=(r_c, g_c, b_c, 255))

    # Organic Cocktail Sunburst Dokusu
    random.seed(101)
    texture = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(texture)
    for _ in range(8000):
        ang = random.uniform(0, 2 * math.pi)
        dist = random.uniform(0, SRADIUS - 20)
        x1 = SCENTER[0] + dist * math.cos(ang)
        y1 = SCENTER[1] + dist * math.sin(ang)
        l = random.uniform(20, 80)
        x2 = x1 + l * math.cos(ang + random.uniform(-0.3, 0.3))
        y2 = y1 + l * math.sin(ang + random.uniform(-0.3, 0.3))
        alpha = int(random.uniform(10, 45) * (1 - (dist / SRADIUS)**2))
        t_draw.line([(x1, y1), (x2, y2)], fill=(220, 140, 95, alpha), width=2)
    
    texture = texture.filter(ImageFilter.GaussianBlur(2 * SCALE))
    img = Image.alpha_composite(img, texture)
    draw = ImageDraw.Draw(img)

    # 2. Dış Dairesel Dakika Çizgileri
    r_track_out = SRADIUS - (8 * SCALE)
    for i in range(60):
        ang = math.radians(i * 6)
        sin_a, cos_a = math.sin(ang), math.cos(ang)
        if i % 5 == 0:
            x1 = SCENTER[0] + (r_track_out - (12 * SCALE)) * sin_a
            y1 = SCENTER[1] - (r_track_out - (12 * SCALE)) * cos_a
            x2 = SCENTER[0] + r_track_out * sin_a
            y2 = SCENTER[1] - r_track_out * cos_a
            draw.line([(x1, y1), (x2, y2)], fill=ROSE_GOLD_LIGHT, width=2*SCALE)
        else:
            x1 = SCENTER[0] + (r_track_out - (6 * SCALE)) * sin_a
            y1 = SCENTER[1] - (r_track_out - (6 * SCALE)) * cos_a
            x2 = SCENTER[0] + r_track_out * sin_a
            y2 = SCENTER[1] - r_track_out * cos_a
            draw.line([(x1, y1), (x2, y2)], fill=(160, 115, 90, 180), width=1*SCALE)

    # 3. 3D Kama İndeksler
    def draw_wedge(angle_deg, is_double=False):
        ang = math.radians(angle_deg)
        sin_a, cos_a = math.sin(ang), math.cos(ang)

        r_out = SRADIUS - (22 * SCALE)
        r_sh  = SRADIUS - (32 * SCALE)
        r_in  = SRADIUS - (68 * SCALE)
        w = (11 if not is_double else 8) * SCALE

        pt_out = (SCENTER[0] + r_out * sin_a, SCENTER[1] - r_out * cos_a)
        pt_in  = (SCENTER[0] + r_in * sin_a, SCENTER[1] - r_in * cos_a)

        perp = ang + math.pi/2
        sh_x = SCENTER[0] + r_sh * sin_a
        sh_y = SCENTER[1] - r_sh * cos_a

        pt_left  = (sh_x + (w/2) * math.cos(perp), sh_y + (w/2) * math.sin(perp))
        pt_right = (sh_x - (w/2) * math.cos(perp), sh_y - (w/2) * math.sin(perp))

        draw.polygon([pt_out, pt_left, pt_in], fill=ROSE_GOLD_LIGHT)
        draw.polygon([pt_out, pt_right, pt_in], fill=ROSE_GOLD_DARK)

    for i in range(12):
        if i == 0:
            draw_wedge(355.5, is_double=True)
            draw_wedge(4.5, is_double=True)
        elif i == 4:
            continue
        else:
            draw_wedge(i * 30)

    # 4. Tarih Penceresi & Logolar
    date_ang = math.radians(135)
    date_r = SRADIUS - (58 * SCALE)
    dx = SCENTER[0] + date_r * math.sin(date_ang)
    dy = SCENTER[1] - date_r * math.cos(date_ang)

    draw.ellipse([dx-(16*SCALE), dy-(16*SCALE), dx+(16*SCALE), dy+(16*SCALE)], fill=(12, 6, 4, 255), outline=ROSE_GOLD_LIGHT, width=2*SCALE)

    img = img.resize(CANVAS_SIZE, Image.LANCZOS)

    draw_final = ImageDraw.Draw(img)
    draw_final.text((dx/SCALE, dy/SCALE), "6", fill=(255, 255, 255, 255), anchor="mm", font_size=15)
    draw_final.text((CENTER[0], CENTER[1] - 78), "SEIKO", fill=SILVER_LOGO, anchor="mm", font_size=23)
    draw_final.text((CENTER[0], CENTER[1] + 68), "PRESAGE", fill=ROSE_GOLD_LIGHT, anchor="mm", font_size=13)
    draw_final.text((CENTER[0], CENTER[1] + 84), "AUTOMATIC", fill=(200, 180, 170, 200), anchor="mm", font_size=9)
    draw_final.text((CENTER[0], CENTER[1] + 175), "JAPAN 4R35...", fill=(150, 120, 100, 160), anchor="mm", font_size=7)

    img.save(RAW_BG, "PNG")
    print(f"[+] Premium Arka Plan & Kama Çizgileri Oluşturuldu: {RAW_BG}")

def generate_premium_hands():
    # Dauphine Akrep
    img_h = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw_h = ImageDraw.Draw(img_h)
    draw_h.polygon([(CENTER[0], CENTER[1] - 122), (CENTER[0] - 9, CENTER[1] - 22), (CENTER[0], CENTER[1] + 20)], fill=ROSE_GOLD_LIGHT)
    draw_h.polygon([(CENTER[0], CENTER[1] - 122), (CENTER[0] + 9, CENTER[1] - 22), (CENTER[0], CENTER[1] + 20)], fill=ROSE_GOLD_DARK)
    img_h.save(RAW_HOUR, "PNG")

    # Dauphine Yelkovan (NameError Düzeltildi)
    img_m = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw_m = ImageDraw.Draw(img_m)
    draw_m.polygon([(CENTER[0], CENTER[1] - 185), (CENTER[0] - 7, CENTER[1] - 22), (CENTER[0], CENTER[1] + 25)], fill=ROSE_GOLD_LIGHT)
    draw_m.polygon([(CENTER[0], CENTER[1] - 185), (CENTER[0] + 7, CENTER[1] - 22), (CENTER[0], CENTER[1] + 25)], fill=ROSE_GOLD_DARK)
    img_m.save(RAW_MINUTE, "PNG")

    # Saniye İbresi
    img_s = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw_s = ImageDraw.Draw(img_s)
    draw_s.line([(CENTER[0], CENTER[1] + 42), (CENTER[0], CENTER[1] - 195)], fill=ROSE_GOLD_LIGHT, width=2)
    draw_s.ellipse([CENTER[0]-6, CENTER[1]+18, CENTER[0]+6, CENTER[1]+30], outline=ROSE_GOLD_LIGHT, width=2)
    draw_s.ellipse([CENTER[0]-4, CENTER[1]-4, CENTER[0]+4, CENTER[1]+4], fill=ROSE_GOLD_LIGHT)
    img_s.save(RAW_SECOND, "PNG")

    print("[+] Premium 3D İbreler Sorunsuz Oluşturuldu.")

if __name__ == "__main__":
    generate_premium_background()
    generate_premium_hands()
