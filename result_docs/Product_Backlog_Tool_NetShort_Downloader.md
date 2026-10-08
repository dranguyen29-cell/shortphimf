# TÀI LIỆU PRODUCT BACKLOG: NÂNG CẤP TOOL NETSHORT DOWNLOADER
> **Dự án:** Tool Crawl & Xử lý Short Phim (NetShort Downloader)  
> **Người thực hiện:** Senior BA / Product Owner  
> **Phiên bản:** 1.0  
> **Ngày lập:** 15/09/2026  
> **Trạng thái:** Ready for Sprint Planning  

---

## I. TỔNG QUAN VÀ BỐI CẢNH (BUSINESS CONTEXT)

### 1. Hiện trạng quy trình vận hành (AS-IS)
- **Bước 1:** Đội vận hành mở tool "NetShort Downloader", chọn danh mục phim ("Theater") và số trang để duyệt danh sách card phim bằng mắt (chưa có ô tìm kiếm tên phim).
- **Bước 2:** Bấm tải phim/tập phim -> Hệ thống tải về máy 2 file riêng biệt: `video.mp4` (video tiếng Anh/gốc) và `phu_de.vtt`.
- **Bước 3:** Đội vận hành phải tự mở công cụ bên ngoài (convert VTT sang SRT), sau đó import từng file MP4 và SRT vào phần mềm dựng (CapCut / Premiere / Aegisub) để dán sub cứng tiếng Việt (Hardsub).
- **Nút thắt (Bottleneck / Pain Points):**
  - Thiếu tính năng tìm kiếm khiến việc tìm đúng phim tốn nhiều thời gian khi số lượng phim lên đến hàng trăm bộ.
  - Mỗi bộ phim ngắn có từ 50 - 100 tập (1-3 phút/tập). Việc mở CapCut/Premiere chèn sub thủ công từng tập ngốn từ 2 - 4 tiếng mỗi ngày của nhân sự vận hành.
  - Lỗi phát sinh do nhân sự phải tự convert thủ công định dạng VTT sang SRT.

### 2. Mục tiêu cải tiến (TO-BE)
- Bổ sung ô tìm kiếm (Search) phim trực tiếp theo tên hoặc ID phim ngay trên giao diện danh sách.
- Tự động hóa 100% quy trình: Khi tải phim về, hệ thống tự động dịch phụ đề sang Tiếng Việt (nếu cần) và dùng **FFmpeg ngầm** để dán sub cứng vào file MP4.
- **Giá trị kinh doanh (Business Value):** Giảm **95% thời gian thủ công**, tải về là có ngay video MP4 hoàn chỉnh đã có sub tiếng Việt chuẩn để đăng lên Web/App/Mạng xã hội.

---

## II. DANH SÁCH PRODUCT BACKLOG ITEMS (PBI)

| Item ID | Loại | Tên tính năng / User Story | Mức độ ưu tiên | Ước tính (Story Points) | Sprint đề xuất |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **PBI-01** | Feature | Tìm kiếm phim theo tên và ID trên màn hình danh sách | **P0 (Must-have)** | 3 | Sprint 1 |
| **PBI-02** | Feature | Tự động ghép Sub cứng vào video MP4 (Auto-burn Hardsub) | **P0 (Must-have)** | 8 | Sprint 1 |
| **PBI-03** | Feature | Tự động dịch phụ đề sang Tiếng Việt (Auto-translate Subtitle) | **P1 (Should-have)**| 5 | Sprint 1 hoặc 2 |
| **PBI-04** | Enhancement | Cấu hình Style phụ đề (Font, Size, Màu viền, Vị trí cho khung hình 9:16) | **P2 (Could-have)** | 3 | Sprint 2 |

---

## III. CHI TIẾT USER STORIES & ACCEPTANCE CRITERIA (INVEST + GHERKIN)

### US-01: Tìm kiếm phim theo tên và Movie ID
- **ID:** `US-01`
- **As a:** Chuyên viên Vận hành nội dung (Content Operator)
- **I want to:** Tìm kiếm phim theo từ khóa tên phim hoặc ID phim trên màn hình crawl
- **So that:** Tôi có thể nhanh chóng tìm đúng bộ phim cần xử lý mà không phải lật tìm thủ công qua từng trang danh mục.

#### Acceptance Criteria:
- **AC1: Tìm kiếm theo tên phim thành công (Happy Path)**
  - **Given** Chuyên viên đang ở màn hình danh sách phim của tool NetShort Downloader
  - **When** Chuyên viên nhập từ khóa tên phim (VD: "Khát Vọng", "Bắt Gian") vào ô tìm kiếm và bấm Enter hoặc click biểu tượng Kính lúp (hoặc debounce gõ phím)
  - **Then** Hệ thống lọc và hiển thị danh sách các thẻ phim có tên chứa từ khóa tìm kiếm (không phân biệt chữ hoa/thường, hỗ trợ tiếng Việt có dấu và không dấu).

