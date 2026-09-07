import os
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright

profile_dir = os.path.abspath("suno_automation/chrome_profile")
output_dir = os.path.abspath("suno_automation/music_output")
os.makedirs(output_dir, exist_ok=True)

print("==========================================================================")
print("🎵 ĐANG MỞ SUNO VÀ TẢI BẢN THU MỚI NHẤT VỀ MÁY...")
print("==========================================================================")

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=profile_dir,
        channel="chrome",
        headless=False,
        accept_downloads=True
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://suno.com/create?wid=default", wait_until="domcontentloaded")
    page.wait_for_timeout(5000)

    # 1. Click nút More options của bài hát đầu tiên
    print("🎯 [1/3] Mở Menu bài hát mới nhất...")
    more_btn = page.locator('button[aria-label="More options"][data-context-menu-trigger="true"]').first
    more_btn.click()
    page.wait_for_timeout(1000)

    # 2. Click mục Download
    print("📥 [2/3] Mở popup Download...")
    download_item = page.locator('div, span, button').filter(has_text="Download").last
    download_item.click()
    page.wait_for_timeout(1500)

    # 3. Bấm Unlock & Download
    print("🚀 [3/3] Đang bấm 'Unlock & Download' và lưu file MP3...")
    try:
        with page.expect_download(timeout=25000) as download_info:
            unlock_btn = page.locator('button:has-text("Unlock"), button:has-text("Download")').last
            unlock_btn.click()
            download = download_info.value
            filename = download.suggested_filename
            dest_file = os.path.join(output_dir, filename)
            download.save_as(dest_file)
            size_mb = round(os.path.getsize(dest_file) / (1024 * 1024), 2)
            print("==========================================================================")
            print(f"🎉🎉🎉 TẢI THÀNH CÔNG BÀI HÁT TỪ SUNO VỀ MÁY!")
            print(f"📁 Đường dẫn file: {dest_file}")
            print(f"📊 Dung lượng file: {size_mb} MB")
            print("==========================================================================")
    except Exception as e:
        print(f"⚠️ Thông báo tải: {e}")

    ctx.close()
