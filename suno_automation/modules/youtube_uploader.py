import os
import json
import time

class YouTubeUploader:
    def __init__(self, credentials_file="client_secret.json", token_file="token.json"):
        self.credentials_file = credentials_file
        self.token_file = token_file

    def upload_video(self, video_file: str, title: str, description: str, tags: list = None, category_id: str = "10", privacy_status: str = "public") -> str:
        """
        Đăng tải video tự động lên YouTube Channel qua YouTube Data API v3
        Category "10" là Music.
        Privacy Status: public / unlisted / private
        """
        print(f"🎬 Đang chuẩn bị đăng video lên YouTube: '{title}'...")
        
        if not os.path.exists(self.credentials_file):
            print(f"⚠️ Chưa tìm thấy file '{self.credentials_file}'!")
            print("💡 Vui lòng tạo OAuth Client ID từ Google Cloud Console và lưu thành client_secret.json")
            print("📌 Video hiện đã sẵn sàng tại local: " + video_file)
            return None

        try:
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.oauth2.credentials import Credentials

            SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

            creds = None
            if os.path.exists(self.token_file):
                creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
            
            if not creds or not creds.valid:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
                with open(self.token_file, "w") as token:
                    token.write(creds.to_json())

            youtube = build("youtube", "v3", credentials=creds)

            body = {
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags or ["lofi", "chill", "music", "study", "relax"],
                    "categoryId": category_id
                },
                "status": {
                    "privacyStatus": privacy_status,
                    "selfDeclaredMadeForKids": False
                }
            }

            media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
            request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

            print("⬆️ Đang tải video lên YouTube...")
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"📊 Đã tải lên: {int(status.progress() * 100)}%")

            video_id = response.get("id")
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            print(f"🎉 ĐĂNG VIDEO LÊN YOUTUBE THÀNH CÔNG!")
            print(f"🔗 Link Video: {video_url}")
            return video_url

        except Exception as e:
            print(f"❌ Lỗi khi đăng video lên YouTube: {e}")
            return None
