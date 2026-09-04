import os
import sys
import subprocess
from datetime import datetime

# Cấu hình UTF-8 cho Windows Terminal
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

def check_system_status():
    print("==========================================================================")
    print("📊 DASHBOARD KIỂM TRA TIẾN TRÌNH & TRẠNG THÁI RENDER NGẦM (SUNO AUTOMATION)")
    print("==========================================================================")
    print(f"⏰ Thời gian hệ thống: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("==========================================================================")

    # 1. KIỂM TRA TIẾN TRÌNH ĐANG CHẠY NGẦM BẰNG POWERSHELL
    print("\n🔍 1. TIẾN TRÌNH RENDER / FFMPEG / PYTHON ĐANG CHẠY NGẦM:")
    ps_cmd = 'Get-Process | Where-Object {$_.ProcessName -match "ffmpeg|python|powershell"} | Select-Object Id, ProcessName, @{N="RunningTime"; E={(Get-Date) - $_.StartTime}}, @{N="MemMB"; E={[Math]::Round($_.WorkingSet64 / 1MB, 1)}} | ConvertTo-Json'
    
    try:
        res = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True, encoding='utf-8', errors='replace')
        if res.returncode == 0 and res.stdout.strip():
            import json
            data = json.loads(res.stdout.strip())
            if isinstance(data, dict):
                data = [data]
            
            print(f"{'PID':<8} | {'Tên Process':<18} | {'Thời gian chạy':<20} | {'RAM (MB)':<10}")
            print("-" * 65)
            for p in data:
                pname = p.get('ProcessName', '')
                pid = p.get('Id', '')
                mem = p.get('MemMB', 0)
                rtime = p.get('RunningTime', {})
                
                # Format running time
                if isinstance(rtime, dict):
                    days = rtime.get('Days', 0)
                    hours = rtime.get('Hours', 0)
                    minutes = rtime.get('Minutes', 0)
                    seconds = rtime.get('Seconds', 0)
                    if days > 0:
                        r_str = f"{days}d {hours}h {minutes}m"
                    elif hours > 0:
                        r_str = f"{hours}h {minutes}m {seconds}s"
                    else:
                        r_str = f"{minutes}m {seconds}s"
                else:
                    r_str = "Đang hoạt động"

                print(f"{pid:<8} | {pname:<18} | {r_str:<20} | {mem:<10}")
        else:
            print("✅ Hiện không có tiến trình Render/FFmpeg nào đang chạy ngầm.")
    except Exception as e:
        print(f"⚠️ Kiểm tra process: {e}")

    # 2. KIỂM TRA THƯ MỤC THÀNH PHẨM (VIDEO OUTPUT MONITOR)
    print("\n🎬 2. KẾT QUẢ VIDEO TRONG THƯ MỤC 'video_output':")
    video_dir = "video_output"
    if os.path.exists(video_dir):
        files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith(".mp4")]
        if files:
            files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            print(f"{'Tên File Video':<50} | {'Dung lượng':<12} | {'Thời gian tạo':<15}")
            print("-" * 82)
            for filepath in files[:5]: # Hiển thị 5 video gần nhất
                filename = os.path.basename(filepath)
                size_mb = round(os.path.getsize(filepath) / (1024 * 1024), 2)
                size_str = f"{size_mb} MB" if size_mb < 1024 else f"{round(size_mb/1024, 2)} GB"
                mod_time = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%H:%M:%S %d/%m")
                print(f"{filename[:48]:<50} | {size_str:<12} | {mod_time:<15}")
        else:
            print("📌 Chưa có file video nào trong folder video_output.")
    else:
        print("📌 Thư mục video_output chưa được tạo.")

    # 3. HƯỚNG DẪN KÍCH HOẠT NHANH
    print("\n==========================================================================")
    print("💡 HƯỚNG DẪN CÁC LUỒNG CHECKING TIẾN TRÌNH:")
    print("   1. Gõ lệnh: py check_status.py (hoặc .\\check_status.ps1)")
    print("   2. Xem Tab Title & Dashboard trên Web: Mở render_video.html trên Chrome")
    print("   3. Chạy Render tự động mới: py main_automation.py --prompt \"...\" --duration 1800")
    print("==========================================================================")

if __name__ == "__main__":
    check_system_status()
