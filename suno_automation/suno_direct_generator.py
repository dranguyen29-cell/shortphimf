import os
import sys
import time
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright

def generate_suno_song_live():
    print("==========================================================================")
    print("🚀 KHỞI ĐỘNG SUNO LIVE GENERATOR TRÊN CHROME CỦA DỰ ÁN")
    print("==========================================================================")
    
    profile_dir = os.path.abspath("chrome_profile")
    os.makedirs(profile_dir, exist_ok=True)

    with sync_playwright() as p:
        print("🌐 Đang mở cửa sổ Chrome thực hiện giao diện Suno AI...")
        context = p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            channel="chrome",
            headless=False,
            viewport={"width": 1400, "height": 900},
            args=["--disable-blink-features=AutomationControlled"]
        )

        page = context.pages[0] if context.pages else context.new_page()
        print("🌐 Truy cập https://suno.com/create...")
        page.goto("https://suno.com/create", wait_until="domcontentloaded")
        time.sleep(4)

        print("🔍 Đang tìm các ô Lời bài hát & Phong cách...")

        # 1. Click mở Lời bài hát nếu đang đóng
        lyrics_header = page.query_selector("div:has-text('Lời bài hát'), span:has-text('Lời bài hát'), p:has-text('Lời bài hát')")
        if lyrics_header:
            try:
                lyrics_header.click()
                time.sleep(1)
            except Exception:
                pass

        # 2. Click mở Phong cách nếu đang đóng
        style_header = page.query_selector("div:has-text('Phong cách'), span:has-text('Phong cách'), p:has-text('Phong cách')")
        if style_header:
            try:
                style_header.click()
                time.sleep(1)
            except Exception:
                pass

        # 3. Điền Lời bài hát Lofi Tiếng Việt mới
        new_lyrics = f"""[Verse 1]
Mưa rơi tí tách bên ô cửa nhỏ
Ánh đèn vàng ấm áp góc bàn quen
Ly cà phê thơm nhẹ giữa đêm đen
Bao ưu tư tan theo từng dòng nhạc...

[Chorus]
Oh, midnight rain, wash away the blue
Chỉ còn đêm nay với những ước mơ xa
Tiếng mưa êm đềm như khúc ca
Đưa ta vào giấc ngủ say bình yên...

[Outro]
Tắm mát tâm hồn... Trôi theo tiếng mưa đêm...
"""
        textareas = page.query_selector_all("textarea")
        if len(textareas) >= 1:
            textareas[0].fill(new_lyrics)
            print("✅ Đã tự động điền Lời bài hát Lofi Tiếng Việt mới!")

        if len(textareas) >= 2:
            textareas[1].fill("lofi hip hop, cozy chillhop, female vocal, soft mellow singing, warm rhodes piano, vinyl crackle, gentle boom bap drums, relaxing")
            print("✅ Đã tự động điền Phong cách nhạc Lofi Chill!")

        time.sleep(2)

        # 4. Tìm và bấm nút Tạo
        create_btn = page.query_selector("button:has-text('Tạo'), button:has-text('Create'), button[type='submit']")
        if create_btn and create_btn.is_enabled():
            print("🚀 ĐÃ BẤM NÚT '✨ TẠO' MÀU CAM TRÊN CỬA SỔ CHROME!")
            create_btn.click()
            print("⏳ Suno đang bắt đầu gen 2 bài hát mới...")
            time.sleep(30)
        else:
            print("📌 Nút Tạo đã được điền sẵn trên cửa sổ Chrome!")

        print("==========================================================================")
        print("🎉 HOÀN THÀNH TỰ ĐỘNG ĐIỀN LỜI & BẤM NÚT TẠO TRÊN CHROME!")
        print("==========================================================================")

if __name__ == "__main__":
    generate_suno_song_live()
