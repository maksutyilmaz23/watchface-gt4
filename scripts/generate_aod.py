import os
import math
from PIL import Image, ImageDraw

CANVAS_SIZE = (466, 466)
CENTER = (233, 233)
RADIUS = 220

# AOD için Düşük Parlaklıklı Renk Paleti (Batarya Tasarrufu)
AOD_BG = (0, 0, 0, 255)                  # Tam Siyah Arka Plan
AOD_GOLD = (180, 130, 105, 255)          # Mat Rose Gold
AOD_MUTED = (120, 120, 120, 255)         # Mat Gri Metinler

RAW_AOD_BG = "assets/raw/bg/seiko_aod_bg.png"
RAW_AOD_HOUR = "assets/raw/hands/seiko_aod_hour.png"
RAW_AOD_MINUTE = "assets/raw/hands/seiko_aod_minute.png"

def create_aod_background():
    img = Image.new("RGBA", CANVAS_SIZE, AOD_BG)
    draw = ImageDraw.Draw(img)

    # Dış Çerçeve ve Saat İmleçleri (Sadece Minimal İnce Hatlar)
    for i in range(12):
        angle = math.radians(i * 30)
        r_in = RADIUS - 20
        r_out = RADIUS - 8
        x1 = CENTER[0] + r_in * math.sin(angle)
        y1 = CENTER[1] - r_in * math.cos(angle)
        x2 = CENTER[0] + r_out * math.sin(angle)
        y2 = CENTER[1] - r_out * math.cos(angle)
        draw.line([(x1, y1), (x2, y2)], fill=AOD_GOLD, width=3)

    # 1. Türkçe Tarih & Gün Kutusu (Saat 3 Yönü) -> Örn: "04 EKİ PAZ"
    draw.rectangle([CENTER[0] + 75, CENTER[1] - 18, CENTER[0] + 175, CENTER[1] + 18], outline=AOD_GOLD, width=1)
    draw.text((CENTER[0] + 125, CENTER[1]), "04 EKİ PAZ", fill=AOD_GOLD, anchor="mm", font_size=13)

    # 2. Türkçe Adım Göstergesi (Saat 6 Yönü) -> Örn: "8450 ADIM"
    draw.text((CENTER[0], CENTER[1] + 110), "8450 ADIM", fill=AOD_MUTED, anchor="mm", font_size=14)

    # Logo (Minimal Mat)
    draw.text((CENTER[0], CENTER[1] - 80), "SEIKO", fill=AOD_GOLD, anchor="mm", font_size=18)

    img.save(RAW_AOD_BG, "PNG")
    print(f"[+] AOD Arka planı oluşturuldu: {RAW_AOD_BG}")

def create_aod_hands():
    # AOD Akrep (İçi Boş / İnce Çerçeve)
    img_h = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw_h = ImageDraw.Draw(img_h)
    points_h = [
        (CENTER[0], CENTER[1] - 110),
        (CENTER[0] + 6, CENTER[1] - 20),
        (CENTER[0], CENTER[1] + 15),
        (CENTER[0] - 6, CENTER[1] - 20)
    ]
    draw_h.polygon(points_h, outline=AOD_GOLD, width=2)
    img_h.save(RAW_AOD_HOUR, "PNG")

    # AOD Yelkovan (İçi Boş / İnce Çerçeve)
    img_m = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw_m = ImageDraw.Draw(img_m)
    points_m = [
        (CENTER[0], CENTER[1] - 175),
        (CENTER[0] + 5, CENTER[1] - 20),
        (CENTER[0], CENTER[1] + 20),
        (CENTER[0] - 5, CENTER[1] - 20)
    ]
    draw_m.polygon(points_m, outline=AOD_GOLD, width=2)
    img_m.save(RAW_AOD_MINUTE, "PNG")

    print(f"[+] AOD Akrep & Yelkovan oluşturuldu.")

if __name__ == "__main__":
    create_aod_background()
    create_aod_hands()
