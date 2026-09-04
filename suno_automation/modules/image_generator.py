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
        
        # Tự động tối ưu hóa prompt cho phong cách Lofi Aesthetic 8K Masterpiece
        enhanced_prompt = f"Masterpiece anime lofi aesthetic wallpaper, {prompt}, cozy room at rainy night, glowing amber desk lamp, steam from coffee cup, rain drops on window glass with blurred city bokeh lights, 8k resolution, ultra detailed, studio ghibli vibe, rich vibrant colors"
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        
        # URL dịch vụ Pollinations AI dùng Model FLUX (Ultra Quality 1920x1080)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1920&height=1080&model=flux&nologo=true&enhance=true"
        
        output_path = os.path.join(self.output_dir, filename)
        
        try:
            # Kiểm tra nếu có bức ảnh Masterpiece Ultra HD 4K (lofi_4k_ultra) thì dùng cố định
            masterpiece_img = os.path.join(self.output_dir, "lofi_4k_ultra_1788172511456.jpg")
            if os.path.exists(masterpiece_img):
                import shutil
                shutil.copy(masterpiece_img, output_path)
                print(f"✅ Đã sử dụng ảnh Masterpiece Ultra HD 4K cố định: {output_path}")
                return output_path
            
            response = requests.get(image_url, timeout=30)
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Đã tạo & tải ảnh nền AI thành công: {output_path}")
                return output_path
            else:
                return output_path
        except Exception as e:
            print(f"❌ Lỗi khi tạo ảnh AI: {e}")
            return output_path

if __name__ == "__main__":
    gen = ImageGenerator()
    gen.generate_lofi_background("Midnight Rain & Coffee Lofi Chill")
