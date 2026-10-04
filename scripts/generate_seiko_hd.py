import os
import math
from PIL import Image, ImageDraw, ImageFilter

CANVAS_SIZE = (466, 466)
CENTER = (233, 233)
RADIUS = 218

RAW_BG = "assets/raw/bg/seiko_presage_bg.png"
RAW_HOUR = "assets/raw/hands/seiko_hour.png"
RAW_MINUTE = "assets/raw/hands/seiko_minute.png"
RAW_SECOND = "assets/raw/hands/seiko_second.png"

# Renkler (Görseldeki Rose-Gold ve Arka Plan)
AMBER_CENTER = (130, 60, 25, 255)
DARK_EDGE = (15, 6, 4, 255)
ROSE_LIGHT = (245, 195, 170, 255)    # Sol ışıklı yüzey
ROSE_DARK = (150, 95, 70, 255)      # Sağ gölgeli yüzey
TRACK_GOLD = (190, 145, 115, 200)

os.makedirs("assets/raw/bg", exist_ok=True)
os.makedirs("assets/raw/hands", exist_ok=True)

def create_authentic_background():
    img = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 255))
    
    # 1. Sunburst Arka Plan
    sunburst = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    sb_draw = ImageDraw.Draw(sunburst)
    num_rays = 1440
    for i in range(num_rays):
        angle = math.radians(i * (360.0 / num_rays))
        x_end = CENTER[0] + RADIUS * math.sin(angle)
        y_end = CENTER[1] - RADIUS * math.cos(angle)
        intensity = math.sin(i * 0.15) * 0.5 + 0.5
        r_c = int(105 + 45 * intensity)
        g_c = int(48 + 22 * intensity)
        b_c = int(18 + 12 * intensity)
        sb_draw.line([(CENTER[0], CENTER[1]), (x_end, y_end)], fill=(r_c, g_c, b_c, 80), width=1)
    
    # Arka Plan Gradyanı
    radial = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    rad_draw = ImageDraw.Draw(radial)
    for r in range(RADIUS, 0, -1):
        factor = (r / RADIUS) ** 1.8
        r_col = int(AMBER_CENTER[0] * (1 - factor) + DARK_EDGE[0] * factor)
        g_col = int(AMBER_CENTER[1] * (1 - factor) + DARK_EDGE[1] * factor)
        b_col = int(AMBER_CENTER[2] * (1 - factor) + DARK_EDGE[2] * factor)
        rad_draw.ellipse([CENTER[0]-r, CENTER[1]-r, CENTER[0]+r, CENTER[1]+r], fill=(r_col, g_col, b_col, 210))

    img = Image.alpha_composite(img, sunburst)
    img = Image.alpha_composite(img, radial)
    draw = ImageDraw.Draw(img)

    # 2. Dış Dakika Çizgileri
    r_track_out = RADIUS - 6
    for i in range(60):
        ang = math.radians(i * 6)
        sin_a, cos_a = math.sin(ang), math.cos(ang)
        if i % 5 == 0:
            draw.line([(CENTER[0] + (r_track_out - 10) * sin_a, CENTER[1] - (r_track_out - 10) * cos_a),
                       (CENTER[0] + r_track_out * sin_a, CENTER[1] - r_track_out * cos_a)], fill=TRACK_GOLD, width=2)
        else:
            draw.line([(CENTER[0] + (r_track_out - 5) * sin_a, CENTER[1] - (r_track_out - 5) * cos_a),
                       (CENTER[0] + r_track_out * sin_a, CENTER[1] - r_track_out * cos_a)], fill=(150, 110, 85, 140), width=1)

    # 3. GÖRSELDEKİ BİREBİR ÇİFT SİVRİ UÇLU KAMA (CHEVRON ARROWHEAD) İNDEKSİ
    def draw_exact_wedge_index(angle_deg, is_double=False):
        ang = math.radians(angle_deg)
        sin_a, cos_a = math.sin(ang), math.cos(ang)
        
        # Konum Ölçüleri
        r_outer_tip = RADIUS - 22      # En dış sivri çatı ucu
        r_shoulder  = RADIUS - 32      # Geniş olan orta yan omuzlar
        r_inner_tip = RADIUS - 68      # Merkeze bakan uzun sivri uç
        
        width = 11 if not is_double else 8  # Genişlik
        
        # 1. En dış sivri uç (Çatı)
        pt_out = (CENTER[0] + r_outer_tip * sin_a, CENTER[1] - r_outer_tip * cos_a)
        
        # 2. En iç uzun sivri uç (Mızrak ucu)
        pt_in = (CENTER[0] + r_inner_tip * sin_a, CENTER[1] - r_inner_tip * cos_a)
        
        # 3. Sol ve Sağ Geniş Omuz Noktaları
        perp = ang + math.pi/2
        sh_x = CENTER[0] + r_shoulder * sin_a
        sh_y = CENTER[1] - r_shoulder * cos_a
        
        pt_left  = (sh_x + (width/2) * math.cos(perp), sh_y + (width/2) * math.sin(perp))
        pt_right = (sh_x - (width/2) * math.cos(perp), sh_y - (width/2) * math.sin(perp))
        
        # SOL YÜZEY (3 Noktalı Poligon: Dış Uç -> Sol Omuz -> İç Uç)
        draw.polygon([pt_out, pt_left, pt_in], fill=ROSE_LIGHT)
        
        # SAĞ YÜZEY (Gölgeli 3D Yüzey: Dış Uç -> Sağ Omuz -> İç Uç)
        draw.polygon([pt_out, pt_right, pt_in], fill=ROSE_DARK)

    # 12 Saat İndeksini Çiz
    for i in range(12):
        if i == 0:
            # Saat 12 Yönü: Çift İkiz Kama
            draw_exact_wedge_index(355.5, is_double=True)
            draw_exact_wedge_index(4.5, is_double=True)
        elif i == 4:
            continue # Tarih penceresi alanı
        else:
            draw_exact_wedge_index(i * 30)

    # 4. Tarih Penceresi & Logolar
    date_ang = math.radians(135)
    date_r = RADIUS - 58
    dx = CENTER[0] + date_r * math.sin(date_ang)
    dy = CENTER[1] - date_r * math.cos(date_ang)
    
    draw.ellipse([dx-15, dy-15, dx+15, dy+15], fill=(12, 6, 4, 255), outline=ROSE_LIGHT, width=2)
    draw.text((dx, dy), "6", fill=(255, 255, 255, 255), anchor="mm", font_size=15)

    draw.text((CENTER[0], CENTER[1] - 78), "SEIKO", fill=(235, 235, 240, 240), anchor="mm", font_size=23)
    draw.text((CENTER[0], CENTER[1] + 68), "PRESAGE", fill=ROSE_LIGHT, anchor="mm", font_size=13)
    draw.text((CENTER[0], CENTER[1] + 84), "AUTOMATIC", fill=(200, 180, 170, 200), anchor="mm", font_size=9)

    img.save(RAW_BG, "PNG")
    print(f"[+] Birebir Görseldeki Kama İndeksli Kadran Oluşturuldu: {RAW_BG}")

