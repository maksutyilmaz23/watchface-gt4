from PIL import Image

# Katmanları Yükle
bg = Image.open("assets/processed/bg/seiko_presage_bg.png").convert("RGBA")
hour = Image.open("assets/processed/hands/seiko_hour.png").convert("RGBA")
minute = Image.open("assets/processed/hands/seiko_minute.png").convert("RGBA")
second = Image.open("assets/processed/hands/seiko_second.png").convert("RGBA")

# Katmanları Üst Üste Bindir (Saat 10:08 Pozisyonu)
preview = Image.alpha_composite(bg, hour)
preview = Image.alpha_composite(preview, minute)
preview = Image.alpha_composite(preview, second)

# Önizleme Görselini Kaydet
preview.save("assets/processed/preview.png")
print("[+] Önizleme görseli oluşturuldu: assets/processed/preview.png")
