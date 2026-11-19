$ErrorActionPreference = "Stop"

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "  SYNAX-OMNI v6.0 & 3D Pixar-Tycoon Agent Office — Windows Setup  " -ForegroundColor Cyan
Write-Host "  (ReAct + NCBI PubMed + Groq LPU + Claude Artifacts Desktop App) " -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan

# 1. Check Python
$PythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $PythonCmd) {
    $PythonCmd = Get-Command py -ErrorAction SilentlyContinue
}
if (-not $PythonCmd) {
    Write-Host "[!] Python bulunamadi. Lutfen https://python.org adresinden Python 3.10+ kurun." -ForegroundColor Yellow
    exit 1
}

$InstallDir = Join-Path $env:USERPROFILE ".synax-desktop"
Write-Host "--> SYNAX-OMNI v6.0 kuruluyor: $InstallDir" -ForegroundColor Yellow

if (Test-Path $InstallDir) {
    try {
        Stop-Process -Name "python" -ErrorAction SilentlyContinue
        Remove-Item -Recurse -Force $InstallDir -ErrorAction SilentlyContinue
    } catch {}
}

# 2. Clone latest repository
git clone --depth 1 https://github.com/ofaemd-creator/synax-agent-office.git $InstallDir

# 3. Create Desktop shortcut for SYNAX Studio
$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "SYNAX Studio v6.0.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -Command `"Start-Process '$PythonCmd' -ArgumentList '$InstallDir\src\synax\agent_office.py --serve --port 8795' -WindowStyle Hidden; Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:8795'`""
$Shortcut.Description = "SYNAX-OMNI v6.0 3D Pixar-Tycoon Agent Office"
$Shortcut.Save()
Write-Host "--> Masaustu kisayolu olusturuldu: SYNAX Studio v6.0.lnk" -ForegroundColor Green

# 4. Start local daemon and open browser
Start-Process $PythonCmd -ArgumentList "$InstallDir\src\synax\agent_office.py --serve --port 8795" -WindowStyle Hidden
Start-Sleep -Seconds 2
Start-Process "http://127.0.0.1:8795"

Write-Host "==================================================================" -ForegroundColor Green
Write-Host "  TEBRIKLER! SYNAX-OMNI v6.0 bilgisayarinizda basariyla baslatildi!" -ForegroundColor Green
Write-Host "  Canli Yerel Arayuz: http://127.0.0.1:8795" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Green
