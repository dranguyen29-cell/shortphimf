# PowerShell Script Kiểm Tra Tiến Trình Render Ngầm & Trạng Thái Hệ Thống
$Host.UI.RawUI.OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

py "c:\Users\hoang\OneDrive\Desktop\Freelance\suno_automation\check_status.py"