- **AC2: Tìm kiếm theo Movie ID chính xác**
  - **Given** Chuyên viên có ID phim (VD: `2098678126826008577`)
  - **When** Nhập chuỗi số ID vào ô tìm kiếm
  - **Then** Hệ thống trả về chính xác card phim có ID tương ứng.

- **AC3: Không tìm thấy kết quả**
  - **Given** Chuyên viên nhập từ khóa không trùng khớp với bất kỳ phim nào
  - **When** Thực hiện tìm kiếm
  - **Then** Hệ thống hiển thị thông báo thân thiện: "Không tìm thấy bộ phim phù hợp với từ khóa '{từ khóa}'" kèm nút "Xóa bộ lọc / Làm mới".

- **AC4: Xóa từ khóa tìm kiếm**
  - **Given** Ô tìm kiếm đang có text
  - **When** Chuyên viên bấm nút [X] trong ô search hoặc xóa trắng nội dung
  - **Then** Danh sách phim lập tức quay về trạng thái hiển thị đầy đủ theo danh mục hiện tại.

---

### US-02: Tự động ghép Sub cứng vào file Video MP4 (Auto-burn Hardsub)
- **ID:** `US-02`
- **As a:** Chuyên viên Vận hành nội dung
- **I want to:** Tùy chọn tự động dán phụ đề cứng tiếng Việt vào file MP4 ngay trong quá trình tải phim
- **So that:** Sau khi tải hoàn tất, tôi có ngay 1 file MP4 đã có phụ đề hoàn chỉnh, không cần mở Premiere hay CapCut chèn sub thủ công.

#### Acceptance Criteria:
- **AC1: Bật tùy chọn Auto-burn sub khi tải tập phim (Happy Path)**
  - **Given** Chuyên viên chọn tải 1 tập hoặc tải toàn bộ danh sách tập của phim
  - **And** Checkbox `[x] Tự động gắn sub cứng vào video` đang được tích chọn
  - **When** Tool tiến hành tải video và file sub về
  - **Then** Hệ thống tự động gọi thư viện xử lý video (FFmpeg) chạy ngầm để burn sub vào video
  - **And** File đầu ra tại thư mục Downloads là 1 file MP4 duy nhất đã có sub tiếng Việt dán sẵn vào video.

- **AC2: Vị trí và định dạng sub không bị che khuất trên màn hình dọc 9:16**
  - **Given** Video phim ngắn là khung hình dọc (9:16)
  - **When** Subtitle được burn vào video
  - **Then** Phụ đề được căn chỉnh lùi cách đáy màn hình (MarginV) một khoảng an toàn (tối thiểu 8-10% chiều cao màn hình) để không bị thanh tiến trình hoặc các nút chức năng của player che khuất
  - **And** Chữ có viền đen (Outline) hoặc shadow chống lóa mắt trên nền sáng.

- **AC3: Tùy chọn tải riêng file (Dành cho trường hợp muốn lấy file thô)**
  - **Given** Chuyên viên bỏ tích chọn checkbox `[ ] Tự động gắn sub cứng vào video`
  - **When** Bấm tải phim
  - **Then** Hệ thống tải về 2 file rời như hiện tại: file `video.mp4` gốc và file `sub.vtt` (hoặc kèm `.srt`).

- **AC4: Xử lý ngoại lệ khi lỗi phụ đề hoặc lỗi FFmpeg**
  - **Given** Quá trình burn sub bị lỗi do file sub rỗng hoặc FFmpeg gặp sự cố
  - **When** Quá trình tải kết thúc
  - **Then** Hệ thống vẫn lưu lại file `video.mp4` gốc và file sub rời, đồng thời hiển thị thông báo cảnh báo: "Không thể tự động ghép sub, đã lưu file video gốc và sub riêng lẻ".

---

### US-03: Tự động dịch phụ đề sang Tiếng Việt (Auto-Translate Subtitle)
- **ID:** `US-03`
- **As a:** Chuyên viên Vận hành nội dung
- **I want to:** Hệ thống tự động phát hiện và dịch phụ đề từ tiếng Anh (hoặc ngôn ngữ gốc) sang Tiếng Việt chuẩn
- **So that:** Tôi không phải mang file sub lên các trang mạng bên ngoài để dịch thủ công.

#### Acceptance Criteria:
- **AC1: Nguồn NetShort đã có sẵn phụ đề Tiếng Việt**
  - **Given** Phim trên NetShort đã có sẵn track subtitle tiếng Việt
  - **When** Tool crawl data
  - **Then** Hệ thống ưu tiên chọn tải ngay track tiếng Việt mà không cần gọi API dịch.

