# BẢNG DANH MỤC CHỨC NĂNG (FUNCTION LIST) & SO SÁNH NĂNG LỰC
## DỰ ÁN: CỔNG GAME HTML5 VTVGAME (`khogame.vtvgame.top`)
### ĐỐI CHUẨN THAM CHIẾU: GAMEVUI (`gamevui.vn`)

---

## I. THÔNG TIN TÀI LIỆU
- **Tên tài liệu:** Bảng Danh mục Chức năng So sánh & Đề xuất Bổ sung (Feature Comparison & Gap Analysis Function List)
- **Hệ thống phân tích:** `khogame.vtvgame.top` (Website mới - Giai đoạn MVP)
- **Hệ thống đối chuẩn (Benchmark):** `gamevui.vn` (Cổng game HTML5 dẫn đầu thị trường)
- **Vai trò thực hiện:** Senior Business Analyst & Product Owner
- **Mục tiêu:** Xác định toàn bộ các tính năng còn thiếu, định lượng khoảng trống năng lực (Gap), đề xuất giải pháp kỹ thuật/UI-UX và phân bổ lộ trình phát triển (MoSCoW Roadmap) nhằm nâng cấp VTVGame thành cổng game hàng đầu.

---

## II. PHÂN TÍCH CHUYÊN SÂU TRANG YÊU THÍCH (`/yeu-thich`) & HỆ THỐNG HEADER

Qua quá trình rà soát trực tiếp mã nguồn và luồng người dùng (User Flow) trên trang `https://khogame.vtvgame.top/yeu-thich` đối chiếu với `https://gamevui.vn/`, phát hiện các **khoảng trống lớn (Critical Gaps)** về UX:

1. **Rào cản Xác thực (Auth Guard Block):**
   - Trên VTVGame: Khi người dùng vãng lai (Guest) truy cập `/yeu-thich`, hệ thống lập tức cưỡng chế chuyển hướng (Redirect 307/308) sang trang `/dang-nhap?callbackUrl=...`. Điều này tạo ra rào cản tâm lý lớn khiến 70% người dùng bỏ trang.
   - Trên GameVui: Cho phép lưu game yêu thích và xem danh sách ngay lập tức ở chế độ Guest (lưu LocalStorage/Cookie), đồng thời chỉ khuyến khích đăng nhập để sao lưu đám mây.
2. **Thiếu Lối vào (Missing Header Entrypoint):**
   - Trên VTVGame: Thanh Header chỉ có Logo, Ô tìm kiếm và nút "Đăng nhập". Hoàn toàn không có nút/icon dẫn tới trang "Game yêu thích" hay "Game đã chơi".
   - Trên GameVui: Header tích hợp sẵn bộ 4 shortcut tiện ích: ❤️ **Yêu thích** (kèm số đếm), 🕒 **Đã chơi**, 🏆 **Bảng vàng**, 💡 **Mẹo chơi**.
3. **Cơ chế Lưu trữ Hybrid (Hybrid Sync Engine):**
   - Cần triển khai kiến trúc: Guest bấm ❤️ ➔ Lưu LocalStorage. Khi người dùng đăng nhập ➔ Hệ thống tự động đồng bộ (Merge) danh sách local lên Database của tài khoản.

---

## III. BẢNG FUNCTION LIST CHI TIẾT & SO SÁNH GAP ANALYSIS (28 CHỨC NĂNG)

