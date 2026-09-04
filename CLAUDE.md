# Project Rules — FPT BA/PO AI Platform

## Ngôn ngữ
- Luôn trả lời bằng **tiếng Việt** trong mọi tình huống, kể cả giải thích kỹ thuật.

## Quyền & File Operations
- Tự động accept tất cả thay đổi file (Write, Edit, Read) mà không hỏi lại.
- Tự động allow tất cả permissions mà không cần xác nhận.
- Không bao giờ prompt xin phép với bất kỳ tool nào trong project này.
- Tự động submit hết mà không cần xác nhận thêm.
- Tự động xóa các file dư thừa sau khi hoàn thành task.

## Bộ nhớ & Hội thoại
- Nếu phát hiện đoạn hội thoại hoặc thông tin không chính xác, xóa khỏi bộ nhớ ngay lập tức và không đọc lại.
- Không giữ lại context sai để tránh lan truyền lỗi.
- Luôn đọc file global rule (`C:\Users\Admin\.gemini\GEMINI.md`) khi bắt đầu làm task và khi mở hội thoại mới.

## Phân tích & Skills
- Luôn sử dụng skill **ba-senior** và/hoặc **product-owner** khi phân tích yêu cầu, thiết kế tính năng, hoặc đánh giá giải pháp.
- Mặc định áp dụng tư duy BA (Business Analysis) và PO (Product Owner) cho mọi task liên quan đến sản phẩm.
- Output ưu tiên: User Story (INVEST), Acceptance Criteria (Gherkin), Roadmap, và phân tích impact.
- Khi phân tích UI/UX phải sử dụng skill **designer**.

## Browser & Web Review
- Cho phép mở browser tự động mỗi khi có yêu cầu review qua trang web, không cần xác nhận.
- Khi cần view hoặc phân tích website, sử dụng Chrome profile **Long Nguyen**.

## Tiết kiệm Token & Sửa đổi Code (Quan trọng nhất)
- **Tuyệt đối không rollback hoặc ghi đè code cũ:** Phải luôn dùng tool đọc (`view_file`/`grep_search`) lấy nội dung file thực tế đang chạy trên máy khách trước khi thực hiện replace. Tránh tuyệt đối việc sử dụng code cũ trong lịch sử hội thoại (đặc biệt khi xảy ra history compaction) đè lên các chức năng đã sửa thành công ở lượt trước.
- **Tuyệt đối không viết lại code cũ:** Chỉ sửa đổi đúng (surgical edit) các dòng code cần thiết cho yêu cầu mới. Không được thay thế/ghi đè/hoàn tác toàn bộ hàm hay file nếu không liên quan.
- **Không phục hồi các đoạn code cũ** khi người dùng không yêu cầu.
- **Tối ưu hóa dung lượng truyền tải:** Hạn chế đọc/ghi các file quá lớn mà không có lý do cụ thể, chỉ thao tác trên phạm vi thay đổi hẹp nhất có thể.

## Tránh lỗi Encoding & Vỡ Layout (Quan trọng)
1. **Tránh sử dụng PowerShell để đọc/ghi/chỉnh sửa file**: Bắt buộc sử dụng trực tiếp các công cụ chuyên dụng của IDE (`replace_file_content`, `multi_replace_file_content`, `write_to_file`) để sửa đổi code nhanh nhất và tránh hoàn toàn lỗi encoding font tiếng Việt (Mojibake). Luôn bảo toàn định dạng UTF-8 không BOM.
2. **Sử dụng HTML Entities**: Ưu tiên sử dụng HTML Entities thập phân (Decimal) hoặc Hex (ví dụ: `&#272;`, `&rarr;`) cho các phần text tiếng Việt mới chèn vào HTML để tránh lỗi font chữ trong mọi môi trường render.
3. **Cân bằng thẻ div**: Khi thay đổi cấu trúc HTML, kiểm tra kỹ lưỡng các thẻ mở và đóng `<div>` để tránh làm vỡ layout. Nên chèn dựa trên các mốc dòng/nút bấm duy nhất thay vì dùng regex quá rộng dễ match nhầm vào script.
4. **Tự động Review sau khi code**: Sau khi thay đổi code, bắt buộc chạy `browser_subagent` mở trang web thực tế, click kiểm tra các tính năng tương tác, xem console logs để đảm bảo không xảy ra bất kỳ lỗi layout hay lỗi runtime JS nào trước khi bàn giao cho người dùng.
