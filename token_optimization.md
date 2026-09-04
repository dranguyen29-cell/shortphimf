# Token Optimization Guide

## Mục tiêu
Giảm lượng token tiêu thụ trong mỗi phiên làm việc mà vẫn duy trì chất lượng phân tích và phát triển.

## Các nguyên tắc chính
1. **Tóm tắt thay vì đọc toàn bộ file**
   - Với file lớn (PDF, DOCX, HTML, CSV) tạo file `*_summary.md` chứa các điểm chính, tiêu đề, cấu trúc và các đoạn mẫu cần thiết.
   - Trong các phiên sau chỉ `view_file` file tóm tắt này.
2. **Giới hạn phạm vi `view_file`**
   - Sử dụng `StartLine`/`EndLine` để đọc một đoạn cụ thể (ví dụ 1‑200 dòng) thay vì toàn bộ nội dung.
3. **Xóa lịch sử không cần thiết**
   - Sau khi một nhiệm vụ hoàn thành, xóa các `PLANNER_RESPONSE` và log không liên quan để giảm token nhập.
4. **Chuẩn hoá đường dẫn và metadata**
   - Dùng alias ngắn gọn (ví dụ `ldp-camera.pdf`) thay vì đường dẫn tuyệt đối dài.
5. **Giới hạn độ dài phản hồi**
   - Đặt độ dài tối đa cho câu trả lời (~150‑200 token) khi không cần mô tả chi tiết.
6. **Lưu hướng dẫn trong file**
   - Tạo file `token_optimization.md` trong thư mục `docs/` để mọi phiên làm việc có thể đọc nhanh (< 500 token).

## Quy trình thực hiện
1. **Tạo file tóm tắt** cho mỗi tài liệu lớn (PDF, HTML, v.v.).
2. **Cập nhật alias** trong các lệnh công cụ.
3. **Xóa lịch sử** khi nhiệm vụ kết thúc.
4. **Tham khảo guide** ở đầu mỗi phiên làm việc.

---

*Áp dụng ngay để tối ưu token cho các phiên làm việc sau.*
