param(
    [string]$AudioFile = "c:\Users\hoang\OneDrive\Desktop\Freelance\suno_automation\music_output\Midnight Rain & Coffee.mp3",
    [string]$ImageFile = "c:\Users\hoang\OneDrive\Desktop\Freelance\suno_automation\Image\lofi.jpg",
    [int]$DurationSeconds = 3600, # Default: 1 Hour
    [string]$OutputFile = "c:\Users\hoang\OneDrive\Desktop\Freelance\suno_automation\video_output\Midnight_Rain_Lofi_1Hour_UltraHD.mp4"
)

$outputDir = Split-Path -Path $OutputFile -Parent
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

$ffmpegCmd = "ffmpeg"
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    $wingetFfmpeg = Get-ChildItem -Path "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Filter "ffmpeg.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
    if ($wingetFfmpeg) { $ffmpegCmd = $wingetFfmpeg }
    else { Write-Host "ERROR: FFmpeg binary not found!" -ForegroundColor Red; exit 1 }
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "🚀 NATIVE FFMPEG PROGRESS & ETA TRACKER" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Audio Input : $AudioFile" -ForegroundColor Yellow
Write-Host "Image Input : $ImageFile" -ForegroundColor Yellow
Write-Host "Target Length: $DurationSeconds sec ($([Math]::Round($DurationSeconds/60)) min)" -ForegroundColor Yellow
Write-Host "Output File  : $OutputFile" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

# FFmpeg Command
$ffmpegArgs = @(
    "-y",
    "-loop", "1",
    "-i", "`"$ImageFile`"",
    "-stream_loop", "-1",
    "-i", "`"$AudioFile`"",
    "-t", "$DurationSeconds",
    "-filter_complex", "`"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,zoompan=z='min(zoom+0.0005,1.08)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080,format=yuv420p[v]`"",
    "-map", "[v]",
    "-map", "1:a",
    "-c:v", "libx264",
    "-preset", "faster",
    "-crf", "18",
    "-b:v", "15M",
    "-c:a", "aac",
    "-b:a", "320k",
    "-r", "60",
    "-progress", "pipe:1",
    "`"$OutputFile`""
)

$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $ffmpegCmd
$psi.Arguments = $ffmpegArgs -join " "
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $false
$psi.CreateNoWindow = $true

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $psi

$startTime = Get-Date
$process.Start() | Out-Null

$lastPercent = -1

while (-not $process.HasExited) {
    $line = $process.StandardOutput.ReadLine()
    if ($line -match "out_time_us=(\d+)") {
        $currentTimeSec = [Math]::Round([long]$matches[1] / 1000000)
        $percent = [Math]::Min(100, [Math]::Round(($currentTimeSec / $DurationSeconds) * 100))
        
        if ($percent -ne $lastPercent -and $percent -ge 0) {
            $lastPercent = $percent
            $elapsedSec = ((Get-Date) - $startTime).TotalSeconds
            
            if ($currentTimeSec -gt 0) {
                $speed = $currentTimeSec / $elapsedSec
                $remainingSec = [Math]::Max(0, [Math]::Round(($DurationSeconds - $currentTimeSec) / $speed))
                
                $etaMin = [Math]::Floor($remainingSec / 60)
                $etaSec = [Math]::Round($remainingSec % 60)
                $elapsedMin = [Math]::Floor($elapsedSec / 60)
                $elapsedSecRem = [Math]::Round($elapsedSec % 60)
                
                # Visual Progress Bar
                $barLength = 20
                $filledLength = [Math]::Round(($percent / 100) * $barLength)
                $bar = ("█" * $filledLength) + ("░" * ($barLength - $filledLength))
                
                Write-Host "`r[$bar] $percent% | Elapsed: ${elapsedMin}m${elapsedSecRem}s | Remaining (ETA): ${etaMin}m${etaSec}s | Speed: $([Math]::Round($speed, 1))x" -NoNewline -ForegroundColor Green
            }
        }
    }
}

$process.WaitForExit()
Write-Host ""

if (Test-Path $OutputFile) {
    $fileSize = (Get-Item $OutputFile).Length / 1MB
    $totalTime = ((Get-Date) - $startTime).TotalSeconds
    $totalMin = [Math]::Floor($totalTime / 60)
    $totalSecRem = [Math]::Round($totalTime % 60)
    
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host "🎉 RENDER FINISHED SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "Total Render Time : ${totalMin} min ${totalSecRem} sec" -ForegroundColor Yellow
    Write-Host "Output File Size  : $([Math]::Round($fileSize, 2)) MB" -ForegroundColor Yellow
    Write-Host "Output Location   : $OutputFile" -ForegroundColor Yellow
    Write-Host "==========================================================" -ForegroundColor Green
} else {
    Write-Host "❌ Render failed!" -ForegroundColor Red
}