- **AC2: Nguồn NetShort chỉ có phụ đề Tiếng Anh (hoặc ngôn ngữ khác)**
  - **Given** Phim chỉ có track phụ đề tiếng Anh
  - **And** Cấu hình `Tự động dịch sang tiếng Việt` đang BẬT
  - **When** Tool tải xong file sub gốc
  - **Then** Hệ thống gọi API dịch (Google Translate API / OpenAI GPT / DeepL) để dịch nội dung phụ đề sang tiếng Việt
  - **And** Giữ nguyên chính xác 100% các mốc thời gian (timestamp) của file phụ đề.

---

### US-04: Cấu hình Style Subtitle (Font, Size, Màu sắc, Vị trí)
- **ID:** `US-04`
- **As a:** Admin / Quản trị viên Tool
- **I want to:** Tùy chỉnh các thông số hiển thị của Subtitle (Cỡ chữ, màu chữ, màu viền, độ cao)
- **So that:** Phim xuất ra đồng bộ nhận diện thương hiệu và dễ đọc trên các thiết bị di động.

#### Acceptance Criteria:
- **AC1: Lưu cấu hình mặc định**
  - **Given** Admin vào tab Cài đặt của tool
  - **When** Admin chọn Font chữ (VD: Arial, Montserrat), Size (VD: 18px), Màu chữ (Trắng), Màu viền (Đen), Vị trí đáy (Margin Bottom: 50px)
  - **Then** Hệ thống lưu cấu hình và áp dụng cho tất cả các lần burn sub tiếp theo.

---

## IV. GIẢI PHÁP KỸ THUẬT CHO BÀI TOÁN "TỰ ĐỘNG ADD SUB VÀO MP4" (PO / TECH LEAD)

### 1. Kiến trúc luồng xử lý tự động (Automated Pipeline)
```
[Crawl Video .mp4 + Sub .vtt]
         │
         ▼
[Kiểm tra ngôn ngữ Sub]
   ├── Đã là tiếng Việt ──> (Bỏ qua dịch)
   └── Là tiếng Anh/khác ──> [Auto-Translate API] ──> [Sub Tiếng Việt]
         │
         ▼
[Auto-Convert .vtt -> .srt/.ass] (Chuẩn hóa format cho encoder)
         │
         ▼
[FFmpeg Subtitles Filter (Run in background)]
   - Ghép chữ chết vào video
   - Giữ nguyên chất lượng hình ảnh & âm thanh (Fast preset, -c:a copy)
         │
         ▼
[Output: 1 File .mp4 duy nhất hoàn chỉnh có Sub Việt]
```

### 2. Lệnh FFmpeg thực thi mẫu (Dev có thể tích hợp ngay vào Tool)
Tích hợp sẵn binary `ffmpeg.exe` (khoảng 80MB) đi kèm vào thư mục của tool crawler. Khi tải xong, tool gọi lệnh ngầm qua shell:

```bash
ffmpeg -i "input_video.mp4" -vf "subtitles='subtitle_vi.srt':force_style='FontName=Arial,FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=1.5,Shadow=0,MarginV=50'" -c:a copy -preset ultrafast "output_subbed.mp4"
```
*Giải thích thông số quan trọng:*
- `FontSize=18`: Cỡ chữ vừa vặn màn hình điện thoại 9:16.
- `PrimaryColour=&H00FFFFFF`: Màu chữ trắng rõ ràng.
- `OutlineColour=&H00000000` & `Outline=1.5`: Viền chữ màu đen chống chìm chữ trên nền sáng.
- `MarginV=50`: Đẩy sub cách đáy 50px, tránh bị nút UI của ứng dụng che.
- `-c:a copy`: Sao chép nguyên vẹn luồng âm thanh gốc, không tốn thời gian encode lại tiếng.
- `-preset ultrafast`: Tối ưu tốc độ xuất video, 1 tập phim 2 phút render mất chưa tới **5 - 10 giây**.

---

## V. ĐỀ XUẤT THIẾT KẾ UI CHO TÍNH NĂNG SEARCH (SKILL DESIGNER)

Dựa trên ảnh giao diện hiện tại của **NetShort Downloader**:
- **Vị trí đặt thanh Search:** 
  - Đặt ngay trên thanh Header ngang trên cùng, nằm giữa ô dropdown `[ Theater  ▼ ]` và ô số trang `[ 1 ]` `[ Tải danh sách phim ]`.
  - Thiết kế: 
    - Chiều rộng: `280px - 320px`.
    - Placeholder: `🔍 Tìm tên phim hoặc Movie ID...`
    - Có nút `[x]` clear text nhanh.
    - Hỗ trợ phím tắt `Enter` để kích hoạt tìm kiếm ngay lập tức.
- **Bổ sung Checkbox tùy chọn:**
  - Nằm cạnh mục `Lưu tại: Downloads`:
  - Thêm checkbox: `☑️ Tự động ghép Sub cứng Tiếng Việt` (Mặc định được tích chọn).
