import os
import sys
import argparse
from datetime import datetime

# Cấu hình hiển thị UTF-8 tiếng Việt chuẩn trên Windows Terminal
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from modules.music_generator import SunoMusicGenerator
from modules.image_generator import ImageGenerator
from modules.video_renderer import VideoRenderer
from modules.youtube_uploader import YouTubeUploader

def run_pipeline(prompt: str, duration_seconds: int = 1800, privacy_status: str = "public"):
    """
    Quy trình tự động hóa End-to-End 1-Click:
    1. Nhập Prompt -> Tự gen bài hát Suno & tải về folder music_output
    2. Tự gen Ảnh nền/Thumbnail AI sắc nét 4K
    3. Tự động Render Video Ultra HD 4K ngầm
    4. Tự động Đăng video lên YouTube Channel với đầy đủ Metadata
    """
    print("==========================================================================")
    print("🚀 BẮT ĐẦU HỆ THỐNG TỰ ĐỘNG HÓA 1-CLICK: SUNO MUSIC -> 4K VIDEO -> YOUTUBE")
    print("==========================================================================")
    print(f"📝 Prompt Nhạc    : {prompt}")
    print(f"⏱️ Thời lượng Video: {duration_seconds} giây ({round(duration_seconds / 60)} phút)")
    print(f"🔒 Chế độ YouTube : {privacy_status}")
    print("==========================================================================")

    # BƯỚC 1: Gen Nhạc AI từ Suno & Tải về folder
    print("\n--- [ BƯỚC 1: TỰ ĐỘNG GEN NHẠC SUNO AI ] ---")
    music_gen = SunoMusicGenerator()
    music_info = music_gen.generate_and_download(prompt=prompt)

    if not music_info or not os.path.exists(music_info["file_path"]):
        print("❌ Lỗi: Không tìm thấy file âm thanh sau bước 1!")
        return

    audio_file = music_info["file_path"]
    song_title = music_info["title"]
    print(f"✅ Đã có file âm thanh: {audio_file}")

    # BƯỚC 2: Gen Ảnh nền AI 4K
    print("\n--- [ BƯỚC 2: TỰ ĐỘNG GEN ẢNH NỀN 4K AI ] ---")
    image_gen = ImageGenerator()
    image_file = image_gen.generate_lofi_background(prompt=prompt)
    print(f"✅ Đã có ảnh nền 4K: {image_file}")

    # BƯỚC 3: Render Video Ultra HD 4K ngầm bằng FFmpeg
    print("\n--- [ BƯỚC 3: RENDER VIDEO ULTRA HD 4K NGẦM ] ---")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_output_file = os.path.join("video_output", f"{song_title.replace(' ', '_')}_{timestamp}_4K.mp4")
    
    renderer = VideoRenderer()
    video_file = renderer.render(
        audio_file=audio_file,
        image_file=image_file,
        duration_seconds=duration_seconds,
        output_file=video_output_file
    )

    if not video_file or not os.path.exists(video_file):
        print("❌ Lỗi: Tiến trình Render video thất bại!")
        return

    print(f"✅ Xuất video thành công: {video_file}")

    # BƯỚC 4: Tự động Đăng Video lên YouTube Channel
    print("\n--- [ BƯỚC 4: TỰ ĐỘNG ĐĂNG VIDEO LÊN YOUTUBE ] ---")
    youtube_title = f"{song_title} ~ Lofi Beats to Study & Relax to"
    youtube_description = f"""☕ {song_title}
✨ Relaxing Lofi Chill Beats for Study, Work, Coding & Sleep.

📌 Track Info:
- Music Generated with Suno AI
- Prompt: {prompt}
- Video Quality: Ultra HD 4K (15 Mbps High Bitrate)

#lofi #studybeats #relaxing #sunomusic #lofibit #4k
"""
    uploader = YouTubeUploader()
    youtube_url = uploader.upload_video(
        video_file=video_file,
        title=youtube_title,
        description=youtube_description,
        privacy_status=privacy_status
    )

    print("\n==========================================================================")
    print("🎉 QUY TRÌNH TỰ ĐỘNG HÓA HOÀN TẤT 100%!")
    print(f"🎵 Audio  : {audio_file}")
    print(f"🖼️ Image  : {image_file}")
    print(f"🎬 Video  : {video_file}")
    if youtube_url:
        print(f"🔗 YouTube: {youtube_url}")
    else:
        print("📌 Video đã xuất sẵn tại local (Thêm client_secret.json để tự động upload lên YouTube)")
    print("==========================================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool Quy Trình Tự Động: Prompt -> Suno -> Render 4K -> YouTube")
    parser.add_argument("--prompt", type=str, default="Midnight Rain & Coffee Lofi Chill", help="Prompt bài nhạc")
    parser.add_argument("--duration", type=int, default=1800, help="Thời lượng video (giây)")
    parser.add_argument("--privacy", type=str, default="public", choices=["public", "unlisted", "private"], help="Chế độ YouTube")
    
    args = parser.parse_args()
    run_pipeline(prompt=args.prompt, duration_seconds=args.duration, privacy_status=args.privacy)
