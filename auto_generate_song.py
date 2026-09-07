import os
import sys
import time
import glob
import argparse
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright

def clean_locks(profile_dir):
    """Dọn dẹp lock file và process cũ nếu có"""
    cmd = 'wmic process where "name=\'chrome.exe\' and commandline like \'%chrome_profile%\'" call terminate'
    subprocess.run(cmd, shell=True, capture_output=True)
    for f in glob.glob(os.path.join(profile_dir, "*lock*")) + glob.glob(os.path.join(profile_dir, "Singleton*")):
        try:
            os.remove(f)
        except Exception:
            pass

def auto_generate_and_download_song(lyrics=None, style=None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    profile_dir = os.path.join(current_dir, "suno_automation", "chrome_profile")
    output_dir = os.path.join(current_dir, "suno_automation", "music_output")
    os.makedirs(profile_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    clean_locks(profile_dir)

    default_lyrics = """[Verse 1]
Gió đông về khẽ lùa qua song cửa
Khói ly cà phê nghi ngút bốc lên
Một thoáng bình yên giữa ngày vội vã
Ngồi lại đây nghe tiếng nhạc êm đềm

[Chorus]
Hương cà phê ấm nồng mùa đông
Gửi trọn yêu thương vào khoảng trời rộng
Giai điệu lofi ru từng nỗi nhớ
Cho ta tìm về những giấc mơ xưa

[Outro]
Mùa đông ấm áp... Giữ mãi trong tim..."""

    default_style = "lofi hip hop, cozy winter chillhop, soft acoustic guitar, mellow electric piano, warm rhodes, vinyl crackle, relaxing gentle drums, 75 bpm"

    song_lyrics = lyrics or default_lyrics
    song_style = style or default_style

    print("==========================================================================")
    print("🚀 BẮT ĐẦU QUY TRÌNH TỰ ĐỘNG HÓA 1-CLICK: TẠO NHẠC SUNO & TỰ TẢI MP3 VỀ")
    print("==========================================================================")
    print(f"📝 Lời bài hát:\n{song_lyrics.strip()}")
    print("--------------------------------------------------------------------------")
    print(f"🎼 Phong cách nhạc: {song_style}")
    print("==========================================================================")
    
    downloaded_file = None

    with sync_playwright() as p:
        print("🌐 [1/5] Đang khởi động Google Chrome với tài khoản draminkute...")
        context = p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            channel="chrome",
            headless=False,
            no_viewport=True,
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled"
            ]
        )

        page = context.pages[0] if context.pages else context.new_page()
        page.bring_to_front()

        print("🌐 [2/5] Đang truy cập Suno Create: https://suno.com/create?wid=default...")
        page.goto("https://suno.com/create?wid=default", wait_until="domcontentloaded", timeout=60000)
        time.sleep(3)

        # 1. Điền Lời bài hát
        print("✍️ [3/5] Đang điền LỜI BÀI HÁT TIẾNG VIỆT vào ô Lyrics...")
        lyrics_filled = False
        try:
            lyrics_box = page.locator("textarea").first
            if lyrics_box.is_visible(timeout=5000):
                lyrics_box.fill(song_lyrics)
                lyrics_filled = True
                print("✅ Đã điền Lời bài hát thành công bằng Playwright!")
        except Exception as e:
            print(f"⚠️ Thử fill lyrics: {e}")

        if not lyrics_filled:
            escaped_lyrics = song_lyrics.replace("`", "\\`").replace('"', '\\"').replace("\n", "\\n")
            page.evaluate(f"""(() => {{
                const ta = document.querySelector("textarea");
                if (ta) {{
                    const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
                    setter.call(ta, "{escaped_lyrics}");
                    ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    ta.style.border = '3px solid #22c55e';
                }}
            }})()""")
            print("✅ Đã điền Lời bài hát bằng DOM Injection!")

        time.sleep(1)

        # 2. Mở Styles và điền Phong cách nhạc
        print("✍️ Đang mở mục Styles và điền PHONG CÁCH NHẠC...")
        try:
            style_header = page.locator("div, span, button").filter(has_text="Styles").first
            if style_header.is_visible(timeout=3000):
                style_header.click()
                time.sleep(0.5)
        except Exception:
            pass

        try:
            all_textareas = page.locator("textarea").all()
            if len(all_textareas) > 1:
                all_textareas[1].fill(song_style)
                print("✅ Đã điền Phong cách nhạc thành công bằng Playwright!")
            else:
                escaped_style = song_style.replace("`", "\\`").replace('"', '\\"')
                page.evaluate(f"""(() => {{
                    const tas = document.querySelectorAll("textarea");
                    const st = tas.length > 1 ? tas[1] : document.querySelector("textarea[placeholder*='style']");
                    if (st) {{
                        const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
                        setter.call(st, "{escaped_style}");
                        st.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        st.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        st.style.border = '3px solid #22c55e';
                    }}
                }})()""")
                print("✅ Đã điền Phong cách nhạc bằng DOM Injection!")
        except Exception as e:
            print(f"⚠️ Điền style: {e}")

        time.sleep(1)

        # 3. Kích hoạt nút Create màu cam
        print("🚀 [4/5] Đang bấm nút ✨ Create để bắt đầu tạo bài hát mới...")
        try:
            create_btn = page.locator("button").filter(has_text="Create").first
            if create_btn.is_visible(timeout=3000):
                create_btn.click()
                print("🎉 ĐÃ BẤM NÚT CREATE THÀNH CÔNG!")
            else:
                page.evaluate("""(() => {
                    const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Create' || b.textContent.includes('Create'));
                    if (btn) btn.click();
                })()""")
                print("🎉 ĐÃ BẤM NÚT CREATE BẰNG DOM INJECTION!")
        except Exception as e:
            print(f"⚠️ Bấm create: {e}")

        # 4. Chờ Suno sáng tác xong (~50-60 giây)
        print("==========================================================================")
        print("⏳ [5/5] Đang chờ Suno hoàn tất quá trình sáng tác nhạc (khoảng 50-60 giây)...")
        print("==========================================================================")
        
        for remaining in range(55, 0, -10):
            print(f"⏱️ Còn khoảng {remaining} giây nữa...")
            time.sleep(10)

        # Thêm 5 giây ổn định
        time.sleep(5)

        # 5. Tự động tải file MP3 bài mới nhất
        print("📥 BẮT ĐẦU TỰ ĐỘNG TẢI FILE MP3 BẢN THU MỚI VỀ MÁY...")
        try:
            # Tìm nút More options của bài hát đầu tiên
            more_btn = page.locator('button[aria-label="More options"][data-context-menu-trigger="true"]').first
            if more_btn.is_visible(timeout=10000):
                more_btn.click()
                print("🎯 Đã mở Menu bài hát mới nhất!")
                time.sleep(1)

                download_item = page.locator('div, span, button').filter(has_text="Download").last
                download_item.click()
                print("📥 Đã mở popup Download!")
                time.sleep(1.5)

                with page.expect_download(timeout=35000) as download_info:
                    unlock_btn = page.locator('button:has-text("Unlock & Download"), button:has-text("Download")').last
                    unlock_btn.click()
                    print("🚀 Đã bấm 'Unlock & Download'...")

                    download = download_info.value
                    original_name = download.suggested_filename
                    final_path = os.path.join(output_dir, original_name)
                    download.save_as(final_path)
                    downloaded_file = final_path
                    size_mb = round(os.path.getsize(final_path) / (1024 * 1024), 2)

                    print("==========================================================================")
                    print(f"🎉🎉🎉 TỰ ĐỘNG TẢI THÀNH CÔNG BÀI HÁT MỚI TỪ SUNO VỀ MÁY!")
                    print(f"📁 File: {final_path}")
                    print(f"📊 Dung lượng: {size_mb} MB")
                    print("==========================================================================")
            else:
                print("⚠️ Không tìm thấy nút More options của bài hát.")
        except Exception as dl_err:
            print(f"⚠️ Lỗi khi tải file từ Suno: {dl_err}")

        context.close()
        return downloaded_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool 1-Click Auto Gen Music Suno & Auto Download MP3")
    parser.add_argument("--lyrics", type=str, default=None, help="Lời bài hát")
    parser.add_argument("--style", type=str, default=None, help="Phong cách bài hát")
    args = parser.parse_args()
    auto_generate_and_download_song(lyrics=args.lyrics, style=args.style)