def create_authentic_hands():
    # Dauphine Akrep
    img_h = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw_h = ImageDraw.Draw(img_h)
    draw_h.polygon([(CENTER[0], CENTER[1] - 122), (CENTER[0] - 9, CENTER[1] - 22), (CENTER[0], CENTER[1] + 20)], fill=ROSE_LIGHT)
    draw_h.polygon([(CENTER[0], CENTER[1] - 122), (CENTER[0] + 9, CENTER[1] - 22), (CENTER[0], CENTER[1] + 20)], fill=ROSE_DARK)
    img_h.save(RAW_HOUR, "PNG")

    # Dauphine Yelkovan
    img_m = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw_m = ImageDraw.Draw(img_m)
    draw_m.polygon([(CENTER[0], CENTER[1] - 185), (CENTER[0] - 7, CENTER[1] - 22), (CENTER[0], CENTER[1] + 25)], fill=ROSE_LIGHT)
    draw_m.polygon([(CENTER[0], CENTER[1] - 185), (CENTER[0] + 7, CENTER[1] - 22), (CENTER[0], CENTER[1] + 25)], fill=ROSE_DARK)
    img_m.save(RAW_MINUTE, "PNG")

    # Saniye İbresi
    img_s = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw_s = ImageDraw.Draw(img_s)
    draw_s.line([(CENTER[0], CENTER[1] + 42), (CENTER[0], CENTER[1] - 195)], fill=ROSE_LIGHT, width=2)
    draw_s.ellipse([CENTER[0]-6, CENTER[1]+18, CENTER[0]+6, CENTER[1]+30], outline=ROSE_LIGHT, width=2)
    draw_s.ellipse([CENTER[0]-4, CENTER[1]-4, CENTER[0]+4, CENTER[1]+4], fill=ROSE_LIGHT)
    img_s.save(RAW_SECOND, "PNG")

if __name__ == "__main__":
    create_authentic_background()
    create_authentic_hands()
