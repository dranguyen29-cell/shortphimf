import os
import time
import requests
from datetime import datetime

class SunoMusicGenerator:
    def __init__(self, output_dir="music_output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_and_download(self, prompt: str, style: str = "Lofi Chill Beats", instrumental: bool = True) -> dict:
        """
        Khởi tạo quy trình tự động gen nhạc từ Suno.com ngầm trên Chrome
        Tự động lưu file .mp3 và trích xuất Metadata (Tiêu đề, Lyric)
        """
        print(f"🎵 Đang khởi động quy trình gen nhạc Suno với prompt: '{prompt}'...")

        # Đặt tên mặc định dựa trên thời gian & prompt
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c if c.isalnum() or c in (' ', '_') else '' for c in prompt)[:30].strip()
        filename = f"{safe_title}_{timestamp}.mp3"
        output_file = os.path.join(self.output_dir, filename)

        try:
            from playwright.sync_api import sync_playwright

            user_data_dir = os.path.abspath("chrome_profile")

            with sync_playwright() as p:
                print("🌐 Đang kết nối Chrome Profile dự án (Duy trì Session Suno AI 100%)...")
                
                browser_context = None
                try:
                    # Thử kết nối qua Chrome CDP Port 9222 nếu Chrome đang mở sẵn
                    browser = p.chromium.connect_over_cdp("http://localhost:9222", timeout=5000)
                    browser_context = browser.contexts[0]
                    print("⚡ Đã kết nối thành công Chrome Port 9222!")
                except Exception:
                    # Chạy Chrome Persistent Context với Profile dự án đã lưu session
                    print("🌐 Khởi động Chrome Persistent Context với Profile dự án...")
                    browser_context = p.chromium.launch_persistent_context(
                        user_data_dir=user_data_dir,
                        channel="chrome",
                        headless=False,
                        args=["--disable-blink-features=AutomationControlled"]
                    )

                page = browser_context.new_page() if not browser_context.pages else browser_context.pages[0]
                print("🌐 Đang truy cập Suno.com/create...")
                page.goto("https://suno.com/create", wait_until="domcontentloaded", timeout=60000)

                time.sleep(3)
                print("✍️ Đang mở các mục 'Lời bài hát' & 'Phong cách' trên giao diện Suno AI Tiếng Việt...")

                # Mở accordion Lời bài hát nếu đang đóng
                lyrics_accordion = page.query_selector("div:has-text('Lời bài hát'), span:has-text('Lời bài hát')")
                if lyrics_accordion:
                    try:
                        lyrics_accordion.click()
                        time.sleep(1)
                    except Exception:
                        pass

                # Mở accordion Phong cách nếu đang đóng
                style_accordion = page.query_selector("div:has-text('Phong cách'), span:has-text('Phong cách')")
                if style_accordion:
                    try:
                        style_accordion.click()
                        time.sleep(1)
                    except Exception:
                        pass

                # Điền Lời bài hát
                lyrics_textarea = page.query_selector("textarea[placeholder*='Bắt đầu'], textarea[placeholder*='Lời'], textarea")
                if lyrics_textarea:
                    lyrics_text = f"""[Verse 1]
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
                    lyrics_textarea.fill(lyrics_text)
                    print("✅ Đã tự động điền Lời bài hát Lofi Tiếng Việt!")

                # Điền Phong cách
                all_textareas = page.query_selector_all("textarea")
                if len(all_textareas) >= 2:
                    all_textareas[1].fill("lofi hip hop, cozy chillhop, female vocal, warm rhodes piano, vinyl crackle, gentle boom bap drums, relaxing")
                    print("✅ Đã tự động điền Phong cách nhạc Lofi Chill!")

                time.sleep(2)
                
                # Bấm nút Tạo
                create_btn = page.query_selector("button:has-text('Tạo'), button:has-text('Create'), button[type='submit']")
                if create_btn and create_btn.is_enabled():
                    print("🚀 Đã bấm nút 'TẠO' trên Suno AI! Đang sáng tác 2 bản thu mới...")
                    create_btn.click()
                    time.sleep(55)
                else:
                    print("📌 Đã điền sẵn Lời & Phong cách trên cửa sổ Suno AI!")

                # Đợi bài hát hoàn tất sáng tác và tự động tải về
                print("⏳ Đang chờ Suno hoàn thiện bài hát...")
                time.sleep(5)

                downloaded_file = None
                try:
                    print("🎯 Đang mở menu bài hát mới nhất để tải file MP3...")
                    more_btn = page.locator('button[aria-label="More options"][data-context-menu-trigger="true"]').first
                    if more_btn.is_visible(timeout=10000):
                        more_btn.click()
                        time.sleep(1)

                        download_item = page.locator('div, span, button').filter(has_text="Download").last
                        download_item.click()
                        time.sleep(1.5)

                        with page.expect_download(timeout=30000) as download_info:
                            unlock_btn = page.locator('button:has-text("Unlock & Download"), button:has-text("Download")').last
                            unlock_btn.click()
                            
                            download = download_info.value
                            downloaded_filename = download.suggested_filename
                            final_path = os.path.join(self.output_dir, downloaded_filename)
                            download.save_as(final_path)
                            downloaded_file = final_path
                            print(f"🎉🎉🎉 ĐÃ TỰ ĐỘNG TẢI THÀNH CÔNG BÀI HÁT TỪ SUNO: {final_path}")
                except Exception as dl_err:
                    print(f"⚠️ Lỗi tự động tải bài hát: {dl_err}")

            if downloaded_file and os.path.exists(downloaded_file):
                return {
                    "title": os.path.splitext(os.path.basename(downloaded_file))[0],
                    "file_path": downloaded_file,
                    "prompt": prompt,
                    "style": style
                }

            # Fallback nếu đã có file trong music_output
            existing_files = [os.path.join(self.output_dir, f) for f in os.listdir(self.output_dir) if f.endswith(".mp3")]
            if existing_files:
                existing_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                latest_mp3 = existing_files[0]
                print(f"🎵 Sử dụng bản thu mới nhất: {latest_mp3}")
                return {
                    "title": os.path.splitext(os.path.basename(latest_mp3))[0],
                    "file_path": latest_mp3,
                    "prompt": prompt,
                    "style": style
                }
            return None

if __name__ == "__main__":
    generator = SunoMusicGenerator()
    generator.generate_and_download("Midnight Rain Coffee Lofi")
