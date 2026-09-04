import os
import subprocess
import sys

# Cấu hình UTF-8 cho stdout/stderr trên Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

class VideoRenderer:
    def __init__(self, script_path="auto_render_ffmpeg.ps1"):
        self.script_path = script_path

    def render(self, audio_file: str, image_file: str, duration_seconds: int, output_file: str) -> str:
        """
        Gọi PowerShell script FFmpeg để render video ngầm chất lượng cao 15 Mbps
        """
        print("==========================================================")
        print("🚀 BẮT ĐẦU RENDER VIDEO NGẦM BẰNG FFMPEG")
        print(f"Audio : {audio_file}")
        print(f"Image : {image_file}")
        print(f"Thời lượng: {duration_seconds}s ({round(duration_seconds / 60)} phút)")
        print(f"Output: {output_file}")
        print("==========================================================")

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        cmd = [
            "powershell",
            "-ExecutionPolicy", "Bypass",
            "-File", self.script_path,
            "-AudioFile", audio_file,
            "-ImageFile", image_file,
            "-DurationSeconds", str(duration_seconds),
            "-OutputFile", output_file
        ]

        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
            for line in iter(process.stdout.readline, ''):
                if line:
                    sys.stdout.write(line)
                    sys.stdout.flush()
            process.wait()
            if process.returncode == 0 and os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"\n🎉 RENDER THÀNH CÔNG! Dung lượng file: {round(size_mb, 2)} MB")
                return output_file
            else:
                print("\n❌ File video đầu ra không tìm thấy hoặc tiến trình bị lỗi!")
                return None
        except Exception as e:
            print(f"❌ Lỗi khi gọi FFmpeg render: {e}")
            return None

if __name__ == "__main__":
    renderer = VideoRenderer()
    renderer.render(
        audio_file="music_output/Midnight Rain & Coffee.mp3",
        image_file="Image/lofi.jpg",
        duration_seconds=60,
        output_file="video_output/Test_Auto_Render.mp4"
    )
