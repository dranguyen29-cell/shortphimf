import os
import sys
import json
import time
import glob
import uuid
import queue
import subprocess
import threading
import urllib.parse
from datetime import datetime
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(BASE_DIR, "suno_studio.html")
ENV_FILE = os.path.join(BASE_DIR, ".env")
OUTPUT_DIR = os.path.join(BASE_DIR, "music_output")
PROFILE_DIR = os.path.join(BASE_DIR, "chrome_profile")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PROFILE_DIR, exist_ok=True)

JOBS = {}
TASK_QUEUE = queue.Queue()
EXT_QUEUE = []
EXT_LAST_SEEN = 0.0


def log_job(job_id: str, msg: str, step: int = None):
    if not job_id or job_id not in JOBS:
        print(msg)
        return
    JOBS[job_id]["logs"].append(msg)
    if step is not None:
        JOBS[job_id]["step"] = step
    print(f"[{job_id[:6]}] {msg}")


def free_profile_locks():
    """
    Giải phóng lock của riêng thư mục suno_automation/chrome_profile
    (Không chạm vào trình duyệt Chrome chính của người dùng).
    """
    ps_kill = (
        "Get-CimInstance Win32_Process -Filter \"Name = 'chrome.exe'\" | "
        "Where-Object { $_.CommandLine -like '*suno_automation*chrome_profile*' } | "
        "ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
    )
    try:
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_kill], capture_output=True, timeout=6)
    except Exception:
        pass

    for lock_file in glob.glob(os.path.join(PROFILE_DIR, "*lock*")) + glob.glob(os.path.join(PROFILE_DIR, "Singleton*")):
        try:
            os.remove(lock_file)
        except Exception:
            pass


def inject_suno_auth_cookie(context, job_id: str = None):
    """
    Nạp trực tiếp SUNO_REFRESH_TOKEN từ file .env vào Cookie __client của trình duyệt
    để đảm bảo luôn đăng nhập sẵn tài khoản Suno (draminkute) 100%.
    """
    if not os.path.exists(ENV_FILE):
        return
    try:
        token = None
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("SUNO_REFRESH_TOKEN="):
                    token = line.strip().split("=", 1)[1].strip()
                    break
        if token:
            log_job(job_id, "🔐 Đồng bộ phiên đăng nhập Suno (draminkute) từ .env token...", step=1)
            context.add_cookies([
                {
                    "name": "__client",
                    "value": token,
                    "domain": "auth.suno.com",
                    "path": "/",
                    "httpOnly": True,
                    "secure": True,
                    "sameSite": "None"
                },
                {
                    "name": "__client",
                    "value": token,
                    "domain": ".suno.com",
                    "path": "/",
                    "httpOnly": True,
                    "secure": True,
                    "sameSite": "Lax"
                }
            ])
    except Exception as e:
        log_job(job_id, f"⚠️ Lưu ý khi nạp token: {e}", step=1)


