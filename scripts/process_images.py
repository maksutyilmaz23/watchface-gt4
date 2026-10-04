import os
from PIL import Image

RAW_DIR = "assets/raw"
PROCESSED_DIR = "assets/processed"
TARGET_CANVAS = (466, 466)
MAX_BG_BYTES = 750 * 1024

def process_backgrounds():
    bg_raw = os.path.join(RAW_DIR, "bg")
    bg_out = os.path.join(PROCESSED_DIR, "bg")
    os.makedirs(bg_raw, exist_ok=True)
    os.makedirs(bg_out, exist_ok=True)

    for f in os.listdir(bg_raw):
        if f.lower().endswith(('.png', '.jpg', '.jpeg')):
            in_path = os.path.join(bg_raw, f)
            out_path = os.path.join(bg_out, os.path.splitext(f)[0] + ".png")
            
            with Image.open(in_path) as img:
                img = img.convert("RGBA")
                img = img.resize(TARGET_CANVAS, Image.Resampling.LANCZOS)
                img.save(out_path, "PNG", optimize=True)
                
            size = os.path.getsize(out_path)
            status = "OK" if size <= MAX_BG_BYTES else "UYARI (>750KB)"
            print(f"[BG] {f} -> {out_path} [{size / 1024:.1f} KB] - {status}")

def process_hands():
    hands_raw = os.path.join(RAW_DIR, "hands")
    hands_out = os.path.join(PROCESSED_DIR, "hands")
    os.makedirs(hands_raw, exist_ok=True)
    os.makedirs(hands_out, exist_ok=True)

    for f in os.listdir(hands_raw):
        if f.lower().endswith('.png'):
            in_path = os.path.join(hands_raw, f)
            out_path = os.path.join(hands_out, f)
            
            with Image.open(in_path) as img:
                img = img.convert("RGBA")
                canvas = Image.new("RGBA", TARGET_CANVAS, (0, 0, 0, 0))
                paste_x = (466 - img.width) // 2
                paste_y = (466 - img.height) // 2
                canvas.paste(img, (paste_x, paste_y), img)
                canvas.save(out_path, "PNG", optimize=True)
                
            print(f"[HAND] {f} -> Merkezlendi (233, 233)")

def process_digits():
    num_raw = os.path.join(RAW_DIR, "digital_num")
    num_out = os.path.join(PROCESSED_DIR, "digital_num")
    os.makedirs(num_raw, exist_ok=True)
    os.makedirs(num_out, exist_ok=True)

    for f in os.listdir(num_raw):
        if f.lower().endswith('.png'):
            in_path = os.path.join(num_raw, f)
            out_path = os.path.join(num_out, f)
            
            with Image.open(in_path) as img:
                img = img.convert("RGBA")
                img.save(out_path, "PNG", optimize=True)
            print(f"[DIGIT] {f} optimize edildi.")

if __name__ == "__main__":
    print("=== GT4 Varlık İşleyici Başlatıldı ===")
    process_backgrounds()
    process_hands()
    process_digits()
    print("=== Tüm İşlemler Tamamlandı ===")
