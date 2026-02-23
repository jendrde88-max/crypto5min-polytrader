# ============================================================
# Crypto5min PolyTrader — Update Script (Windows PowerShell)
# ============================================================
#
# HOW TO USE:
#   1. Download the new version ZIP from Whop
#   2. Unzip it into a NEW folder (don't overwrite the old one)
#   3. Open PowerShell in the NEW folder
#   4. Run:  .\update.ps1 -OldPath "C:\path\to\old\folder"
#
#   Example:
#     .\update.ps1 -OldPath "C:\Users\You\Desktop\crypto5min-polytrader-old"
#
#   The script will:
#   - Copy your config/.env from the old folder (keeps your settings)
#   - Copy your logs/ folder (keeps your trade history)
#   - Stop the old container (if running)
#   - Build and start the new version
#
# ============================================================

Param(
  [Parameter(Mandatory=$false)]
  [string]$OldPath
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Crypto5min PolyTrader - Update Script"   -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# --- Check for old path argument ---
if (-not $OldPath) {
    Write-Host "Usage:" -ForegroundColor Yellow -NoNewline
    Write-Host "  .\update.ps1 -OldPath `"C:\path\to\old\folder`""
    Write-Host ""
    Write-Host "  Example:"
    Write-Host "    .\update.ps1 -OldPath `"C:\Users\You\Desktop\crypto5min-polytrader-old`""
    Write-Host ""
    Write-Host "This copies your settings and trade history from the old version."
    Write-Host "If you already copied config\.env manually, just run: docker compose up -d --build"
    exit 1
}

# --- Validate old path ---
if (-not (Test-Path $OldPath)) {
    Write-Host "ERROR: " -ForegroundColor Red -NoNewline
    Write-Host "Folder not found: $OldPath"
    Write-Host "Make sure you typed the full path to your OLD installation folder."
    exit 1
}

if (-not (Test-Path (Join-Path $OldPath "docker-compose.yml"))) {
    Write-Host "ERROR: " -ForegroundColor Red -NoNewline
    Write-Host "$OldPath doesn't look like a Crypto5min PolyTrader folder."
    Write-Host "It should contain docker-compose.yml, src\, config\, etc."
    exit 1
}

# --- Check we're in the new folder ---
if (-not (Test-Path "docker-compose.yml")) {
    Write-Host "ERROR: " -ForegroundColor Red -NoNewline
    Write-Host "Run this script from inside the NEW version folder."
    Write-Host "  cd C:\path\to\new\crypto5min-polytrader"
    Write-Host "  .\update.ps1 -OldPath `"C:\path\to\old\folder`""
    exit 1
}

# --- Copy config/.env ---
$oldEnv = Join-Path $OldPath "config\.env"
if (Test-Path $oldEnv) {
    New-Item -ItemType Directory -Force -Path "config" | Out-Null
    Copy-Item -Force -Path $oldEnv -Destination "config\.env"
    Write-Host "  OK " -ForegroundColor Green -NoNewline
    Write-Host "Copied config\.env (your settings)"
} else {
    Write-Host "  !! " -ForegroundColor Yellow -NoNewline
    Write-Host "No config\.env found in old folder - you'll need to run the Setup Wizard"
}

# --- Copy logs/ (trade history, state, runtime config) ---
$oldLogs = Join-Path $OldPath "logs"
if ((Test-Path $oldLogs) -and (Get-ChildItem $oldLogs -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0) {
    New-Item -ItemType Directory -Force -Path "logs" | Out-Null
    Copy-Item -Recurse -Force -Path (Join-Path $oldLogs "*") -Destination "logs\" -ErrorAction SilentlyContinue
    Write-Host "  OK " -ForegroundColor Green -NoNewline
    Write-Host "Copied logs\ (trade history & state)"
} else {
    Write-Host "  !! " -ForegroundColor Yellow -NoNewline
    Write-Host "No logs found in old folder - starting fresh"
}

# --- Copy data/ (cached candles) ---
$oldData = Join-Path $OldPath "data"
if ((Test-Path $oldData) -and (Get-ChildItem $oldData -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0) {
    New-Item -ItemType Directory -Force -Path "data" | Out-Null
    Copy-Item -Recurse -Force -Path (Join-Path $oldData "*") -Destination "data\" -ErrorAction SilentlyContinue
    Write-Host "  OK " -ForegroundColor Green -NoNewline
    Write-Host "Copied data\ (cached candles)"
}

# --- Stop old container ---
Write-Host ""
Write-Host "Stopping old container (if running)..."
try {
    Push-Location $OldPath
    docker compose down 2>$null
    Pop-Location
} catch {
    Pop-Location -ErrorAction SilentlyContinue
}
Write-Host "  OK " -ForegroundColor Green -NoNewline
Write-Host "Old container stopped"

# --- Build and start new version ---
Write-Host ""
Write-Host "Building and starting new version..."
Write-Host "(First build may take 2-5 minutes)"
Write-Host ""
docker compose up -d --build

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  Update complete!"                        -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Dashboard: http://localhost:8602"
Write-Host "  (or http://YOUR_SERVER_IP:8602 on a VPS)"
Write-Host ""
Write-Host "  Your settings, trade history, and data have been preserved."
Write-Host "  Check the dashboard to verify everything looks right."
Write-Host ""
Write-Host "  Tip: You can safely delete the old folder now."
Write-Host ""