def fill_and_trigger_suno_v6(page, job_id: str, title: str, lyrics: str, style: str, instrumental: bool) -> dict:
    """
    Cuộn từng ô (scrollIntoView) ra giữa khung nhìn và dùng thao tác chuột/bàn phím phần cứng
    (page.mouse.click & page.keyboard.insert_text) để kích hoạt đầy đủ state React 18 của Suno v6-mini.
    """
    log_job(job_id, "⏳ Đang chờ thanh chuyển đổi Simple / Advanced hiển thị...", step=2)

    for _ in range(35):
        try:
            ready = page.evaluate(
                "() => Array.from(document.querySelectorAll('button[role=\"tab\"]')).some(e => e.textContent.trim() === 'Advanced')"
            )
            if ready:
                break
        except Exception:
            pass
        time.sleep(1.0)

    time.sleep(1.2)

    # 1. Click tab Advanced (BUTTON[role="tab"] ở phía trên cùng)
    log_job(job_id, "⚡ [1/4] Bấm chuyển sang tab Advanced...", step=2)
    adv_rect = page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button[role="tab"]'))
            .find(e => e.textContent.trim() === 'Advanced');
        if (!btn) return null;
        const r = btn.getBoundingClientRect();
        return { x: r.x, y: r.y, width: r.width, height: r.height };
    }""")
    if adv_rect:
        page.mouse.click(adv_rect["x"] + adv_rect["width"] / 2, adv_rect["y"] + adv_rect["height"] / 2)
        time.sleep(1.2)

    # 2. Cuộn ô Lyrics ([contenteditable="true"]) ra giữa và gõ phím thật
    log_job(job_id, "✍️ [2/4] Cuộn khung Lyrics và gõ Lời bài hát...", step=2)
    page.evaluate("""() => {
        const el = Array.from(document.querySelectorAll('[contenteditable="true"]'))
            .find(e => e.getBoundingClientRect().width > 200);
        if (el) el.scrollIntoView({ block: 'center' });
    }""")
    time.sleep(0.35)
    lyrics_rect = page.evaluate("""() => {
        const el = Array.from(document.querySelectorAll('[contenteditable="true"]'))
            .find(e => e.getBoundingClientRect().width > 200);
        if (!el) return null;
        el.style.outline = '2px solid #38A169';
        const r = el.getBoundingClientRect();
        return { x: r.x, y: r.y, width: r.width, height: r.height };
    }""")
    if lyrics_rect:
        page.mouse.click(lyrics_rect["x"] + lyrics_rect["width"] / 2, lyrics_rect["y"] + 45)
        time.sleep(0.2)
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        if not instrumental and lyrics:
            page.keyboard.insert_text(lyrics)
        time.sleep(0.4)

    # 3. Cuộn ô Styles (<textarea> có dấu phẩy trong placeholder) ra giữa và gõ phím thật
    log_job(job_id, "🎸 [3/4] Cuộn khung Styles và gõ Phong cách âm nhạc...", step=2)
    page.evaluate("""() => {
        const el = Array.from(document.querySelectorAll('textarea'))
            .find(e => (e.placeholder || '').includes(','));
        if (el) el.scrollIntoView({ block: 'center' });
    }""")
    time.sleep(0.35)
    style_rect = page.evaluate("""() => {
        const el = Array.from(document.querySelectorAll('textarea'))
            .find(e => (e.placeholder || '').includes(','));
        if (!el) return null;
        el.style.outline = '2px solid #38A169';
        const r = el.getBoundingClientRect();
        return { x: r.x, y: r.y, width: r.width, height: r.height };
    }""")
    if style_rect:
        page.mouse.click(style_rect["x"] + style_rect["width"] / 2, style_rect["y"] + 35)
        time.sleep(0.2)
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        page.keyboard.insert_text(style)
        time.sleep(0.4)

    # 4. Cuộn ô Song Title (<input placeholder*="Song Title">) ra giữa và gõ phím thật
    log_job(job_id, "🏷️ [4/4] Cuộn khung Song Title và gõ Tiêu đề bài hát...", step=2)
    page.evaluate("""() => {
        const inps = Array.from(document.querySelectorAll('input'))
            .filter(e => (e.placeholder || '').toLowerCase().includes('song title'));
        const el = inps[inps.length - 1];
        if (el) el.scrollIntoView({ block: 'center' });
    }""")
    time.sleep(0.35)
    title_rect = page.evaluate("""() => {
        const inps = Array.from(document.querySelectorAll('input'))
            .filter(e => (e.placeholder || '').toLowerCase().includes('song title'));
        const el = inps[inps.length - 1];
        if (!el) return null;
        el.style.outline = '2px solid #38A169';
        const r = el.getBoundingClientRect();
        return { x: r.x, y: r.y, width: r.width, height: r.height };
    }""")
    if title_rect and title:
        page.mouse.click(title_rect["x"] + title_rect["width"] / 2, title_rect["y"] + title_rect["height"] / 2)
        time.sleep(0.2)
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        page.keyboard.insert_text(title)
        time.sleep(0.4)

    # 5. Kiểm tra nút Create đã bật sáng màu cam (disabled == False) và click thật
    btns_after = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('button'))
            .filter(e => e.offsetParent !== null && e.textContent.trim().includes('Create'))
            .map(e => ({ txt: e.textContent.trim(), disabled: e.disabled, rect: e.getBoundingClientRect() }));
    }""")
    clicked = False
    if btns_after:
        b = btns_after[-1]
        rect = b["rect"]
        page.mouse.click(rect["x"] + rect["width"] / 2, rect["y"] + rect["height"] / 2)
        clicked = not b["disabled"]

    return {
        "clicked": clicked,
        "lyrics_ok": bool(lyrics_rect),
        "style_ok": bool(style_rect),
        "title_ok": bool(title_rect)
    }


