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

# Otantik Seiko Rose Gold ve Kadran Renk Paleti
AMBER_CENTER = (135, 65, 30, 255)       # Kadran merkezi karamel kahve
DARK_EDGE = (18, 8, 5, 255)            # Dış kenar siyahımsı koyu kahve
ROSE_LIGHT = (238, 185, 155, 255)       # İndekslerin ışık alan tarafı
ROSE_DARK = (145, 90, 65, 255)          # İndekslerin gölgeli tarafı
TRACK_GOLD = (200, 155, 125, 220)       # Dış dakika çizgileri
SILVER_TEXT = (235, 235, 240, 240)      # SEIKO logosu

os.makedirs("assets/raw/bg", exist_ok=True)
os.makedirs("assets/raw/hands", exist_ok=True)

def create_authentic_background():
    img = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 255))
    
    # 1. GERÇEK SUNBURST (IŞINSAL MİKRORAY) DOKUSU (360 DERECE 1440 IŞIN)
    sunburst = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    sb_draw = ImageDraw.Draw(sunburst)
    
    num_rays = 1440  # Çeyrek derecelik hassas ışınlar
    for i in range(num_rays):
        angle = math.radians(i * (360.0 / num_rays))
        x_end = CENTER[0] + RADIUS * math.sin(angle)
        y_end = CENTER[1] - RADIUS * math.cos(angle)
        
        # Işık-gölge dalgalanması (Güneş ışını efekti)
        intensity = math.sin(i * 0.15) * 0.5 + 0.5
        r_c = int(110 + 40 * intensity)
        g_c = int(50 + 20 * intensity)
        b_c = int(20 + 10 * intensity)
        alpha = int(40 + 50 * intensity)
        
        sb_draw.line([(CENTER[0], CENTER[1]), (x_end, y_end)], fill=(r_c, g_c, b_c, alpha), width=1)
    
    # 2. RADYAL AMBER / DERİN KAHVE DERECELİ MASKE
    radial = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    rad_draw = ImageDraw.Draw(radial)
    for r in range(RADIUS, 0, -1):
        factor = (r / RADIUS) ** 1.8  # Kenarlara doğru ivmeli koyulaşma
        r_col = int(AMBER_CENTER[0] * (1 - factor) + DARK_EDGE[0] * factor)
        g_col = int(AMBER_CENTER[1] * (1 - factor) + DARK_EDGE[1] * factor)
        b_col = int(AMBER_CENTER[2] * (1 - factor) + DARK_EDGE[2] * factor)
        rad_draw.ellipse([CENTER[0]-r, CENTER[1]-r, CENTER[0]+r, CENTER[1]+r], fill=(r_col, g_col, b_col, 210))

    img = Image.alpha_composite(img, sunburst)
    img = Image.alpha_composite(img, radial)
    draw = ImageDraw.Draw(img)

    # 3. DIŞ DAKİKA/SANİYE ÇİZGİLERİ (OUTER TRACK)
    r_track_out = RADIUS - 8
    r_track_in = RADIUS - 18
    for i in range(60):
        ang = math.radians(i * 6)
        sin_a, cos_a = math.sin(ang), math.cos(ang)
        if i % 5 == 0:
            x1 = CENTER[0] + (r_track_out - 10) * sin_a
            y1 = CENTER[1] - (r_track_out - 10) * cos_a
            x2 = CENTER[0] + r_track_out * sin_a
            y2 = CENTER[1] - r_track_out * cos_a
            draw.line([(x1, y1), (x2, y2)], fill=TRACK_GOLD, width=2)
        else:
            x1 = CENTER[0] + (r_track_out - 5) * sin_a
            y1 = CENTER[1] - (r_track_out - 5) * cos_a
            x2 = CENTER[0] + r_track_out * sin_a
            y2 = CENTER[1] - r_track_out * cos_a
            draw.line([(x1, y1), (x2, y2)], fill=(160, 120, 95, 160), width=1)

    # 4. PRİZMATİK 3D ELMAS KESİM (FACETED) İNDEKS ÇİZİMİ
    def draw_faceted_index(angle_deg, is_double=False):
        ang = math.radians(angle_deg)
        sin_a, cos_a = math.sin(ang), math.cos(ang)
        
        r_out = RADIUS - 22
        r_in = RADIUS - 62
        width = 10 if not is_double else 8
        
        # Nokta hesaplamaları (Prizmatik Ok Başı)
        pt_out = (CENTER[0] + r_out * sin_a, CENTER[1] - r_out * cos_a)
        pt_in = (CENTER[0] + r_in * sin_a, CENTER[1] - r_in * cos_a)
        
        perp = ang + math.pi/2
        mid_r = r_in + (r_out - r_in) * 0.65
        mid_x = CENTER[0] + mid_r * sin_a
        mid_y = CENTER[1] - mid_r * cos_a
        
        pt_left = (mid_x + (width/2) * math.cos(perp), mid_y + (width/2) * math.sin(perp))
        pt_right = (mid_x - (width/2) * math.cos(perp), mid_y - (width/2) * math.sin(perp))
        
        # Sol yüzey (İşık Alan Parfaj)
        draw.polygon([pt_out, pt_left, pt_in], fill=ROSE_LIGHT)
        # Sağ yüzey (Gölgede Kalan Parfaj - 3D Efekti)
        draw.polygon([pt_out, pt_right, pt_in], fill=ROSE_DARK)

    # 12 Saat İndekslerini Yerleştir
    for i in range(12):
        if i == 0:
            # 12 Yönü: Çift İkiz Kama (V İndeks)
            draw_faceted_index(355.5, is_double=True)
            draw_faceted_index(4.5, is_double=True)
        elif i == 4:
            # Saat 4:30 civarındaki tarih çerçevesine yer aç
            continue
        else:
            draw_faceted_index(i * 30)

    # 5. SAAT 4.5 YÖNÜ TARİH PENCERESİ VE TİPOGRAFİ
    date_ang = math.radians(135)
    date_r = RADIUS - 58
    dx = CENTER[0] + date_r * math.sin(date_ang)
    dy = CENTER[1] - date_r * math.cos(date_ang)
    
    # Metal çerçeveli tarih halkası
    draw.ellipse([dx-16, dy-16, dx+16, dy+16], fill=(12, 6, 4, 255), outline=ROSE_LIGHT, width=2)
    draw.text((dx, dy), "6", fill=(255, 255, 255, 255), anchor="mm", font_size=15)

    # Tipografi
    draw.text((CENTER[0], CENTER[1] - 78), "SEIKO", fill=SILVER_TEXT, anchor="mm", font_size=23)
    draw.text((CENTER[0], CENTER[1] + 68), "PRESAGE", fill=ROSE_LIGHT, anchor="mm", font_size=13)
    draw.text((CENTER[0], CENTER[1] + 84), "AUTOMATIC", fill=(210, 190, 180, 210), anchor="mm", font_size=9)

    img.save(RAW_BG, "PNG")
    print(f"[+] Gerçek Sunburst & 3D İndeks Arka Planı Üretildi: {RAW_BG}")

