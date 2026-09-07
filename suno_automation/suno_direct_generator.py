import os
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright

def run_suno_live_autofill():
    print("==========================================================================")
    print("🚀 BẮT ĐẦU TỰ ĐỘNG ĐIỀN TRỰC QUAN 100% TRÊN CỬA SỔ CHROME")
    print("==========================================================================")
    
    profile_dir = os.path.abspath("chrome_profile")
    os.makedirs(profile_dir, exist_ok=True)

    with sync_playwright() as p:
        print("🌐 Đang khởi động trình duyệt Chrome hiển thị trực tiếp trên màn hình...")
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

        print("🌐 Đang truy cập Suno Create: https://suno.com/create...")
        page.goto("https://suno.com/create", wait_until="domcontentloaded", timeout=60000)
        time.sleep(3)

        # Inject Banner thông báo tự động hóa trực tiếp lên giao diện Suno
        banner_script = """
        (() => {
            if (document.getElementById('auto-banner')) return;
            const b = document.createElement('div');
            b.id = 'auto-banner';
            b.style.position = 'fixed';
            b.style.top = '10px';
            b.style.left = '50%';
            b.style.transform = 'translateX(-50%)';
            b.style.background = 'linear-gradient(90deg, #0284c7, #2563eb)';
            b.style.color = '#ffffff';
            b.style.padding = '12px 28px';
            b.style.borderRadius = '30px';
            b.style.fontSize = '16px';
            b.style.fontWeight = 'bold';
            b.style.zIndex = '9999999';
            b.style.boxShadow = '0 10px 25px rgba(0,0,0,0.5)';
            b.innerText = '🤖 ANTIGRAVITY ĐANG TỰ ĐỘNG ĐIỀN FORM TẠO BÀI HÁT...';
            document.body.appendChild(b);
        })()
        """
        try:
            page.evaluate(banner_script)
        except Exception:
            pass

        # 1. Kích hoạt Custom mode nếu chưa bật
        print("⚙️ Đang kiểm tra & kích hoạt chế độ Tùy chỉnh (Custom)...")
        custom_toggle = page.query_selector("button:has-text('Tùy chỉnh'), button:has-text('Custom'), div[role='switch']:has-text('Custom')")
        if custom_toggle:
            try:
                aria_checked = custom_toggle.get_attribute("aria-checked")
                if aria_checked == "false" or "inactive" in (custom_toggle.get_attribute("class") or ""):
                    custom_toggle.click()
                    print("✅ Đã bật Custom Mode!")
                    time.sleep(1)
            except Exception:
                pass

        # 2. Mở Lời bài hát & Phong cách nếu đang đóng
        for title in ['Lời bài hát', 'Phong cách', 'Lyrics', 'Style']:
            header = page.query_selector(f"div:has-text('{title}'), span:has-text('{title}'), button:has-text('{title}')")
            if header:
                try:
                    header.click()
                    time.sleep(0.5)
                except Exception:
                    pass

        # Nội dung bài hát Lofi mới
        song_lyrics = """[Verse 1]
Mưa rơi tí tách bên ô cửa nhỏ
Ánh đèn vàng ấm áp góc bàn quen
Ly cà phê thơm nhẹ giữa đêm đen
Bao ưu tư tan theo từng dòng nhạc...

[Chorus]
Oh, midnight rain, wash away the blue
Chỉ còn đêm nay với những ước mơ xa
Tiếng mưa êm đềm như khúc ca
Đưa ta vào giấc ngủ say bình yên...

[Verse 2]
Phố cũ lặng im dưới hàng cây ướt
Gió khẽ lay từng kỷ niệm ngày qua
Một thoáng dịu dàng giữa những bôn ba
Lòng bình yên nghe tiếng thì thầm...

[Outro]
Tắm mát tâm hồn... Trôi theo tiếng mưa đêm...
Giấc ngủ ngọt ngào..."""

        song_style = "lofi hip hop, cozy chillhop, female vocal, soft mellow singing, warm rhodes piano, vinyl crackle, gentle boom bap drums, relaxing bpm 75"
        song_title = "Ký Ức Đêm Mưa - Midnight Rain Lofi"

        print("✍️ Đang tự động điền LỜI BÀI HÁT...")
        textareas = page.query_selector_all("textarea")
        if len(textareas) >= 1:
            textareas[0].evaluate("el => el.style.border = '3px solid #4ade80'")
            textareas[0].fill(song_lyrics)
            print("✅ Đã điền xong Lời bài hát!")
            time.sleep(1)

        print("✍️ Đang tự động điền PHONG CÁCH NHẠC...")
        if len(textareas) >= 2:
            textareas[1].evaluate("el => el.style.border = '3px solid #4ade80'")
            textareas[1].fill(song_style)
            print("✅ Đã điền xong Phong cách nhạc!")
            time.sleep(1)

        print("✍️ Đang tự động điền TIÊU ĐỀ BÀI HÁT...")
        title_inp = page.query_selector("input[placeholder*='Tiêu đề'], input[placeholder*='tiêu đề'], input[placeholder*='Title'], input[placeholder*='title']")
        if title_inp:
            title_inp.evaluate("el => el.style.border = '3px solid #4ade80'")
            title_inp.fill(song_title)
            print(f"✅ Đã điền xong Tiêu đề: '{song_title}'!")
            time.sleep(1)

        # Cập nhật banner thông báo
        try:
            page.evaluate("""(() => {
                const b = document.getElementById('auto-banner');
                if (b) {
                    b.style.background = 'linear-gradient(90deg, #16a34a, #059669)';
                    b.innerText = '🚀 ĐÃ ĐIỀN XONG TOÀN BỘ CÁC TRƯỜNG! ĐANG BẤM NÚT TẠO...';
                }
            })()""")
        except Exception:
            pass

        time.sleep(1.5)

        # 3. Tự động bấm nút Tạo (Create)
        print("🚀 Đang tìm và bấm nút ✨ Tạo...")
        create_btn = page.query_selector("button:has-text('Tạo'), button:has-text('Create'), button[type='submit']")
        if create_btn:
            create_btn.evaluate("el => el.style.outline = '4px solid #f97316'")
            create_btn.click()
            print("🎉 ĐÃ TỰ ĐỘNG BẤM NÚT TẠO THÀNH CÔNG TRÊN CỬA SỔ CHROME!")
        else:
            print("📌 Đã điền hoàn tất tất cả các ô trên màn hình!")

        try:
            page.evaluate("""(() => {
                const b = document.getElementById('auto-banner');
                if (b) {
                    b.innerText = '🎉 HOÀN TẤT TỰ ĐỘNG ĐIỀN & BẤM TẠO! BẠN CÓ THỂ LÀM VIỆC TIẾP TỤC TRÊN CỬA SỔ NÀY.';
                }
            })()""")
        except Exception:
            pass

        print("==========================================================================")
        print("👁️ CỬA SỔ CHROME ĐƯỢC GIỮ NGUYÊN TRÊN MÀN HÌNH ĐỂ BẠN TIẾP TỤC THEO DÕI VÀ LÀM VIỆC!")
        print("==========================================================================")
        
        # Giữ cửa sổ Chrome luôn mở liên tục không bao giờ tự tắt
        page.wait_for_timeout(3600000)

if __name__ == "__main__":
    run_suno_live_autofill()
