# DIỄN GIẢI DANH SÁCH TÍNH NĂNG HIỆN CÓ CỦA HỆ THỐNG
## DỰ ÁN: NỀN TẢNG PHIM NGẮN PINEDRAMA (CLIENT APP & BACK OFFICE CMS)

> **Tài liệu tham chiếu UI Prototype:**
> - [Giao diện Back Office tương tác](file:///c:/Users/Admin/OneDrive/Desktop/Freelance/result_docs/wireframe_bo_interactive.html)
> - [Giao diện App Phim tương tác](file:///c:/Users/Admin/OneDrive/Desktop/Freelance/result_docs/wireframe_interactive.html)
> - **Mục đích:** Diễn giải chi tiết các chức năng hiện có trên giao diện để User/Khách hàng nắm bắt, kiểm tra và nghiệm thu sản phẩm.

---

## PHẦN 1: DIỄN GIẢI CHỨC NĂNG PHÂN HỆ APP / WEB CLIENT (NGƯỜI DÙNG)

Phân hệ dành cho khán giả xem phim trên điện thoại di động (hoặc trình duyệt web responsive) với trải nghiệm phim ngắn 100% miễn phí, vuốt lướt theo chiều dọc.

### 1. Màn Hình Trang Chủ & Khám Phá (Home Discover)
* **Logo nhận diện & định vị thương hiệu:** Hiển thị thương hiệu "🔥 PineDrama" cùng thông tin định vị nền tảng phim ngắn miễn phí.
* **Tìm kiếm phim:** Thanh tìm kiếm cho phép gõ từ khóa tên phim để tìm nhanh phim mong muốn.
* **Phân loại danh mục theo tab cuộn ngang:** Khán giả có thể vuốt ngang chọn các thể loại phim như *Cho Bạn, Hot Trend, Ngôn Tình, Chủ Tịch, Trả Thù...* để lọc nhanh danh sách phim theo sở thích.
* **Banner phim nổi bật (Hero Banner):** Hiển thị bộ phim hot nhất trang đầu với hình ảnh bắt mắt, tóm tắt thể loại, số tập và nút bấm *"▶ Xem Ngay"* để vào xem phim ngay lập tức.
* **Lưới phim thịnh hành (Trending Grid):** Trình bày các bộ phim theo dạng lưới 2 cột gọn gàng, thể hiện rõ: Ảnh poster dọc, Tên phim, Tổng số tập và Điểm đánh giá sao ⭐ (VD: 80 Tập • ⭐ 4.9).
* **Nút xem tất cả:** Điều hướng mở rộng danh sách phim cho từng chuyên mục.

---

### 2. Màn Hình Xem Phim Dọc (Vertical Short Drama Player)
* **Trình chiếu video khung dọc 9:16:** Tối ưu hóa cho thiết bị di động, phát video toàn màn hình theo trải nghiệm Reels/TikTok.
* **Thanh điều hướng nhanh phía trên (Top Overlay):**
  * Nút Quay lại (‹): Trở về màn hình trước đó.
  * Tên phim có thể bấm (clickable): Bấm thẳng vào tên phim để chuyển nhanh đến trang Chi Tiết Phim.
  * Hiển thị số thứ tự tập: Cho biết rõ đang xem tập mấy trên tổng số tập (VD: *Tập 12 / 80*).
  * Nhãn phụ đề (Sub: VI).
* **Phụ đề nổi thông minh (Floating Subtitles):** Đặt ở vị trí cao trên video, đảm bảo không bị che khuất bởi các nút điều khiển hay thanh tiến trình.
* **Cột tương tác nhanh bên phải:**
  * **Thả Tim (❤️):** Bấm để thích phim, đồng thời hệ thống tự động lưu phim này vào danh sách *Phim Yêu Thích* của cá nhân.
  * **Xem & Mở Bình Luận (💬):** Hiển thị số lượt bình luận (VD: 1.8K), bấm vào sẽ trượt bảng bình luận lên để đọc và chat.
* **Khung thông tin tập dưới đáy (Bottom Overlay):**
  * Tên phim và badge số tập tinh giản.
  * Nút *"Phát tất cả (80 tập)":* Xuất hiện khi khán giả lướt xem ngẫu nhiên, bấm vào sẽ mở toàn bộ danh sách tập của phim đó.
* **Thanh tiến trình phát (Progress Bar):** Đường line hiển thị tiến độ thời gian xem của tập phim hiện tại.
* **Cụm nút chuyển tập tiện lợi:**
  * Nút *‹ Tập Trước* để lùi lại tập vừa xem.
  * Nút nổi bật *Tập Sau (▶ Xem Tiếp)* để nhảy ngay sang tập kế tiếp chỉ với 1 chạm.
* **Tự động lưu tiến trình xem:** Ghi nhớ chính xác khán giả đang xem đến tập nào để lần sau vào có thể xem tiếp ngay.

---

### 3. Màn Hình Chi Tiết Phim (Drama Detail)
* **Ảnh nền Backdrop & Nút Back:** Thiết kế hiệu ứng kính mờ nghệ thuật kèm nút quay lại trang trước.
* **Thông tin tổng quan bộ phim:** Hiển thị Poster dọc, Tên phim, Thể loại và Điểm đánh giá trung bình ⭐ (VD: *9.8 / 10 từ 14.2K lượt đánh giá*).
* **Khung tự chấm điểm (Star Rating):** Khán giả có thể tự chạm chọn từ 1 đến 5 sao để gửi đánh giá chất lượng phim.
* **Cụm nút hành động chính:**
  * Nút *"▶ Xem Từ Tập 1":* Bắt đầu thưởng thức phim ngay từ tập mở đầu.
  * Nút *"❤️ Yêu Thích":* Lưu phim vào tủ phim cá nhân để xem lại sau.
* **Bộ chọn phần phim (Multi-Seasons Select):** Dropdown dành cho phim dài tập chia nhiều mùa (Phần 1, Phần 2, Ngoại truyện...). Khán giả chọn phần nào thì danh sách tập bên dưới sẽ đổi theo phần đó.
* **Lưới danh sách tập phim (Episodes Grid):** Hiển thị toàn bộ các tập (Tập 1 -> Tập 80). Bấm vào bất kỳ tập nào sẽ mở Player phát đúng tập đó.

---

### 4. Khung Bình Luận & Tương Tác (Comments Sheet)
* **Bảng trượt từ đáy màn hình (Bottom Sheet Modal):** Trượt lên mượt mà mà không làm gián đoạn việc phát video ở nền dưới.
* **Hiển thị tổng số bình luận:** Cập nhật số lượng bình luận theo thời gian thực (VD: 1,842 bình luận).
* **Danh sách bình luận chi tiết:** Thể hiện Avatar người bình luận, Họ tên, Thời gian đăng bài (VD: *15 phút trước*), Nội dung bình luận.
* **Thả tim bình luận:** Bấm like để tăng số lượt yêu thích cho bình luận hay.
* **Trả lời bình luận (Reply):** Bấm trả lời sẽ tự động gắn thẻ `@Tên_Người_Dùng` vào ô soạn thảo.
* **Khung gửi bình luận:** Hiển thị avatar của chính mình, ô gõ nội dung và nút *"Gửi"* để đăng bình luận tức thì.

---

### 5. Màn Hình Đăng Nhập / Đăng Ký (Authentication)
* **Tab chuyển đổi 2 chế độ:** Chuyển đổi nhanh giữa biểu mẫu [Đăng Nhập] và [Đăng Ký].
* **Đăng nhập tài khoản:** Đăng nhập bằng Số điện thoại hoặc Email + Mật khẩu, có liên kết "Quên mật khẩu".
* **Đăng ký tài khoản mới:** Đăng ký thành viên với Họ tên, Email, Mật khẩu, Xác nhận mật khẩu và Checkbox đồng ý Điều khoản chính sách.
* **Đăng nhập nhanh qua Google:** 1 chạm liên kết với tài khoản Google để vào xem phim không cần tạo mật khẩu rườm rà.

---

### 6. Màn Hình Hồ Sơ Cá Nhân & Tủ Phim (Profile & Library)
* **Thẻ thông tin cá nhân:** Hiển thị Avatar, Tên người dùng, Huy hiệu thành viên PineDrama, Mã ID người dùng và SĐT/Email liên kết.
* **Chỉnh sửa thông tin & Đổi Avatar:**
  * Chọn các ảnh đại diện mẫu có sẵn.
  * Tự tải ảnh cá nhân từ máy điện thoại lên.
  * Tự tạo avatar bằng 2 chữ cái viết tắt (Initials).
  * Chỉnh sửa Tên hiển thị và Số điện thoại/Email.
* **Tab "Lịch Sử Xem":** Lưu lại tất cả những bộ phim người dùng đã xem kèm số tập đang xem dở (VD: *Đã xem Tập 12/80*) và nút *"▶ Xem Tiếp"* để tiếp tục xem ngay.
* **Tab "Phim Yêu Thích":** Nơi lưu trữ các bộ phim người dùng đã bấm thả tim ❤️ để tiện cày phim dài ngày.
* **Đăng xuất:** Nút đăng xuất an toàn khỏi tài khoản khi không sử dụng.

---

### 7. Thanh Điều Hướng Đáy Màn Hình (Bottom Navigation Bar)
* Gồm 3 tab chính cố định dưới đáy màn hình:
  * **Trang Chủ:** Về trang khám phá nội dung.
  * **Xem Phim:** Chuyển nhanh vào màn hình xem phim dọc.
  * **Tài Khoản / Tôi:** Tự động nhận diện: Nếu chưa đăng nhập sẽ dẫn vào màn hình Đăng Nhập; nếu đã đăng nhập sẽ hiển thị Profile cá nhân.

---

## PHẦN 2: DIỄN GIẢI CHỨC NĂNG PHÂN HỆ BACK OFFICE (BO / CMS QUẢN TRỊ)

Phân hệ dành cho Ban Quản trị, Đội ngũ Biên tập nội dung (Content) và Bộ phận Vận hành quản lý toàn bộ hệ thống phim ngắn.

### 1. Cổng Đăng Nhập Quản Trị (Admin Login Portal)
* **Giao diện đăng nhập bảo mật:** Tách biệt hoàn toàn với App người dùng, có thương hiệu PineDrama BO v3.0.
* **Tính năng mật khẩu:** Có nút icon mắt (👁️) để ẩn/hiện mật khẩu tránh gõ sai, tính năng ghi nhớ đăng nhập 30 ngày.
* **Chức năng 1-Click Demo Login:** Hỗ trợ đăng nhập thử nghiệm nhanh bằng 1 click theo từng vai trò quản trị:
  * *Super Admin:* Toàn quyền hệ thống.
  * *Content Manager:* Chỉ quản lý danh sách phim, tập phim và danh mục.
  * *User Moderator:* Chỉ quản lý người dùng và thực hiện khóa tài khoản vi phạm.
* **Menu người dùng góc sidebar (Dropup):** Đổi tài khoản quản trị, Quản trị Admin và Đăng xuất khỏi hệ thống.

---

### 2. Dashboard Vận Hành Tổng Quan (Executive Dashboard)
* **Bộ lọc mốc thời gian:**
  * *⚡ Hôm Qua (D-1):* Xem số liệu đã chốt sổ trọn vẹn của ngày hôm trước (mặc định an toàn cho vận hành).
  * *🔴 Hôm Nay (Live):* Xem số liệu lưu lượng đang diễn ra theo thời gian thực.
  * *📅 Theo Tháng:* Dropdown chọn xem tổng hợp các tháng trong năm (Tháng 08, Tháng 07, Tháng 06...).
* **4 Thẻ chỉ số hiệu suất chính (KPI Cards):**
  * *Tổng lượt xem (Views):* Thống kê tổng lượt xem và % tăng trưởng so với kỳ trước.
  * *Thời lượng xem (Watch Time):* Tổng số giờ khán giả đã xem trên toàn hệ thống (VD: 82,450 Giờ).
  * *Người dùng hoạt động (DAU):* Số lượng user truy cập hoạt động mỗi ngày.
  * *Tỷ lệ xem hết bộ (100% Free):* Đo lường tỷ lệ khán giả xem trọn vẹn từ tập đầu đến tập cuối của bộ phim.
* **Biểu đồ lưu lượng truy cập theo 24 giờ (Hourly Traffic Chart):** Thể hiện trực quan các khung giờ xem phim từ 00:00 đến 23:59, làm nổi bật khung giờ vàng cao điểm (*Peak: 19:00 - 22:00*).
* **Bảng Top 5 Phim Hot nhất:** Thống kê 5 bộ phim có lượt xem cao nhất trong kỳ lọc kèm thể loại và số lượt view.
* **Nút xuất báo cáo Dashboard:** Xuất số liệu tổng quan phục vụ báo cáo nội bộ.

---

### 3. Quản Lý Danh Sách Phim (Dramas Management)
* **Bộ lọc và tìm kiếm phim:**
  * Ô tìm kiếm theo Tên bộ phim, Mã ID phim.
  * Lọc theo trạng thái gán thể loại: *Đã Gán Thể Loại* hoặc *Chưa Gán Thể Loại*.
  * Lọc theo trạng thái phát hành: *Đã Xuất Bản* hoặc *Tạm Ẩn*.
* **Bảng dữ liệu danh sách phim trực quan:**
  * Hiển thị: Checkbox chọn nhiều, STT, Ảnh Poster nhỏ, Tên bộ phim, Thể loại, Tổng số tập, Trạng thái, Cột thao tác.
* **Gán thể loại nhanh ngay trên dòng (Quick Add Category):** Bấm nút `[+]` ngay tại cột thể loại trên dòng bảng để mở bảng chọn thể loại gắn thêm trực tiếp mà không cần mở form chỉnh sửa.
* **Công tắc bật/tắt trạng thái phát hành (Toggle Switch):** Gạt công tắc trực tiếp trên dòng để đổi trạng thái giữa *🟢 Đã Xuất Bản* (hiện trên App) và *🔴 Tạm Ẩn* (ẩn khỏi App).
* **Thanh thao tác hàng loạt nổi (Floating Bulk Action Bar):** Khi tích chọn một hoặc nhiều bộ phim, một thanh công cụ nổi sẽ trượt lên từ đáy màn hình cung cấp các tác vụ:
  * Đếm số lượng phim đang được chọn.
  * *Gán Category đồng loạt:* Mở modal chọn thể loại để gắn hàng loạt cho tất cả các phim đã chọn.
  * *Xuất bản các phim đã chọn:* Kích hoạt hiển thị đồng loạt lên App.
  * *Xóa đã chọn:* Xóa đồng loạt các phim được đánh dấu.
* **Modal Tạo Mới & Chỉnh Sửa Phim (Create/Edit Drama Modal):**
  * **Thông tin chung:** Nhập tên bộ phim, chọn loại hình (*Phim Bộ* nhiều tập hoặc *Phim Lẻ* 1 tập duy nhất).
  * **Cấu hình Poster:** Dán link URL ảnh poster, có khung hiển thị xem trước ảnh ngay lập tức để kiểm tra link ảnh có hợp lệ hay không.
  * **Gán thể loại phim:** Chọn nhiều thể loại cùng lúc dưới dạng các nhãn chip, có thanh gõ tìm kiếm thể loại và nút xóa nhanh nhãn.
  * **Xử lý Phim Lẻ (Single Movie):** Chỉ cần dán duy nhất 1 đường link URL video master (.m3u8 hoặc .mp4), có nút phát thử video (▶️) để kiểm tra luồng stream.
  * **Xử lý Phim Bộ Đa Phần (Multi-Seasons & Episode Manager):**
    * Thêm/xóa các Phần phim (*Season 1, Season 2...*).
    * **Khung dán link tập phim hàng loạt (Bulk URLs Importer):** Cho phép copy-paste danh sách hàng chục/hàng trăm link video (mỗi dòng 1 link), có cấu hình số tập bắt đầu (VD: bắt đầu từ tập 1 hay tập 11), bấm *"⚡ Gán Phim"* hệ thống sẽ tự động tạo danh sách tập tuần tự trong 1 giây.
    * **Bảng danh sách tập phim:** Cho phép đổi tên từng tập, dán lại link tập lẻ, bật/tắt trạng thái từng tập, kéo thả chuột đổi thứ tự tập hoặc thêm/xóa tập lẻ.
  * **Tùy chọn lưu:** Cho phép chọn lưu ở dạng *⏸️ TẠM ẨN* (để chỉnh sửa tiếp) hoặc *💾 XUẤT BẢN* (phát hành ngay lên App).

---

### 4. Quản Lý Danh Mục / Thể Loại Phim (Category Management)
* **Bảng danh mục thể loại:** Hiển thị Thứ tự hiển thị, Tên danh mục, Số lượng phim đang thuộc danh mục, Trạng thái và Hành động.
* **Sắp xếp thứ tự bằng Kéo Thả Chuột (Drag & Drop):** Mỗi dòng có tay nắm `⠿`. Người quản trị chỉ cần giữ chuột kéo thả dòng lên hoặc xuống để thay đổi vị trí xuất hiện của Tab trên App. Hệ thống tự động cập nhật lại số thứ tự `#1, #2, #3...` tương ứng.
* **Xem nhanh danh sách phim theo danh mục:** Cột số lượng phim có nút bấm (VD: *🎬 28 Phim [Xem DS ↗️]*). Bấm vào sẽ mở popup hiển thị toàn bộ danh sách các bộ phim đang được gán thể loại này kèm ô tìm kiếm phim nhanh.
* **Bật/Tắt hiển thị danh mục:** Dùng công tắc Toggle để ẩn/hiện một thể loại khỏi thanh cuộn trên App người dùng.
* **Tạo mới danh mục:** Nhập tên thể loại mới và chọn trạng thái hiển thị.
* **Chỉnh sửa / Đổi tên & Xóa danh mục:** Sửa tên thể loại hiển thị hoặc xóa khỏi hệ thống.

---

### 5. Quản Lý Báo Cáo & Thống Kê Chi Tiết (Reports & Analytics)
* **Bộ lọc đa chiều nâng cao:**
  * Lọc xem theo khoảng ngày bất kỳ (Từ ngày ... Đến ngày ...).
  * Lọc xem theo từng tháng.
  * Lọc theo thể loại phim (Ngôn Tình, Trả Thù, Gia Đình, Tổng Tài...).
  * Lọc tìm đích danh một bộ phim theo tên hoặc ID.
* **4 Thẻ Mini KPI chốt kỳ lọc:** Tổng lượt xem trong kỳ, Phim có nhiều lượt xem nhất, Phim được khán giả yêu thích nhất (nhiều tim nhất) và Số lượng User hoạt động.
* **3 Phân hệ báo cáo chuyên sâu (Sub-tabs):**
  * **Sub-tab 1: Báo cáo hiệu suất từng bộ phim:** Thể hiện bảng xếp hạng phim có lượt xem cao nhất, mã ID, số tập, thể loại, số view chi tiết và số lượt thả tim.
  * **Sub-tab 2: Báo cáo hành vi & duy trì người dùng (User Retention Cohort):** Đo lường tỷ lệ khán giả quay lại app sau 1 ngày (D1 Retention: 58.4%), sau 7 ngày (D7 Retention: 34.8%), sau 30 ngày (D30 Retention) và thời lượng xem trung bình mỗi ngày của người dùng.
  * **Sub-tab 3: Báo cáo tỷ trọng thể loại:** Thống kê thể loại nào đang được xem nhiều nhất trên hệ thống (Tỉ lệ % lượt xem, Tổng view, Số lượng phim).
* **Nút xuất file báo cáo:** Hỗ trợ xuất dữ liệu đang lọc ra file Excel/CSV để lập báo cáo tài chính/vận hành.

---

### 6. Quản Lý Người Dùng & Khóa Tài Khoản (User Moderation)
* **Bộ lọc trạng thái tài khoản:** Lọc xem danh sách tài khoản đang *🟢 Hoạt Động* hoặc tài khoản đang *🔴 Bị Khóa*.
* **Tìm kiếm người dùng:** Tìm kiếm nhanh theo Mã User ID, Tên hiển thị, Địa chỉ Email hoặc lý do vi phạm.
* **Bảng thông tin người dùng:** Hiển thị User ID, Tên, Email, Hình thức đăng nhập (Google/SĐT), Ngày tạo tài khoản và Trạng thái.
* **Thao tác Khóa Tài Khoản (Ban Account):** Dành cho tài khoản vi phạm (spam link, bình luận tục tĩu...). Bấm nút *"🔒 Khóa Acc"* hệ thống sẽ chuyển trạng thái sang Bị Khóa, người này sẽ bị vô hiệu hóa quyền đăng nhập và bình luận trên App ngay lập tức.
* **Thao tác Mở Khóa Tài Khoản (Unban Account):** Dành cho tài khoản đã xử lý xong khiếu nại, bấm *"🔓 Mở Khóa Acc"* để cấp lại quyền hoạt động bình thường.
* **Xuất danh sách User bị khóa:** Nút xuất danh sách các tài khoản vi phạm ra file báo cáo.

---

### 7. Quản Trị Hệ Thống & Phân Quyền Admin (System Admin & RBAC)
* **Bảng danh sách tài khoản Quản trị viên (Admin Table):** Quản lý toàn bộ nhân sự nội bộ có quyền truy cập vào BO CMS, hiển thị: Avatar, Tên, Email, Vai trò, Quyền hạn chính, Trạng thái hoạt động, Thời gian và Địa chỉ IP đăng nhập cuối cùng.
* **Hệ thống 4 Vai trò định danh chuẩn (Standard RBAC Roles):**
  * **👑 Super Admin:** Toàn quyền quản trị cao nhất hệ thống, không thể bị khóa quyền hay xóa nhầm.
  * **🎬 Content Manager:** Chỉ có quyền kéo API, tạo phim, biên tập tập phim và quản lý danh mục.
  * **🛡️ User Moderator:** Chỉ có quyền xem danh sách người dùng và thực hiện khóa/mở khóa tài khoản.
  * **📊 Data Analyst:** Chỉ có quyền xem Dashboard thống kê và xuất các file báo cáo.
* **Cấp mới tài khoản Admin (Modal Create Admin):**
  * Nhập Họ tên, Email công việc, Mật khẩu khởi tạo.
  * Chọn Vai trò (Role).
  * **Ma trận phân quyền động:** Cho phép tích chọn chi tiết từng quyền hạn (Xem Dashboard, Tạo phim, Quản lý danh mục, Quản lý User, Quản lý Admin khác).
  * Tự động gửi thông tin tài khoản và mật khẩu đến email của nhân sự.
* **Đổi mật khẩu Admin:** Cập nhật lại mật khẩu mới cho bất kỳ quản trị viên nào khi cần thiết.
* **Khóa / Mở tài khoản Admin:** Khóa quyền đăng nhập của nhân sự khi nghỉ việc hoặc nghi vấn lộ tài khoản.
* **Xóa tài khoản Admin:** Xóa vĩnh viễn quyền truy cập của một quản trị viên khỏi hệ thống.
