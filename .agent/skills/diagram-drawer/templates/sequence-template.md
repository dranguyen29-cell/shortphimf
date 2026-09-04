# Sơ đồ Sequence Diagram: {{TÊN_SƠ_ĐỒ}}

{{MÔ_TẢ_NGẮN_GỌN_LUỒNG_HOẠT_ĐỘNG}}

![Sơ đồ Sequence Diagram](./{{tên-sơ-đồ}}.png)

## Mã nguồn Mermaid (Dùng để render ảnh)
```mermaid
%%{init: { 'theme': 'dark' } }%%
sequenceDiagram
    autonumber

    %% ══════════════════════════════════════════
    %% KHAI BÁO THỰC THỂ THAM GIA
    %% ══════════════════════════════════════════
    %% Dùng "actor" cho người dùng bên ngoài (hình người que 🧍)
    %% Dùng "participant" cho thành phần hệ thống (hộp chữ nhật 📦)
    actor User as "Người dùng"
    participant FE as "Frontend"
    participant BE as "Backend API"
    participant DB as "Database"

    %% ══════════════════════════════════════════
    %% PHÂN CẢNH 1: [TÊN PHÂN CẢNH] 
    %% ══════════════════════════════════════════
    Note over User, DB: {{TÊN PHÂN CẢNH 1 - CHỮ IN HOA}}

    %% --- Message đồng bộ (Sync): Nét liền ──▶ mũi tên đặc ---
    User->>FE: "Thực hiện hành động (vd: Đăng nhập)"

    %% --- Activation Box: Hộp kích hoạt trên lifeline ---
    %% Cách viết tắt: dùng "+" để activate, "-" để deactivate
    FE->>+BE: "Gọi API đồng bộ (POST /api/login)"

    %% --- Self-Message: Tự gọi chính mình ---
    BE->>BE: "Validate dữ liệu đầu vào"

    BE->>+DB: "Truy vấn DB (SELECT * FROM users)"

    %% --- Return Message: Nét đứt ╌╌▷ phản hồi ---
    DB-->>-BE: "Trả về kết quả query"

    %% --- Combined Fragment: ALT (Rẽ nhánh if-else) ---
    alt Đăng nhập thành công
        BE-->>FE: "200 OK - JWT Token"
        FE-->>User: "Chuyển hướng trang Dashboard"
    else Sai mật khẩu
        BE-->>FE: "401 Unauthorized"
        FE-->>User: "Hiển thị lỗi sai mật khẩu"
    end
    deactivate BE

    %% ══════════════════════════════════════════
    %% PHÂN CẢNH 2: [TÊN PHÂN CẢNH 2]
    %% ══════════════════════════════════════════
    Note over User, DB: {{TÊN PHÂN CẢNH 2 - CHỮ IN HOA}}

    %% --- Combined Fragment: OPT (Tùy chọn, chỉ if) ---
    opt Người dùng bật xác thực 2FA
        BE->>User: "Gửi mã OTP qua SMS"
        User->>BE: "Nhập mã OTP"
    end

    %% --- Combined Fragment: LOOP (Vòng lặp) ---
    loop Mỗi 30 giây
        FE->>BE: "Heartbeat ping"
        BE-->>FE: "Pong"
    end

    %% --- Combined Fragment: PAR (Song song) ---
    par Gửi email xác nhận
        BE-)User: "Gửi email bất đồng bộ (async ──▷)"
    and Ghi log hệ thống
        BE-)DB: "Insert audit log (async)"
    end

    %% --- Combined Fragment: BREAK (Ngoại lệ/Thoát) ---
    break Khi server quá tải
        BE-->>FE: "503 Service Unavailable"
    end

    %% --- Highlight Area: Rect tô nền nhóm message ---
    rect rgba(255, 165, 0, 0.1)
        Note over FE, BE: Vùng xử lý quan trọng
        FE->>+BE: "Thao tác nghiệp vụ chính"
        BE-->>-FE: "Kết quả xử lý"
    end
```

## Bảng ký hiệu sử dụng trong sơ đồ

| Ký hiệu | Cú pháp Mermaid | Ý nghĩa |
|:--------:|:----------------|:---------|
| 🧍 Actor | `actor X as "Tên"` | Người dùng / Hệ thống bên ngoài |
| 📦 Participant | `participant X as "Tên"` | Thành phần nội bộ hệ thống |
| ──▶ Sync | `A->>B: "msg"` | Gọi đồng bộ (chờ phản hồi) |
| ╌╌▶ Return | `A-->>B: "msg"` | Phản hồi / Trả về kết quả |
| ──▷ Async | `A-)B: "msg"` | Gọi bất đồng bộ (không chờ) |
| ↻ Self | `A->>A: "msg"` | Tự gọi nội bộ |
| ▮ Activate | `activate X` / `+` `-` | Hộp kích hoạt (đang xử lý) |
| [alt] | `alt ... else ... end` | Rẽ nhánh if-else |
| [opt] | `opt ... end` | Xử lý tùy chọn (chỉ if) |
| [loop] | `loop ... end` | Vòng lặp |
| [par] | `par ... and ... end` | Xử lý song song |
| [break] | `break ... end` | Ngoại lệ / Thoát |
| [critical] | `critical ... option ... end` | Vùng tới hạn |
| 📝 Note | `Note over/left/right` | Ghi chú / Dải phân cảnh |
| 🟦 Rect | `rect rgb(...) ... end` | Highlight vùng quan trọng |

## Giải thích luồng nghiệp vụ chi tiết

### 1. {{Phân đoạn nghiệp vụ 1}}
*   **Bước 1 - N:** {{Giải thích chi tiết hoạt động của các bước trong phân đoạn 1}}
*   **Bước N+1 - M:** {{Giải thích chi tiết hoạt động tiếp theo}}

### 2. {{Phân đoạn nghiệp vụ 2}}
*   **Bước M+1 - P:** {{Giải thích chi tiết hoạt động của các bước trong phân đoạn 2}}
*   **Bước P+1 - Q:** {{Giải thích chi tiết hoạt động tiếp theo}}
