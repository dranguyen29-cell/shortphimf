import os
import sys
import time
import glob

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright

DOM_INJECTOR_SCRIPT = """
(() => {
    return new Promise((resolve) => {
        console.log("⚡ [DOM Fast Injection] Bắt đầu tự động chọc thẳng DOM...");
        
        // Helper trigger React state update
        function setInputValue(el, value) {
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
            nativeInputValueSetter.call(el, value);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }

        // 1. Click Advanced nếu đang ở chế độ Simple
        const advancedBtn = Array.from(document.querySelectorAll('button, div, span')).find(el => el.textContent.trim() === 'Advanced');
        if (advancedBtn) {
            console.log("⚡ Click Advanced");
            advancedBtn.click();
        }

        setTimeout(() => {
            // 2. Click Write Lyrics
            const writeLyricsBtn = Array.from(document.querySelectorAll('button, div, span')).find(el => el.textContent.trim() === 'Write Lyrics');
            if (writeLyricsBtn) {
                console.log("⚡ Click Write Lyrics");
                writeLyricsBtn.click();
            }

            setTimeout(() => {
                // 3. Điền Lyrics
                const lyricsText = `[Verse 1]
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
Tắm mát tâm hồn... Trôi theo tiếng mưa đêm...`;

                const allTextareas = document.querySelectorAll('textarea');
                if (allTextareas.length > 0) {
                    setInputValue(allTextareas[0], lyricsText);
                    allTextareas[0].style.border = '2px solid #22c55e';
                    console.log("✅ Đã chọc DOM điền Lyrics thành công!");
                }

                // 4. Click Styles accordion
                const stylesHeader = Array.from(document.querySelectorAll('div, button, span')).find(el => el.textContent.trim().startsWith('Styles') || el.textContent.trim().startsWith('Phong cách'));
                if (stylesHeader) {
                    console.log("⚡ Click mở Styles");
                    stylesHeader.click();
                }

                setTimeout(() => {
                    const textareasAfter = document.querySelectorAll('textarea');
                    const styleArea = textareasAfter.length > 1 ? textareasAfter[1] : document.querySelector('textarea[placeholder*="style"], textarea[placeholder*="Style"]');
                    if (styleArea) {
                        setInputValue(styleArea, "lofi hip hop, cozy chillhop, female vocal, soft mellow singing, warm rhodes piano, vinyl crackle, gentle boom bap drums, relaxing bpm 75");
                        styleArea.style.border = '2px solid #22c55e';
                        console.log("✅ Đã chọc DOM điền Style thành công!");
                    }

                    // 5. Bấm nút Create màu cam
                    setTimeout(() => {
                        const createBtn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Create' || b.textContent.trim() === 'Tạo');
                        if (createBtn) {
                            createBtn.style.outline = '4px solid #f97316';
                            createBtn.click();
                            console.log("🚀 ĐÃ CHỌC DOM BẤM NÚT CREATE THÀNH CÔNG!");
                            resolve({ success: true, message: "Đã điền và bấm nút Create thành công!" });
                        } else {
                            resolve({ success: true, message: "Đã điền đủ Lời & Style!" });
                        }
                    }, 400);

                }, 400);

            }, 400);

        }, 400);
    });
})()
"""

def fast_dom_generate():
    print("==========================================================================")
    print("⚡ KHỞI ĐỘNG FAST DOM INJECTION 1-CLICK: TỰ ĐỘNG CHỌC THẲNG VÀO DOM SUNO")
    print("==========================================================================")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    profile_dir = os.path.join(current_dir, "chrome_profile")
    os.makedirs(profile_dir, exist_ok=True)
    
    # Dọn dẹp lock cũ nếu có
    for lock_file in glob.glob(os.path.join(profile_dir, "*lock*")) + glob.glob(os.path.join(profile_dir, "Singleton*")):
        try: os.remove(lock_file)
        except Exception: pass

    # Đồng bộ Profile 'Long Nguyen' (Profile 1)
    import shutil
    src_p1 = os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1')
    print("🔄 Đồng bộ dữ liệu Profile Long Nguyen...")
    try:
        shutil.copytree(os.path.join(src_p1, 'Network'), os.path.join(profile_dir, 'Default', 'Network'), dirs_exist_ok=True, ignore=shutil.ignore_patterns('*.lock', 'LOCK', '*journal*'))
    except Exception:
        pass

    with sync_playwright() as p:
        print("🌐 Mở Google Chrome...")
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

        print("🌐 Vào thẳng https://suno.com/create...")
        page.goto("https://suno.com/create", wait_until="domcontentloaded", timeout=60000)
        time.sleep(2)

        print("⚡ Đang chọc thẳng vào DOM HTML để điền toàn bộ trường và bấm Create...")
        result = page.evaluate(DOM_INJECTOR_SCRIPT)
        print(f"🎉 Kết quả thực thi DOM: {result}")
        
        print("==========================================================================")
        print("✅ ĐÃ HOÀN TẤT TRONG 1 LỆNH DUY NHẤT! TRÌNH DUYỆT ĐƯỢC GIỮ NGUYÊN ĐỂ THEO DÕI.")
        print("==========================================================================")
        
        # Giữ nguyên cửa sổ
        page.wait_for_timeout(3600000)

if __name__ == "__main__":
    fast_dom_generate()