| STT | Mã Chức Năng | Phân Hệ / Module | Tên Chức Năng | Mô Tả Nghiệp Vụ & Quy Tắc Logic | Hiện Trạng VTVGame | Hiện Trạng GameVui | Đánh Giá Khoảng Trống (Gap) | Mức Ưu Tiên (MoSCoW) | Lộ Trình (Sprint) | Giá Trị Mang Lại |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :--- | :---: | :---: | :--- |
| **1** | **F-PL-01** | Trình phát Game | **Chế độ Tắt đèn (Theater Mode)** | Click bật/tắt lớp phủ nền đen (overlay 85% opacity) phủ toàn bộ trang web, làm nổi bật duy nhất khung màn hình game giúp người chơi không bị phân tâm. | ❌ Chưa có |  Đã có | **Thiếu hoàn toàn (High Gap)** | **MUST HAVE** | Sprint 1 | Tăng tập trung, tăng thời gian chơi game on-site |
| **2** | **F-PL-02** | Trình phát Game | **Tải lại Game độc lập (Reload Frame)** | Nút bấm reset/load lại riêng thẻ `<iframe>` chứa game khi game bị đơ, lỗi mạng mà không phải F5 tải lại toàn bộ trang web. | ❌ Chưa có |  Đã có | **Thiếu hoàn toàn (High Gap)** | **MUST HAVE** | Sprint 1 | Giảm tỷ lệ thoát trang do lỗi game |
| **3** | **F-PL-03** | Trình phát Game | **Toàn màn hình thông minh (Smart Fullscreen)** | Tự động kích hoạt Fullscreen API, nhận diện game dọc (Portrait) hoặc game ngang (Landscape) và tự động khóa góc xoay màn hình trên thiết bị di động. | ⚠️ Có nút nhưng chưa tối ưu |  Đã có chuẩn | **Cần hoàn thiện (Medium Gap)** | **MUST HAVE** | Sprint 1 | Nâng cao trải nghiệm chơi trên Mobile/Tablet |
| **4** | **F-PL-04** | Trình phát Game | **Hiển thị Phím điều khiển Trực quan** | Hiển thị đồ họa trực quan các phím bấm cần thiết (WASD, Mũi tên, Phím cách, Click chuột, Chạm cảm ứng) thay vì văn bản tiếng Anh thô. | ⚠️ Text tiếng Anh thô |  Có icon phím rõ ràng | **Cần làm mới (Medium Gap)** | **SHOULD HAVE** | Sprint 2 | Giúp trẻ em/người mới chơi dễ dàng làm quen |
| **5** | **F-PL-05** | Trình phát Game | **Nút Phóng to / Thu nhỏ Khung chơi (Zoom)** | Cho phép người dùng chuyển đổi linh hoạt giữa các kích thước khung chơi: Kích thước mặc định (800x600), Kích thước Rộng (1024x768) hoặc Rạp phim. | ❌ Chưa có |  Đã có | **Thiếu (Medium Gap)** | **COULD HAVE** | Sprint 3 | Tùy biến theo kích thước màn hình PC/Laptop |
| **6** | **F-US-01** | Tài khoản & Giữ chân | **Lịch sử Game đã chơi gần đây** | Tự động ghi nhớ 20 game người dùng vừa bấm chơi. Lưu LocalStorage cho khách vãng lai và đồng bộ DB khi đăng nhập. Hiển thị ở Header & Trang chủ. | ❌ Chưa có |  Đã có (Mục Đã chơi) | **Cốt lõi còn thiếu (High Gap)** | **MUST HAVE** | Sprint 1 | Tăng tỷ lệ người dùng quay lại (Retention) thêm 35-45% |
| **7** | **F-US-02** | Tài khoản & Giữ chân | **Bộ sưu tập Game yêu thích Hybrid (Bookmarks)** | Cho phép Guest bấm ❤️ lưu LocalStorage không bắt login; Khi login tự merge vào DB; Có trang Dashboard `/yeu-thich` quản lý, lọc theo thể loại và xóa nhanh. | ⚠️ Ép login, chưa lưu Local |  Đã có chuẩn | **Cần tái cấu trúc (High Gap)** | **MUST HAVE** | Sprint 1 | Tạo thư viện cá nhân, loại bỏ rào cản ép đăng nhập |
| **8** | **F-US-03** | Tài khoản & Giữ chân | **Phím tắt Shortcut Tiện ích trên Header** | Bổ sung các icon truy cập nhanh trên Header: ❤️ Yêu thích (badge đếm số lượng), 🕒 Đã chơi, 🏆 Bảng vàng giúp người dùng mở ngay không cần tìm. | ❌ Chưa có lối vào |  Đầy đủ trên Header | **Thiếu lối vào UX (High Gap)** | **MUST HAVE** | Sprint 1 | Giúp người dùng tiếp cận tính năng yêu thích/đã chơi trong 1 click |
| **9** | **F-US-04** | Tài khoản & Giữ chân | **Đăng nhập Nhanh Đa nền tảng (Social SSO)** | Tích hợp đăng nhập 1-chạm không cần nhớ mật khẩu thông qua Google OAuth 2.0, Facebook Login và đặc biệt là Zalo Open API (thị trường VN). | ⚠️ Form đăng nhập email đơn giản |  Đã có Google/FB | **Cần hoàn thiện (High Gap)** | **MUST HAVE** | Sprint 2 | Tăng 80% tỷ lệ chuyển đổi đăng ký thành viên |
| **10** | **F-US-05** | Tài khoản & Giữ chân | **Hồ sơ Cá nhân & Quản lý Avatar (Profile)** | Trang xem thông tin cá nhân, chọn avatar nhân vật game ngộ nghĩnh, xem cấp độ, tổng điểm tích lũy, huy hiệu đạt được và lịch sử hoạt động. | ❌ Chưa có |  Đã có cơ bản | **Thiếu (Medium Gap)** | **SHOULD HAVE** | Sprint 2 | Gia tăng tính định danh cá nhân |
| **11** | **F-US-06** | Tài khoản & Giữ chân | **Điểm danh & Chuỗi Nhiệm vụ Ngày** | Cơ chế nhận thưởng Exp/Xu khi đăng nhập hàng ngày (Streak 7 ngày); Hoàn thành nhiệm vụ: Chơi 3 game, Chơi 15 phút, Chia sẻ 1 game. | ❌ Chưa có | ❌ Chưa có | **Điểm đột phá (New Competitive)** | **COULD HAVE** | Sprint 4 | Tạo thói quen truy cập hàng ngày cho người dùng |
| **12** | **F-DIS-01** | Tìm kiếm & Khám phá | **Live Search Autocomplete (Tìm tức thì)** | Khi gõ từ khóa, hiển thị dropdown tức thì (dưới 100ms) gồm: Ảnh thumbnail, Tên game, Thể loại chính, Lượt chơi và gợi ý từ khóa HOT. | ⚠️ Form submit cổ điển |  Đã có Autocomplete | **Cần nâng cấp (High Gap)** | **MUST HAVE** | Sprint 1 | Giảm thời gian tìm kiếm, tăng trải nghiệm mượt |
| **13** | **F-DIS-02** | Tìm kiếm & Khám phá | **Ma trận Phân loại Tags Nhân vật** | Bổ sung hàng trăm Tag theo nhân vật/chủ đề hot: Doraemon, Pikachu, Mario, Sonic, Nấu ăn Sara, Người que, Bắn súng Y8, Minecraft 2D... | ❌ Chỉ có 15 danh mục gốc |  Đầy đủ ma trận tag | **Khoảng trống lớn (High Gap)** | **SHOULD HAVE** | Sprint 2 | Bùng nổ Long-tail Keywords cho SEO Google |
| **14** | **F-DIS-03** | Tìm kiếm & Khám phá | **Bộ lọc Đa tiêu chí (Multi-Filter)** | Bộ lọc kết hợp: Nền tảng (Mobile/PC/Cảm ứng), Chế độ chơi (1 người/2 người), Đặc tính (Game nhẹ, Không cần mạng, Game 3D), Sắp xếp (Hot, Mới, Top Vote). | ❌ Chưa có | ⚠️ Có một phần | **Khoảng trống lớn (High Gap)** | **SHOULD HAVE** | Sprint 2 | Giúp người dùng lọc đúng game phù hợp thiết bị |
| **15** | **F-DIS-04** | Tìm kiếm & Khám phá | **Bố cục Hero Bento Grid / Featured Highlight** | Trang chủ biến thiên kích thước thẻ Game (Thẻ lớn 2x2 cho Game tiêu điểm HOT, Thẻ 1x1 cho Game thường) thay vì lưới đều tăm tắp. | ⚠️ Lưới đồng đều 1 kích thước |  Bố cục đa kích thước bắt mắt | **Cải tiến UI/UX (Medium Gap)** | **SHOULD HAVE** | Sprint 2 | Tạo điểm nhấn thị giác đẳng cấp, thu hút click |
| **16** | **F-GAM-01** | Gamification & Đua Top | **Bảng Vàng Đua Top Điểm (Leaderboard)** | Tích hợp Game SDK bắt điểm số (High Score). Lưu và xếp hạng Top người chơi theo Ngày, Tuần, Tháng, Mọi thời đại kèm vinh danh Top 1-2-3. | ❌ Chưa có |  Đã có (Bảng vàng) | **Tính năng cốt lõi (High Gap)** | **SHOULD HAVE** | Sprint 3 | Kích thích tính tranh đua, tăng tỷ lệ chơi lại |
| **17** | **F-GAM-02** | Gamification & Đua Top | **Bình luận Phân luồng & Khoe Kỷ lục** | Hệ thống comment hỗ trợ Reply theo thread, Like bình luận, chèn Sticker cảm xúc và đặc biệt là nút "Đính kèm ảnh chụp màn hình điểm số". | ⚠️ Textarea đơn giản |  Đã có comment | **Cần nâng cấp (Medium Gap)** | **SHOULD HAVE** | Sprint 3 | Xây dựng cộng đồng tương tác sôi nổi (UGC) |
| **18** | **F-GAM-03** | Gamification & Đua Top | **Cấp bậc Thành viên & Huy hiệu (Badges)** | Hệ thống tính điểm kinh nghiệm (Exp) khi chơi game, bình luận, đạt top điểm; Mở khóa danh hiệu (Tân thủ, Cao thủ, Thần đồng, Bất bại) và khung avatar. | ❌ Chưa có |  Đã có cấp độ | **Thiếu (Medium Gap)** | **COULD HAVE** | Sprint 4 | Tạo động lực gắn bó lâu dài với hệ sinh thái |
| **19** | **F-CON-01** | Nội dung Vệ tinh | **Chia sẻ Đa nền tảng 1-Chạm (Social Share)** | Bộ nút chia sẻ nhanh tối ưu cho Việt Nam: Zalo, Facebook Messenger, Telegram, Copy Link kèm lời mời chơi thách đấu bạn bè. | ❌ Chưa có |  Đã có (Zalo, FB, YT) | **Thiếu (Medium Gap)** | **MUST HAVE** | Sprint 1 | Kéo traffic Viral tự nhiên miễn phí |
| **20** | **F-CON-02** | Nội dung Vệ tinh | **Cung cấp Mã Nhúng Game (Embed Code)** | Tạo đoạn mã `<iframe src="...">` cho phép các blog cá nhân, website tin tức nhúng game về trang của họ, kèm logo bản quyền & link trỏ về VTVGame. | ❌ Chưa có |  Đã có | **Thiếu (Medium Gap)** | **SHOULD HAVE** | Sprint 2 | Tăng mạng lưới Backlink và nhận diện thương hiệu |
| **21** | **F-CON-03** | Nội dung Vệ tinh | **Video Clip Hướng dẫn Vượt màn (Walkthrough)** | Tích hợp tab nhúng video YouTube gameplay/mẹo phá đảo cho các tựa game giải đố khó ngay dưới màn hình chơi. | ❌ Chưa có |  Có kho video riêng | **Thiếu (Medium Gap)** | **COULD HAVE** | Sprint 3 | Tăng Time-on-page vượt trội, cải thiện SEO |
| **22** | **F-CON-04** | Nội dung Vệ tinh | **Chuyên mục Minigame Trắc nghiệm (Quiz)** | Hệ thống tạo và làm bài test trắc nghiệm vui (Kiểm tra IQ, Tính cách, Kiến thức học đường, Đố vui Anime) chấm điểm tự động và chia sẻ kết quả. | ❌ Chưa có |  Đã có kho trắc nghiệm | **Khoảng trống nội dung (Medium Gap)**| **COULD HAVE** | Sprint 4 | Thu hút tệp người dùng học sinh, sinh viên, Gen Z |
| **23** | **F-ADM-01** | Quản trị CMS | **Tự động Đồng bộ Game qua API (Auto-Sync)** | Module Backend tự động quét và nhập hàng nghìn game mới từ GameMonetize / GamePix / Famobi kèm tự động dịch metadata sang tiếng Việt. | ⚠️ Nhập thủ công/script đơn giản |  Hệ thống CMS tự động | **Cần hoàn thiện Backend** | **MUST HAVE** | Sprint 1 | Tiết kiệm 95% công sức vận hành nội dung |
| **24** | **F-ADM-02** | Quản trị CMS | **Quản lý Banner Quảng cáo & Tối ưu AdSense** | Quản lý vị trí đặt banner (Top header, Sidebar, Dưới game, Interstitial ad trước khi vào game) không làm che khuất trải nghiệm chơi. | ❌ Chưa có |  Hệ thống adbox tối ưu | **Sẵn sàng doanh thu** | **SHOULD HAVE** | Sprint 2 | Tối ưu hóa doanh thu quảng cáo bền vững |
| **25** | **F-ADM-03** | Quản trị CMS | **Thống kê & Phân tích Hành vi (Analytics)** | Báo cáo chi tiết: Game nào chơi nhiều nhất, thời gian chơi trung bình, tỷ lệ thoát trang, thiết bị truy cập, từ khóa tìm kiếm phổ biến. | ⚠️ Google Analytics cơ bản |  Báo cáo chuyên sâu | **Cần hoàn thiện** | **SHOULD HAVE** | Sprint 3 | Cung cấp dữ liệu để ra quyết định nhập game |
| **26** | **F-NFR-01** | Phi chức năng | **Tối ưu Cài đặt Ứng dụng Web (PWA Support)** | Cung cấp Service Worker, manifest chuẩn PWA cho phép người dùng click "Thêm vào Màn hình chính" để mở game như App Native trên iOS/Android. | ⚠️ Chưa có PWA chuẩn |  Đã có Manifest | **Cải tiến công nghệ (Medium Gap)** | **SHOULD HAVE** | Sprint 2 | Giữ chân người dùng Mobile không cần qua App Store |
| **27** | **F-NFR-02** | Phi chức năng | **Tối ưu Core Web Vitals & Lazy Load Iframe** | Chỉ load Iframe game khi người dùng bấm nút "Bấm để chơi", tải trước (preload) thumbnail WebP, chống Layout Shift (CLS = 0). | ⚠️ Tạm ổn | ⚠️ Tốc độ trung bình | **Lợi thế Next.js của VTVGame** | **MUST HAVE** | Sprint 1 | Vượt trội GameVui về tốc độ tải trang trên Google |
| **28** | **F-NFR-03** | Phi chức năng | **Giao diện Tối / Sáng (Dark / Light Mode)** | Tùy chọn giao diện nền tối bảo vệ mắt khi chơi game ban đêm, đồng bộ theo tùy chọn hệ điều hành của người dùng. | ❌ Mặc định Dark Theme | ⚠️ Mặc định Light Theme | **Trải nghiệm UI/UX mới** | **COULD HAVE** | Sprint 3 | Cá nhân hóa hiển thị, tiết kiệm pin cho OLED |

