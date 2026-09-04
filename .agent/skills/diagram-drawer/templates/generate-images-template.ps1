# ============================================================
# Script biên dịch sơ đồ Mermaid sang file ảnh PNG/SVG
# Sử dụng API công cộng: https://mermaid.ink
# ============================================================
# HƯỚNG DẪN: Thay đổi biến $diagramName bên dưới thành tên
# file sơ đồ của bạn (không cần phần mở rộng .mermaid)
# ============================================================

$diagramName = "{{tên-sơ-đồ}}"

# --- Không cần sửa gì bên dưới ---

# Read the mermaid file with UTF-8 encoding
$content = Get-Content -Path "diagrams/$diagramName.mermaid" -Encoding UTF8

# Filter out markdown code fences (lines containing ```)
$pureCodeLines = @()
foreach ($line in $content) {
    if ($line -notmatch '```') {
        $pureCodeLines += $line
    }
}
$pureCode = $pureCodeLines -join "`n"
$pureCode = $pureCode.Trim()

# Encode to base64 UTF-8
$bytes = [System.Text.Encoding]::UTF8.GetBytes($pureCode)
$base64 = [Convert]::ToBase64String($bytes)

# Make it URL-safe base64 without padding
$base64Safe = $base64.Replace('+', '-').Replace('/', '_').Replace('=', '')

# Define URLs with solid dark background (#121212)
# Dùng ${base64Safe} có ngoặc nhọn để tránh lỗi nhận diện biến PowerShell
$svgUrl = "https://mermaid.ink/svg/${base64Safe}?bgColor=121212"
$pngUrl = "https://mermaid.ink/img/${base64Safe}?bgColor=121212"

# Create diagrams directory if not exists
if (-not (Test-Path "diagrams")) {
    New-Item -ItemType Directory -Path "diagrams"
}

# Download SVG
Write-Output "Downloading SVG..."
try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $svgUrl -OutFile "diagrams/$diagramName.svg" -UserAgent "Mozilla/5.0"
    Write-Output "Saved diagrams/$diagramName.svg successfully!"
} catch {
    Write-Output "Failed to download SVG: $_"
}

# Download PNG
Write-Output "Downloading PNG..."
try {
    Invoke-WebRequest -Uri $pngUrl -OutFile "diagrams/$diagramName.png" -UserAgent "Mozilla/5.0"
    Write-Output "Saved diagrams/$diagramName.png successfully!"
} catch {
    Write-Output "Failed to download PNG: $_"
}
