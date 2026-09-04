$envFile = Join-Path $PSScriptRoot ".env"
$token = ""
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match "^SUNO_TOKEN=(.*)$") { $token = $matches[1].Trim() }
    }
}

$headers = @{
    "Authorization" = "Bearer $token"
    "User-Agent"    = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    "Content-Type"  = "application/json"
    "Origin"        = "https://suno.com"
    "Referer"       = "https://suno.com/create"
}

$outputDir = Join-Path $PSScriptRoot "music_output"
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

Write-Host "=== SUNO AI LOFI GENERATOR ===" -ForegroundColor Cyan

# Payload chuan Custom Mode + Instrumental
$payload = @{
    "custom_mode"       = $true
    "prompt"            = ""
    "tags"              = "lofi hip hop, chillhop, warm rhodes piano, soft vinyl crackle, mellow boom bap drums, relaxed jazz chords, nostalgic, cozy rain ambience, 75 bpm, smooth bassline"
    "title"             = "Midnight Rain and Coffee"
    "make_instrumental" = $true
    "mv"                = "chirp-v4"
} | ConvertTo-Json -Depth 3

Write-Host "Payload:" -ForegroundColor Gray
Write-Host $payload -ForegroundColor Gray
Write-Host "" -ForegroundColor Gray

$genUrl = "https://studio-api-prod.suno.com/api/generate/v2/"

Write-Host "Sending to: $genUrl" -ForegroundColor Cyan

try {
    $response = Invoke-WebRequest -Uri $genUrl -Method Post -Headers $headers -Body $payload -UseBasicParsing
    Write-Host "SUCCESS! Status: $($response.StatusCode)" -ForegroundColor Green
    $data = $response.Content | ConvertFrom-Json
    
    $clipIds = @($data.clips | ForEach-Object { $_.id })
    Write-Host "Suno is generating $($clipIds.Count) clip(s)..." -ForegroundColor Green
    Write-Host "Clip IDs: $($clipIds -join ', ')" -ForegroundColor Yellow

    # Polling loop
    $completedClips = @()
    $maxWaitSec = 180
    $startTime = Get-Date

    Write-Host "Waiting for rendering..." -ForegroundColor Cyan

    while (((Get-Date) - $startTime).TotalSeconds -lt $maxWaitSec) {
        Start-Sleep -Seconds 10

        $feedUrl = "https://studio-api-prod.suno.com/api/feed/?ids=$($clipIds -join ',')"
        $feedRaw = Invoke-WebRequest -Uri $feedUrl -Method Get -Headers $headers -UseBasicParsing
        $feedResponse = $feedRaw.Content | ConvertFrom-Json

        foreach ($clip in $feedResponse) {
            $clipTitle = $clip.title
            $clipStatus = $clip.status
            Write-Host "  -> [$clipTitle]: $clipStatus" -ForegroundColor Gray

            if ($clipStatus -eq "complete" -and $clip.audio_url) {
                if ($completedClips -notcontains $clip.id) {
                    $completedClips += $clip.id
                    $cleanTitle = $clipTitle -replace '[\\/:*?"<>|]', '_'
                    $shortId = $clip.id.Substring(0, 6)
                    $filePath = Join-Path $outputDir "${cleanTitle}_${shortId}.mp3"

                    Write-Host "Downloading: $filePath" -ForegroundColor Green
                    Invoke-WebRequest -Uri $clip.audio_url -OutFile $filePath
                    Write-Host "SAVED: $filePath" -ForegroundColor Green
                }
            }
            elseif ($clipStatus -eq "error") {
                Write-Host "ERROR rendering clip $($clip.id)" -ForegroundColor Red
            }
        }

        if ($completedClips.Count -ge $clipIds.Count -and $clipIds.Count -gt 0) {
            Write-Host "==============================" -ForegroundColor Green
            Write-Host "ALL DONE! Files saved to: $outputDir" -ForegroundColor Green
            Write-Host "==============================" -ForegroundColor Green
            break
        }
    }

    if ($completedClips.Count -lt $clipIds.Count) {
        Write-Host "TIMEOUT: Some clips may still be rendering." -ForegroundColor Yellow
    }
}
catch {
    $statusCode = "N/A"
    $body = "N/A"
    if ($_.Exception.Response) {
        $statusCode = [int]$_.Exception.Response.StatusCode
        try {
            $stream = $_.Exception.Response.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($stream)
            $body = $reader.ReadToEnd()
        } catch {}
    }
    Write-Host "FAILED ($statusCode)" -ForegroundColor Red
    Write-Host "Response: $body" -ForegroundColor Red
    Write-Host "Exception: $($_.Exception.Message)" -ForegroundColor Red
}