def create_authentic_hands():
    # 3D Keskin Dauphine Akrep
    img_h = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw_h = ImageDraw.Draw(img_h)
    draw_h.polygon([(CENTER[0], CENTER[1] - 122), (CENTER[0] - 9, CENTER[1] - 22), (CENTER[0], CENTER[1] + 20)], fill=ROSE_LIGHT)
    draw_h.polygon([(CENTER[0], CENTER[1] - 122), (CENTER[0] + 9, CENTER[1] - 22), (CENTER[0], CENTER[1] + 20)], fill=ROSE_DARK)
    img_h.save(RAW_HOUR, "PNG")

    # 3D Keskin Dauphine Yelkovan
    img_m = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw_m = ImageDraw.Draw(img_m)
    draw_m.polygon([(CENTER[0], CENTER[1] - 185), (CENTER[0] - 7, CENTER[1] - 22), (CENTER[0], CENTER[1] + 25)], fill=ROSE_LIGHT)
    draw_m.polygon([(CENTER[0], CENTER[1] - 185), (CENTER[0] + 7, CENTER[1] - 22), (CENTER[0], CENTER[1] + 25)], fill=ROSE_DARK)
    img_m.save(RAW_MINUTE, "PNG")

    # Saniye İbresi ve Dairesel İkiz Karşı Ağırlık
    img_s = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw_s = ImageDraw.Draw(img_s)
    draw_s.line([(CENTER[0], CENTER[1] + 42), (CENTER[0], CENTER[1] - 195)], fill=ROSE_LIGHT, width=2)
    draw_s.ellipse([CENTER[0]-6, CENTER[1]+18, CENTER[0]+6, CENTER[1]+30], outline=ROSE_LIGHT, width=2)
    draw_s.ellipse([CENTER[0]-4, CENTER[1]-4, CENTER[0]+4, CENTER[1]+4], fill=ROSE_LIGHT)
    img_s.save(RAW_SECOND, "PNG")

    print("[+] Otantik 3D İbreler Oluşturuldu.")

if __name__ == "__main__":
    create_authentic_background()
    create_authentic_hands()
