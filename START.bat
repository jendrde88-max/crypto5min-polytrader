@echo off
chcp 65001 >nul 2>&1

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║        Crypto5min PolyTrader — Windows Launcher          ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: ── Step 1: Check Docker ─────────────────────────────────────────
where docker >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker is not installed or not in PATH.
    echo.
    echo Please install Docker Desktop from:
    echo   https://www.docker.com/products/docker-desktop/
    echo.
    echo After installing, restart your computer and run this script again.
    echo.
    pause
    exit /b 1
)
echo [OK] Docker found.

:: Check if Docker daemon is running
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARN] Docker Desktop is not running. Starting it...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo Waiting for Docker to start (this may take 30-60 seconds)...
    :wait_docker
    timeout /t 5 /nobreak >nul
    docker info >nul 2>&1
    if %ERRORLEVEL% NEQ 0 goto wait_docker
    echo [OK] Docker Desktop is running.
)

:: ── Step 2: Check Docker Compose ─────────────────────────────────
docker compose version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker Compose not found.
    echo Please update Docker Desktop to the latest version.
    pause
    exit /b 1
)
echo [OK] Docker Compose ready.

:: ── Step 3: Create directories ───────────────────────────────────
if not exist "config" mkdir config
if not exist "logs" mkdir logs
if not exist "data" mkdir data
echo [OK] Directories ready.

:: ── Step 4: Create config/.env if missing ────────────────────────
if exist "config\.env" (
    echo [OK] Found config\.env
) else if exist ".env" (
    echo [WARN] Found legacy .env — copying to config\.env
    copy /Y .env config\.env >nul
) else if exist ".env.example" (
    copy /Y .env.example config\.env >nul
    echo [OK] Created config\.env from .env.example
) else (
    echo C5_DASHBOARD_PASSWORD=> config\.env
    echo C5_DASHBOARD_HOST=0.0.0.0>> config\.env
    echo C5_DASHBOARD_PORT=8601>> config\.env
    echo C5_DASHBOARD_PUBLIC_PORT=8602>> config\.env
    echo C5_SYMBOL=BTC-USD>> config\.env
    echo C5_GRANULARITY_SECONDS=300>> config\.env
    echo C5_LOOKBACK_DAYS=30>> config\.env
    echo C5_RETRAIN_MINUTES=60>> config\.env
    echo C5_CONFIDENCE_THRESHOLD=0.55>> config\.env
    echo C5_PAPER_ENABLED=true>> config\.env
    echo [OK] Created minimal config\.env
)

:: ── Step 5: Build and start ──────────────────────────────────────
echo.
echo Building and starting the container (first time may take 2-5 minutes)...
echo.
docker compose up -d --build

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Docker compose failed. Check the output above for details.
    echo Common fix: Make sure Docker Desktop is running and try again.
    pause
    exit /b 1
)

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║  [OK] Bot is running!                                    ║
echo ║                                                          ║
echo ║  Opening your browser to the Setup Wizard...             ║
echo ║  If it doesn't open, go to: http://localhost:8602        ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Wait a moment for the container to fully start
timeout /t 3 /nobreak >nul

:: Open the dashboard in the default browser
start http://localhost:8602

echo Press any key to close this window (the bot will keep running)...
pause >nul
