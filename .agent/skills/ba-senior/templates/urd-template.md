# USER REQUIREMENTS DOCUMENT (URD)

**Dự án:** [Tên Dự Án/Hệ Thống]
**Mã hiệu:** [Mã hiệu tài liệu]
**Phiên bản:** [X.X]
**Ngày:** [Ngày/Tháng/Năm]

---

## REVISION HISTORY

_[A]: Add – Thêm mới | [U]: Update – Cập nhật | [D]: Delete - Xóa_

| Date   | Version | Author | Change Description |
| :----- | :------ | :----- | :----------------- |
| [Ngày] | [V1.0]  | [Tên]  | [Mô tả thay đổi]   |

---

## MỤC LỤC

A. GIỚI THIỆU
B. TỔNG QUAN
C. ĐẶC TẢ CÁC CHỨC NĂNG
D. YÊU CẦU PHI CHỨC NĂNG
E. PHỤ LỤC (Nếu có)

---

## A. GIỚI THIỆU

### 1. Mục đích tài liệu

- Mô tả và phác thảo yêu cầu của người dùng cuối.
- Làm cơ sở cho việc phân tích, thiết kế, lập trình, kiểm thử và nghiệm thu.

### 2. Thông tin chung

| STT | HẠNG MỤC             | MÔ TẢ                                                        |
| :-- | :------------------- | :----------------------------------------------------------- |
| 1   | Giới thiệu tổng quan | [Mô tả ngắn gọn về dự án/tính năng mới]                      |
| 2   | Hiện trạng           | [Mô tả hệ thống hiện tại đang có gì hoặc đang gặp vấn đề gì] |
| 3   | Mục tiêu kỳ vọng     | [Các KPI hoặc hiệu quả mong muốn đạt được]                   |
| 4   | Phạm vi triển khai   | [Các module hoặc khu vực sẽ áp dụng thay đổi]                |

### 3. Thuật ngữ và viết tắt

| STT | THUẬT NGỮ   | MÔ TẢ                      |
| :-- | :---------- | :------------------------- |
| 1   | URD         | User Requirements Document |
| 2   | [Thuật ngữ] | [Giải thích]               |

---

## B. TỔNG QUAN

### 1. Sơ đồ luồng nghiệp vụ tổng quan (Business Flow)

[Chèn link hình ảnh hoặc mô tả sơ đồ luồng nghiệp vụ tổng quát]

### 2. Danh sách các chức năng

| STT | Chức năng       | Version | Loại (New/Update) | Mô tả tóm tắt    |
| :-- | :-------------- | :------ | :---------------- | :--------------- |
| 1   | [Tên chức năng] | [2.0]   | [New]             | [Mô tả ngắn gọn] |

### 3. Ma trận quyền (Permission Matrix)

| Chức năng     |  Role A   |  Role B   | Ghi chú |
| :------------ | :-------: | :-------: | :------ |
| [Chức năng 1] | View/Edit | View Only |         |

---

## C. ĐẶC TẢ CÁC CHỨC NĂNG

### I. [Tên Chức Năng/Module 1]

#### 1. Đặc tả Use Case (Use Case Specification)

##### a. Thuộc tính Use Case

| Thuộc tính         | Đặc tả chi tiết                                  |
| :----------------- | :----------------------------------------------- |
| **Description**    | [Chức năng cho phép người dùng...]               |
| **Actor**          | [Tác nhân thực hiện hành động]                   |
| **Trigger**        | [Sự kiện kích hoạt chức năng]                    |
| **Pre-condition**  | [Điều kiện tiên quyết để thực hiện]              |
| **Post-condition** | [Kết quả nhận được sau khi thực hiện thành công] |

##### b. Diễn giải các bước thực hiện (Step-by-step)

- **Bước 1:** Người dùng truy cập [Module] -> chọn [Tính năng].
- **Bước 2:** Hệ thống hiển thị [Giao diện danh sách/Form nhập].
- **Bước 3:** Người dùng thực hiện [Thêm / Sửa / Xóa].
- **Bước 4:** Người dùng nhập các thông tin: [Hình ảnh, Text...].
- **Bước 5:** Người dùng nhấn nút "Lưu".
- **Bước 6:** Hệ thống thực hiện validate dữ liệu, lưu vào DB và cập nhật hiển thị ngoài website.

#### 2. Business Rules

| Rule | Mô tả                                           |
| :--- | :---------------------------------------------- |
| BR01 | [Ví dụ: Trường A là bắt buộc, tối đa 100 ký tự] |
| BR02 | [Ví dụ: Điều kiện để hiển thị dữ liệu B là...]  |

#### 3. Mô tả màn hình (Screen Description)

| Field       | Kiểu dữ liệu     | Ràng buộc/Validation | Business Rule | Hành vi hệ thống           |
| :---------- | :--------------- | :------------------- | :------------ | :------------------------- |
| [Tên Field] | [Text/Select...] | [Bắt buộc/Format]    | [BRXX]        | [Mô tả khi User tương tác] |

#### 4. Các trường hợp lỗi & thông báo (Error Messages)

| Tình huống | Thông báo hiển thị     | Hành vi UI           |
| :--------- | :--------------------- | :------------------- |
| [Lỗi A]    | "[Nội dung thông báo]" | [Inline error/Popup] |

---

## D. CÁC YÊU CẦU PHI CHỨC NĂNG

- **Hiệu năng:** [Tốc độ phản hồi...]
- **Bảo mật:** [Ẩn thông tin cá nhân bằng dấu *...]
- **Trải nghiệm (UI/UX):** [Màu sắc, banner, hiển thị trên mobile/web...]

---

## E. PHỤ LỤC

- Wireframe/Mockup (Link)
- Tài liệu tham khảo khác.