def playwright_persistent_worker():
    from playwright.sync_api import sync_playwright

    pw = None
    context = None
    page = None

    def ensure_session(job_id: str = None):
        nonlocal pw, context, page
        if context is not None and page is not None:
            try:
                _ = page.url
                return page
            except Exception:
                try:
                    context.close()
                except Exception:
                    pass
                context = None
                page = None

        if pw is None:
            pw = sync_playwright().start()

        free_profile_locks()
        log_job(job_id, "🌐 Mở cửa sổ Google Chrome (Suno Direct Studio)...", step=1)

        context = pw.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            channel="chrome",
            headless=False,
            accept_downloads=True,
            ignore_default_args=["--enable-automation"],
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled"
            ],
            viewport={"width": 1440, "height": 900}
        )
        context.add_init_script("try { delete Object.getPrototypeOf(navigator).webdriver; } catch (e) {}")
        inject_suno_auth_cookie(context, job_id)
        page = context.pages[0] if context.pages else context.new_page()
        return page

    while True:
        task = TASK_QUEUE.get()
        if task is None:
            break

        action = task.get("action")
        job_id = task.get("job_id")
        payload = task.get("payload", {})

        try:
            active_page = ensure_session(job_id)
            try:
                active_page.bring_to_front()
            except Exception:
                pass

            if action == "open_only":
                if "suno.com/create" not in (active_page.url or ""):
                    try:
                        active_page.goto("https://suno.com/create", wait_until="commit", timeout=20000)
                    except Exception:
                        pass
                if job_id and job_id in JOBS:
                    JOBS[job_id]["status"] = "completed"

            elif action == "generate":
                title = payload.get("title", "Suno Studio Track")
                lyrics = payload.get("lyrics", "")
                style = payload.get("style", "lofi hip hop, warm rhodes piano")
                instrumental = bool(payload.get("instrumental", False))
                auto_download = bool(payload.get("auto_download", True))

                if "suno.com/create" not in (active_page.url or ""):
                    log_job(job_id, "🌐 Đang mở https://suno.com/create...", step=2)
                    try:
                        active_page.goto("https://suno.com/create", wait_until="commit", timeout=20000)
                    except Exception:
                        pass
                else:
                    log_job(job_id, "⚡ Thao tác trực tiếp trên cửa sổ Chrome Suno đang mở...", step=2)

                res = fill_and_trigger_suno_v6(
                    page=active_page,
                    job_id=job_id,
                    title=title,
                    lyrics=lyrics,
                    style=style,
                    instrumental=instrumental
                )

                if res.get("clicked"):
                    log_job(
                        job_id,
                        f"🎉 ĐÃ GÕ PHÍM THẬT ĐIỀN ĐẦY ĐỦ 3 Ô (Lyrics={res.get('lyrics_ok')}, Style={res.get('style_ok')}, Title={res.get('title_ok')}) & BẤM NÚT CAM '✨ Create'!",
                        step=3
                    )
                else:
                    log_job(job_id, f"✅ Đã điền dữ liệu lên Suno ({res})! Hãy kiểm tra nút Create trên cửa sổ Chrome.", step=3)

                if auto_download:
                    log_job(job_id, "⏳ Đang giữ cửa sổ để Suno sáng tác (45 giây)... Hãy xem trực tiếp trên cửa sổ Chrome vừa bật lên!", step=3)
                    time.sleep(45)
                    log_job(job_id, "📥 Hoàn tất chu kỳ! Bạn có thể bấm 'Tải MP3 Mới Nhất' để lưu file về máy.", step=4)

                JOBS[job_id]["status"] = "completed"

            elif action == "download_latest":
                log_job(job_id, "🌐 Đang kiểm tra danh sách bài hát trên https://suno.com/create...", step=4)
                if "suno.com/create" not in (active_page.url or ""):
                    try:
                        active_page.goto("https://suno.com/create?wid=default", wait_until="commit", timeout=20000)
                    except Exception:
                        pass
                    time.sleep(4.0)

                log_job(job_id, "🎯 Đang mở menu (...) của bài hát đầu tiên...", step=4)
                active_page.evaluate("""() => {
                    const btn = document.querySelector('button[aria-label="More options"], button[data-context-menu-trigger="true"]');
                    if (btn) btn.click();
                }""")
                time.sleep(1.0)
                active_page.evaluate("""() => {
                    const dl = Array.from(document.querySelectorAll('div, span, button'))
                        .filter(e => e.textContent.trim().includes('Download')).pop();
                    if (dl) dl.click();
                }""")
                time.sleep(1.5)

                with active_page.expect_download(timeout=25000) as download_info:
                    active_page.evaluate("""() => {
                        const btn = Array.from(document.querySelectorAll('button'))
                            .filter(e => e.textContent.includes('Unlock') || e.textContent.includes('Download') || e.textContent.includes('MP3')).pop();
                        if (btn) btn.click();
                    }""")
                    download = download_info.value
                    filename = download.suggested_filename
                    dest_file = os.path.join(OUTPUT_DIR, filename)
                    download.save_as(dest_file)
                    size_mb = round(os.path.getsize(dest_file) / (1024 * 1024), 2)
                    log_job(job_id, f"🎉 TẢI THÀNH CÔNG BÀI HÁT TỪ SUNO: {filename} ({size_mb} MB)!", step=4)

                JOBS[job_id]["status"] = "completed"

        except Exception as e:
            log_job(job_id, f"❌ Lỗi trong quá trình thực thi: {e}", step=2)
            if job_id and job_id in JOBS:
                JOBS[job_id]["status"] = "failed"
            if "closed" in str(e).lower() or "target" in str(e).lower():
                context = None
                page = None


class SunoStudioRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def _send_json(self, data: dict, status: int = 200):
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        global EXT_LAST_SEEN
        parsed = urllib.parse.urlparse(self.path)
        path = urllib.parse.unquote(parsed.path)

        if path in ("/", "/index.html", "/suno_studio.html"):
            with open(HTML_FILE, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(content)
            return

        if path == "/api/ext-poll":
            EXT_LAST_SEEN = time.time()
            task = EXT_QUEUE.pop(0) if EXT_QUEUE else None
            self._send_json({"task": task})
            return

        if path == "/api/tracks":
            tracks = []
            if os.path.exists(OUTPUT_DIR):
                mp3_files = [
                    os.path.join(OUTPUT_DIR, f)
                    for f in os.listdir(OUTPUT_DIR)
                    if f.lower().endswith(".mp3")
                ]
                mp3_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                for fpath in mp3_files:
                    fname = os.path.basename(fpath)
                    title = os.path.splitext(fname)[0]
                    size_mb = round(os.path.getsize(fpath) / (1024 * 1024), 2)
                    mtime = datetime.fromtimestamp(os.path.getmtime(fpath)).strftime("%d/%m/%Y %H:%M")
                    tracks.append({
                        "name": fname,
                        "title": title,
                        "style": "Suno AI Master Track · 48kHz Stereo",
                        "size_mb": size_mb,
                        "modified": mtime,
                        "url": "/audio/" + urllib.parse.quote(fname)
                    })
            self._send_json({
                "tracks": tracks,
                "bridge_connected": (time.time() - EXT_LAST_SEEN) < 3.5
            })
            return

        if path.startswith("/api/status/"):
            job_id = path.split("/api/status/")[-1]
            job = JOBS.get(job_id)
            if not job:
                self._send_json({"error": "Job not found"}, 404)
            else:
                self._send_json(job)
            return

        if path.startswith("/audio/"):
            fname = os.path.basename(path[len("/audio/"):])
            fpath = os.path.join(OUTPUT_DIR, fname)
            if not os.path.exists(fpath):
                self.send_error(404, "Audio file not found")
                return

            file_size = os.path.getsize(fpath)
            range_header = self.headers.get("Range")
            if range_header and range_header.startswith("bytes="):
                ranges = range_header.replace("bytes=", "").split("-")
                start = int(ranges[0]) if ranges[0] else 0
                end = int(ranges[1]) if len(ranges) > 1 and ranges[1] else file_size - 1
                end = min(end, file_size - 1)
                length = end - start + 1

                with open(fpath, "rb") as f:
                    f.seek(start)
                    data = f.read(length)

                self.send_response(206)
                self.send_header("Content-Type", "audio/mpeg")
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
                self.send_header("Content-Length", str(length))
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(data)
            else:
                with open(fpath, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "audio/mpeg")
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Length", str(file_size))
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(data)
            return

        self.send_error(404, "Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body_raw = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            payload = json.loads(body_raw)
        except Exception:
            payload = {}

        if path == "/api/ext-report":
            job_id = payload.get("job_id")
            msg = payload.get("msg")
            step = payload.get("step")
            status = payload.get("status")
            if job_id and msg:
                log_job(job_id, msg, step=step)
            if job_id and status and job_id in JOBS:
                JOBS[job_id]["status"] = status
            self._send_json({"ok": True})
            return

        if path == "/api/generate":
            job_id = str(uuid.uuid4())
            JOBS[job_id] = {
                "job_id": job_id,
                "status": "running",
                "step": 1,
                "logs": [f"🚀 Khởi tạo lệnh tạo nhạc trực tiếp: '{payload.get('title', 'Untitled')}'"]
            }
            # Nếu Tab Suno trên trình duyệt chính đang kết nối Bridge/Extension (< 3.5 giây), ưu tiên chạy thẳng trên Tab đang mở!
            if (time.time() - EXT_LAST_SEEN) < 3.5:
                log_job(job_id, "🔗 Phát hiện Tab Suno đang mở đã kết nối Live Bridge — Gửi lệnh thẳng sang Tab Suno!", step=2)
                EXT_QUEUE.append({
                    "action": "generate",
                    "job_id": job_id,
                    "payload": payload
                })
            else:
                TASK_QUEUE.put({
                    "action": "generate",
                    "job_id": job_id,
                    "payload": payload
                })
            self._send_json({"job_id": job_id, "status": "started"})
            return

        if path == "/api/download-latest":
            job_id = str(uuid.uuid4())
            JOBS[job_id] = {
                "job_id": job_id,
                "status": "running",
                "step": 4,
                "logs": ["📥 Khởi chạy tiến trình tải bản thu mới nhất từ Suno..."]
            }
            TASK_QUEUE.put({
                "action": "download_latest",
                "job_id": job_id,
                "payload": {}
            })
            self._send_json({"job_id": job_id, "status": "started"})
            return

        if path == "/api/open-suno":
            job_id = str(uuid.uuid4())
            JOBS[job_id] = {
                "job_id": job_id,
                "status": "running",
                "step": 1,
                "logs": ["🌐 Mở cửa sổ Suno AI..."]
            }
            TASK_QUEUE.put({
                "action": "open_only",
                "job_id": job_id,
                "payload": {}
            })
            self._send_json({"ok": True, "job_id": job_id})
            return

        self._send_json({"error": "Unknown endpoint"}, 404)


def run_server(port: int = 8088):
    server = ThreadingHTTPServer(("0.0.0.0", port), SunoStudioRequestHandler)
    http_thread = threading.Thread(target=server.serve_forever, daemon=True)
    http_thread.start()

    print("==========================================================================")
    print(f"🎹 SUNO DIRECT STUDIO WEB SERVER ĐANG CHẠY TẠI: http://localhost:{port}")
    print(f"📂 Thư mục nhạc MP3: {OUTPUT_DIR}")
    print("==========================================================================")
    playwright_persistent_worker()


if __name__ == "__main__":
    run_server(8088)
