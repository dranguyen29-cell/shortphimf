---
name: doc-toolkit
description: >
  Bộ công cụ xử lý tài liệu chuyên dụng cho dự án FPT: convert PDF sang text,
  chuyển đổi Markdown sang Word (.doc/.docx), fix encoding UTF-8 tiếng Việt (mojibake),
  và tổng hợp nhiều tài liệu thành một file URD/SRS hoàn chỉnh.
  
  Kích hoạt skill này khi user đề cập đến bất kỳ thao tác nào sau:
  - "convert PDF", "đọc PDF", "trích xuất PDF", "PDF sang text/md/doc"
  - "chuyển md sang doc/docx/word", "tạo file word từ markdown"
  - "fix encoding", "fix UTF-8", "lỗi tiếng Việt", "ký tự bị lỗi", "mojibake"
  - "tổng hợp tài liệu", "gộp file", "merge tài liệu", "tổng hợp thành 1 file"
  - "tạo URD", "tạo SRS", "export ra doc", "lưu thành word"
  Không cần user nói đúng tên skill — chỉ cần có ý định xử lý tài liệu là dùng.
---

# Doc Toolkit — Bộ Công Cụ Xử Lý Tài Liệu

Skill này cung cấp các công cụ tái sử dụng để xử lý tài liệu, giúp tránh phải viết lại script
mỗi lần sử dụng. Tất cả script nằm trong thư mục `scripts/`.

## Tổng quan công cụ

| Tool | Script | Mô tả |
|------|--------|-------|
| PDF → TXT | `scripts/pdf_to_txt.ps1` | Đọc PDF qua browser, lưu text |
| MD → DOC | `scripts/md_to_doc.ps1` | Convert Markdown sang HTML-Word |
| Fix UTF-8 | `scripts/fix_utf8.ps1` | Fix mojibake CP1252 → UTF-8 |
| Tổng hợp tài liệu | `scripts/merge_docs.ps1` | Gộp nhiều file thành 1 |

---

## 1. PDF → TXT: Trích xuất nội dung PDF

**Khi nào dùng**: User muốn đọc nội dung file PDF và lưu thành `.txt` để xử lý tiếp.

**Cách dùng**:

Vì Windows thường không có `pdftotext`, cách tốt nhất là dùng browser để đọc PDF:

```
Dùng browser_subagent để:
1. Mở file PDF: file:///đường-dẫn/đến/file.pdf
2. Đọc toàn bộ nội dung trang
3. Trả về text đầy đủ
4. Lưu vào file .txt tương ứng
```

**Script PowerShell** (nếu có thư viện iTextSharp hoặc dùng COM Word):

```powershell
# Dùng script: scripts/pdf_to_txt.ps1
# Tham số: -PdfPath <đường dẫn PDF> -OutputPath <đường dẫn TXT>
powershell -ExecutionPolicy Bypass -File .agent/skills/doc-toolkit/scripts/pdf_to_txt.ps1 `
  -PdfPath "result_docs/file.pdf" `
  -OutputPath "result_docs/file.txt"
```

**Lưu ý quan trọng**:
- PDF dạng scan hình ảnh cần OCR (dùng browser để đọc visual content)
- PDF dạng text thuần thường đọc được qua browser
- Đặt tên file output theo pattern: `pdf<số>_<tên_ngắn>.txt`

---

## 2. MD → DOC: Chuyển Markdown sang Word

**Khi nào dùng**: User muốn export tài liệu Markdown thành file Word (`.doc` hoặc `.docx`).

**Hai phương pháp**:

### Phương pháp A: HTML-Word (khuyến nghị — không cần cài thêm)

Tạo file `.doc` thực chất là HTML với Word namespace. Microsoft Word đọc được hoàn hảo.

```powershell
# Dùng script: scripts/md_to_doc.ps1
powershell -ExecutionPolicy Bypass -File .agent/skills/doc-toolkit/scripts/md_to_doc.ps1 `
  -InputMd "result_docs/document.md" `
  -OutputDoc "result_docs/document.doc" `
  -TemplatePath ".agent/skills/ba-senior/templates/fpt_urd_template.doc"
```

**Cấu trúc HTML-Word chuẩn FPT**:
- Font body: Times New Roman 12pt
- Font heading: Arial (h1=#1f4e78, h2=#2e75b6, h3=#5b9bd5)
- Table styles: `header-table`, `data-table`, `usecase-table`
- Encoding: UTF-8 bắt buộc

### Phương pháp B: Dùng pandoc (nếu đã cài)

```powershell
pandoc -f markdown -t docx -o output.docx input.md --reference-doc=template.docx
```

**Quy tắc encoding bắt buộc** (tránh lỗi tiếng Việt):
```powershell
# ĐÚNG: Dùng WriteAllText với UTF-8 encoding
[System.IO.File]::WriteAllText($outputPath, $content, [System.Text.Encoding]::UTF8)

# SAI: Dùng Out-File thông thường (gây mojibake)
# $content | Out-File $outputPath  ← KHÔNG dùng cái này
```

---

## 3. Fix UTF-8: Sửa lỗi encoding tiếng Việt

**Khi nào dùng**: File `.doc`/`.html`/`.txt` có ký tự tiếng Việt bị lỗi kiểu:
- `MÃ£ hiá»‡u` thay vì `Mã hiệu`
- `â€"` thay vì `–`
- `chuáº©n` thay vì `chuẩn`