---

## IV. LỘ TRÌNH TRIỂN KHAI THEO SPRINT (SPRINT ROADMAP)

### 🔹 Sprint 1: Hoàn thiện Trải nghiệm Cốt lõi & Giữ chân Tức thì (Tuần 1 - 2)
- **Mục tiêu:** Khắc phục triệt để các nhược điểm của trình phát game, mở khóa tính năng Yêu thích & Đã chơi cho Guest, hoàn thiện thanh điều hướng Header.
- **Danh sách chức năng:**
  1. `F-PL-01`: Chế độ Tắt đèn (Theater Mode)
  2. `F-PL-02`: Nút Tải lại Game độc lập (Reload Frame)
  3. `F-PL-03`: Fullscreen API thông minh & xoay màn hình Mobile
  4. `F-US-01`: Lịch sử "Game đã chơi gần đây" (LocalStorage + Slider Home)
  5. `F-US-02`: Bộ sưu tập "Game yêu thích Hybrid" (Không chặn login, lưu LocalStorage)
  6. `F-US-03`: Thêm Shortcut Tiện ích trên Header (Icon ❤️, 🕒, 🏆)
  7. `F-DIS-01`: Live Search Autocomplete (Gợi ý tức thì)
  8. `F-CON-01`: Nút chia sẻ Zalo / FB / Messenger / Copy Link 1-chạm
  9. `F-NFR-02`: Tối ưu Lazy load iframe & WebP

