# Script Mở Chrome với Cổng Debug 9222 để Tự Động Hóa Trực Tiếp Trên Màn Hình
$Host.UI.RawUI.OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
if (-not (Test-Path $chromePath)) {
    $chromePath = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
}

Write-Host "🌐 Đang khởi động Chrome với Cổng Remote Debugging Port 9222..." -ForegroundColor Cyan
Start-Process -FilePath $chromePath -ArgumentList "--remote-debugging-port=9222", "https://suno.com/create"
Write-Host "✅ Đã mở Suno.com trên Chrome! Bây giờ mọi lệnh Automation sẽ điền trực tiếp trên màn hình này." -ForegroundColor Green