**Nguyên nhân**: File được ghi bằng UTF-8 nhưng đọc/lưu lại theo CP1252 (Windows-1252), gây double-encode.

**Script sửa lỗi**:

```powershell
# Dùng script: scripts/fix_utf8.ps1
powershell -ExecutionPolicy Bypass -File .agent/skills/doc-toolkit/scripts/fix_utf8.ps1 `
  -FilePath "đường-dẫn/file-bị-lỗi.doc"
# Script sẽ overwrite trực tiếp file gốc sau khi fix
```

**Logic fix (inline)**:
```powershell
try { [System.Text.Encoding]::RegisterProvider([System.Text.CodePagesEncodingProvider]::Instance) } catch {}

$bytes    = [System.IO.File]::ReadAllBytes($filePath)
$utf8Str  = [System.Text.Encoding]::UTF8.GetString($bytes)
$cp1252   = [System.Text.Encoding]::GetEncoding(1252)
$fixed    = [System.Text.Encoding]::UTF8.GetString($cp1252.GetBytes($utf8Str))

# Loại bỏ BOM nếu có
$idx = $fixed.IndexOf("<html")
if ($idx -gt 0) { $fixed = $fixed.Substring($idx) }

[System.IO.File]::WriteAllText($filePath, $fixed, [System.Text.Encoding]::UTF8)
```

---

## 4. Tổng hợp tài liệu: Gộp nhiều file thành 1 URD

**Khi nào dùng**: User có nhiều file (PDF text, MD, DOC) và muốn gộp thành 1 tài liệu hoàn chỉnh.

**Quy trình chuẩn**:

```
Bước 1: Đọc từng file nguồn theo thứ tự ưu tiên
  - File MD: đọc trực tiếp bằng view_file
  - File TXT (từ PDF): đọc trực tiếp bằng view_file  
  - File DOC: đọc bằng view_file (HTML-based)

Bước 2: Phân tích và map cấu trúc
  - Xác định section nào thuộc về module/chức năng nào
  - Tránh trùng lặp nội dung
  - Giữ nguyên toàn bộ nội dung — KHÔNG rút gọn

Bước 3: Gộp theo cấu trúc URD FPT chuẩn
  - REVISION HISTORY
  - I. GIỚI THIỆU (Mục đích, Phạm vi, Thuật ngữ)
  - II. TỔNG QUAN HỆ THỐNG (Business Flow, Danh sách chức năng, Permission Matrix)
  - III. ĐẶC TẢ CHI TIẾT CÁC CHỨC NĂNG (Use Case Specs từng module)
  - IV. YÊU CẦU PHI CHỨC NĂNG (Performance, UX, Security)
  - V. PHỤ LỤC

Bước 4: Export ra MD trước, sau đó convert sang DOC
```

**Lệnh tổng hợp nhanh**:
```powershell
# Dùng script: scripts/merge_docs.ps1
powershell -ExecutionPolicy Bypass -File .agent/skills/doc-toolkit/scripts/merge_docs.ps1 `
  -InputFiles "file1.txt,file2.txt,file3.md" `
  -OutputMd "result_docs/output.md" `
  -OutputDoc "result_docs/output.doc"
```

---

## Checklist trước khi giao file cho user

- [ ] File `.doc` mở được bằng Microsoft Word không bị lỗi format
- [ ] Tiếng Việt hiển thị đúng, không có ký tự lạ kiểu `Ã`, `â€`
- [ ] File có `<meta charset="utf-8">` trong `<head>`
- [ ] Sử dụng đúng template FPT (font, màu heading, table styles)
- [ ] Nội dung đầy đủ, không bị cắt bớt so với source

---

## Scripts reference

Xem chi tiết từng script trong thư mục `scripts/`:
- `pdf_to_txt.ps1` — Trích xuất PDF sang TXT
- `md_to_doc.ps1` — Convert MD sang HTML-Word
- `fix_utf8.ps1` — Sửa lỗi encoding UTF-8
- `merge_docs.ps1` — Tổng hợp nhiều file thành 1

---

## Tips & Gotchas

### Tránh lỗi encoding khi tạo file bằng PowerShell here-string

```powershell
# VẤN ĐỀ: PowerShell here-string @"..."@ có thể gây lỗi encoding với tiếng Việt
# GIẢI PHÁP: Luôn dùng WriteAllText với UTF-8 encoding rõ ràng
[System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)
```

### Khi file DOC quá lớn (>5MB), dùng MD trước

Tạo file `.md` hoàn chỉnh trước, sau đó convert sang `.doc` để tránh lỗi memory/timeout.

### PDF scan vs PDF text

- **PDF text thuần**: Dùng browser_subagent đọc nội dung DOM
- **PDF scan (hình ảnh)**: Phải dùng OCR — có thể dùng browser để đọc text được render bởi PDF viewer

### Thứ tự ưu tiên khi tổng hợp

Nếu có thông tin trùng lặp giữa các file, ưu tiên theo thứ tự:
1. File mới nhất (timestamp cao hơn)
2. File có version cao hơn (v1.1 > v1.0)
3. File có nhiều chi tiết hơn
