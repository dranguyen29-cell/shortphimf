import os
import requests
import urllib.parse
from datetime import datetime

class ImageGenerator:
    def __init__(self, output_dir="Image"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_lofi_background(self, prompt: str, filename: str = "lofi.jpg") -> str:
        """
        Tự động tạo hình nền Ultra HD 4K dựa trên prompt âm nhạc
        Sử dụng Pollinations AI (Free High-Quality AI Image Generator)
        """
        print(f"🎨 Đang tự động tạo hình nền AI cho prompt: '{prompt}'...")
        
        # Tối ưu hóa prompt nghệ thuật chuẩn YouTube Lo-Fi Masterpiece
        enhanced_prompt = f"Masterpiece anime lofi aesthetic wallpaper, {prompt}, cute anime girl wearing headphones chilling at cozy wooden desk, rainy night window with city bokeh lights, warm glowing amber desk lamp, steaming coffee mug, cozy aesthetic bedroom, studio ghibli art style, 8k resolution, highly detailed, soft warm atmospheric lighting, cinematic composition"
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        
        # URL FLUX AI (Độ phân giải 1920x1080 chuẩn 16:9 sắc nét)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1920&height=1080&model=flux&nologo=true&seed={datetime.now().microsecond}"
        
        output_path = os.path.join(self.output_dir, filename)
        
        try:
            print(f"🎨 Đang gọi FLUX AI Model để vẽ Artwork 16:9 sắc nét cho: '{prompt}'...")
            response = requests.get(image_url, timeout=60)
            if response.status_code == 200 and len(response.content) > 10000:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                size_kb = round(len(response.content) / 1024, 1)
                print(f"✅ ĐÃ TẠO XONG ẢNH NỀN AI THÀNH CÔNG! ({size_kb} KB)")
                print(f"📁 Lưu tại: {output_path}")
                return output_path
            else:
                print(f"⚠️ Không nhận được ảnh từ server (status: {response.status_code})")
                return output_path
        except Exception as e:
            print(f"❌ Lỗi khi tạo ảnh AI: {e}")
            return output_path

if __name__ == "__main__":
    gen = ImageGenerator()
    gen.generate_lofi_background("Midnight Rain & Coffee Lofi Chill")
