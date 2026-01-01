Write-Host "Starting external access tunnel..." -ForegroundColor Cyan

# Check if Docker is running
docker ps > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker is not running. Start Docker first." -ForegroundColor Red
    exit 1
}

# Check if ngrok is already running
$existingProcess = Get-Process ngrok -ErrorAction SilentlyContinue
if ($existingProcess) {
    Write-Host "Stopping existing ngrok process..." -ForegroundColor Yellow
    Stop-Process -Name ngrok -Force
    Start-Sleep -Seconds 2
}

# Your static domain from ngrok dashboard
$staticDomain = "unpleated-braxton-nondynastical.ngrok-free.dev"

# Start ngrok with static domain in the background
Write-Host "Starting ngrok tunnel..." -ForegroundColor Green
Start-Process -WindowStyle Hidden -FilePath "ngrok" -ArgumentList "http", "8080", "--domain=$staticDomain"

# Wait longer for ngrok to initialize
Write-Host "Waiting for ngrok to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

$maxRetries = 5
$retryCount = 0
$success = $false

while ($retryCount -lt $maxRetries -and -not $success) {
    try {
        $response = Invoke-RestMethod -Uri "http://127.0.0.1:4040/api/tunnels" -ErrorAction Stop
        $httpsUrl = $response.tunnels | Where-Object { $_.proto -eq "https" } | Select-Object -First 1 -ExpandProperty public_url

        if ($httpsUrl) {
            Write-Host "`n External Allure Reports URL (PERSISTENT):" -ForegroundColor Cyan
            Write-Host $httpsUrl -ForegroundColor Yellow
            Write-Host "`n Local URL: http://localhost:8080" -ForegroundColor Gray
            Write-Host "`n URL copied to clipboard!" -ForegroundColor Green
            Set-Clipboard -Value $httpsUrl
            $success = $true
        } else {
            throw "No HTTPS tunnel found"
        }
    } catch {
        $retryCount++
        if ($retryCount -lt $maxRetries) {
            Write-Host "Retry $retryCount/$maxRetries..." -ForegroundColor Yellow
            Start-Sleep -Seconds 3
        }
    }
}

if (-not $success) {
    Write-Host "`n Could not retrieve tunnel info after $maxRetries attempts" -ForegroundColor Red
    Write-Host "Check the ngrok web interface at: http://127.0.0.1:4040" -ForegroundColor Yellow
    Write-Host "`nTroubleshooting:" -ForegroundColor Cyan
    Write-Host "1. Verify ngrok is authenticated: ngrok config check" -ForegroundColor White
    Write-Host "2. Check if port 8080 is accessible: curl http://localhost:8080" -ForegroundColor White
    Write-Host "3. Verify your static domain is claimed in ngrok dashboard" -ForegroundColor White
}