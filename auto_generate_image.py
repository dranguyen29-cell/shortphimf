import os
import sys
import argparse
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Import module ImageGenerator
sys.path.append(os.path.join(os.path.dirname(__file__), "suno_automation"))
from modules.image_generator import ImageGenerator

def run_image_generation(prompt="Warm Rhodes Night Lofi Chill", style_theme="cozy_rain"):
    print("==========================================================================")
    print("🎨 BẮT ĐẦU TỰ ĐỘNG HÓA STAGE 2: GEN ARTWORK / HÌNH NỀN 4K AI CHO VIDEO")
    print("==========================================================================")
    print(f"📝 Chủ đề bài hát: {prompt}")
    print(f"🖌️ Phong cách Visual: Studio Ghibli Anime Lo-Fi Aesthetic (Tỷ lệ 16:9)")
    print("==========================================================================")

    output_dir = os.path.join("suno_automation", "Image")
    gen = ImageGenerator(output_dir=output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = "".join(c if c.isalnum() or c in (' ', '_') else '' for c in prompt)[:25].strip().replace(' ', '_')
    output_filename = f"{safe_title}_{timestamp}.jpg"
    
    # Sinh ảnh mới độc bản
    img_path = gen.generate_lofi_background(prompt=prompt, filename=output_filename)
    
    # Đồng thời cập nhật vào file lofi.jpg mặc định để render video ăn ngay
    default_lofi = os.path.join(output_dir, "lofi.jpg")
    try:
        import shutil
        shutil.copy2(img_path, default_lofi)
        print(f"📌 Đã đồng bộ làm ảnh nền mặc định cho bộ Render Video: {default_lofi}")
    except Exception:
        pass

    print("==========================================================================")
    print(f"🎉 HOÀN TẤT GEN ẢNH NỀN AI CHO BÀI HÁT: '{prompt}'!")
    print(f"🖼️ File ảnh: {img_path}")
    print("==========================================================================")
    return img_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool Gen Ảnh Nền AI 4K Cho Video Lo-Fi YouTube")
    parser.add_argument("--prompt", type=str, default="Warm Rhodes Night - Cozy Rainy Bedroom Lofi", help="Chủ đề hình ảnh")
    args = parser.parse_args()
    run_image_generation(prompt=args.prompt)