### 🔹 Sprint 2: Xác thực Người dùng, Ma trận Phân loại & PWA (Tuần 3 - 4)
- **Mục tiêu:** Mở rộng traffic tự nhiên (SEO) và xây dựng hệ thống thành viên.
- **Danh sách chức năng:**
  1. `F-US-04`: Đăng nhập SSO (Google, Zalo, Facebook) & Tự động Merge dữ liệu LocalStorage
  2. `F-US-05`: Trang Profile thành viên & Quản lý Avatar
  3. `F-DIS-02`: Ma trận Tags nhân vật & Chủ đề chuyên sâu (Doraemon, Mario, Nấu ăn...)
  4. `F-DIS-03`: Bộ lọc Đa tiêu chí (1 người/2 người, Mobile/PC)
  5. `F-DIS-04`: Bố cục Bento Grid làm nổi bật Game Tiêu điểm
  6. `F-PL-04`: Icon hướng dẫn phím bấm trực quan
  7. `F-CON-02`: Tạo mã Embed nhúng game cho đối tác
  8. `F-NFR-01`: Hỗ trợ Progressive Web App (PWA) cài đặt màn hình chính

### 🔹 Sprint 3: Gamification, Đua Top & Tương tác Cộng đồng (Tuần 5 - 6)
- **Mục tiêu:** Tạo tính gắn kết và cạnh tranh cao độ giữa các người chơi.
- **Danh sách chức năng:**
  1. `F-GAM-01`: Bảng vàng Đua Top Điểm (Leaderboard SDK)
  2. `F-GAM-02`: Bình luận Phân luồng (Reply Thread) + Đính kèm ảnh điểm số
  3. `F-CON-03`: Nhúng Video Clip hướng dẫn chơi (Walkthrough)
  4. `F-ADM-02`: Quản lý Vị trí Quảng cáo (Banner/Interstitial)
  5. `F-ADM-03`: Dashboard Thống kê & Phân tích Hành vi
  6. `F-PL-05`: Nút Phóng to/Thu nhỏ khung chơi đa kích cỡ
  7. `F-NFR-03`: Tùy chọn giao diện Dark / Light Mode

### 🔹 Sprint 4: Hệ sinh thái Giải trí Vệ tinh & Tối ưu Nâng cao (Tuần 7 - 8)
- **Mục tiêu:** Đa dạng hóa trải nghiệm, vượt trội GameVui về hệ tính năng giữ chân.
- **Danh sách chức năng:**
  1. `F-US-06`: Chuỗi Điểm danh & Nhiệm vụ Ngày (Daily Quests)
  2. `F-GAM-03`: Cấp bậc Thành viên, Exp & Huy hiệu Danh hiệu (Badges)
  3. `F-CON-04`: Phân hệ Minigame Trắc nghiệm (Interactive Quiz)
