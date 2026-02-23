#!/usr/bin/env bash
# ============================================================
# Crypto5min PolyTrader — Update Script (Linux / Mac)
# ============================================================
#
# HOW TO USE:
#   1. Download the new version ZIP from Whop
#   2. Unzip it into a NEW folder (don't overwrite the old one yet)
#   3. Open a terminal in the NEW folder
#   4. Run:  bash update.sh /path/to/old/folder
#
#   Example:
#     bash update.sh /root/crypto5min-polytrader-old
#
#   The script will:
#   - Copy your config/.env from the old folder (keeps your settings)
#   - Copy your logs/ folder (keeps your trade history)
#   - Stop the old container (if running)
#   - Build and start the new version
#
# ============================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo "=========================================="
echo "  Crypto5min PolyTrader — Update Script"
echo "=========================================="
echo ""

# --- Check for old path argument ---
OLD_PATH="$1"

if [ -z "$OLD_PATH" ]; then
    echo -e "${YELLOW}Usage:${NC}  bash update.sh /path/to/old/installation"
    echo ""
    echo "  Example (VPS):     bash update.sh /root/crypto5min-polytrader-old"
    echo "  Example (Desktop): bash update.sh ~/Desktop/crypto5min-polytrader-old"
    echo ""
    echo "This copies your settings and trade history from the old version."
    echo "If you already copied config/.env manually, just run: bash setup.sh"
    exit 1
fi

# --- Validate old path ---
if [ ! -d "$OLD_PATH" ]; then
    echo -e "${RED}ERROR:${NC} Folder not found: $OLD_PATH"
    echo "Make sure you typed the full path to your OLD installation folder."
    exit 1
fi

if [ ! -f "$OLD_PATH/docker-compose.yml" ]; then
    echo -e "${RED}ERROR:${NC} $OLD_PATH doesn't look like a Crypto5min PolyTrader folder."
    echo "It should contain docker-compose.yml, src/, config/, etc."
    exit 1
fi

# --- Check we're in the new folder ---
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}ERROR:${NC} Run this script from inside the NEW version folder."
    echo "  cd /path/to/new/crypto5min-polytrader"
    echo "  bash update.sh /path/to/old/folder"
    exit 1
fi

# --- Copy config/.env ---
if [ -f "$OLD_PATH/config/.env" ]; then
    mkdir -p config
    cp "$OLD_PATH/config/.env" config/.env
    echo -e "${GREEN}✓${NC} Copied config/.env (your settings)"
else
    echo -e "${YELLOW}⚠${NC} No config/.env found in old folder — you'll need to run the Setup Wizard"
fi

# --- Copy logs/ (trade history, state, runtime config) ---
if [ -d "$OLD_PATH/logs" ] && [ "$(ls -A "$OLD_PATH/logs" 2>/dev/null)" ]; then
    mkdir -p logs
    cp -r "$OLD_PATH/logs/"* logs/ 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Copied logs/ (trade history & state)"
else
    echo -e "${YELLOW}⚠${NC} No logs found in old folder — starting fresh"
fi

# --- Copy data/ (cached candles — saves re-download time) ---
if [ -d "$OLD_PATH/data" ] && [ "$(ls -A "$OLD_PATH/data" 2>/dev/null)" ]; then
    mkdir -p data
    cp -r "$OLD_PATH/data/"* data/ 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Copied data/ (cached candles)"
fi

# --- Stop old container ---
echo ""
echo "Stopping old container (if running)..."
(cd "$OLD_PATH" && docker compose down 2>/dev/null) || true
echo -e "${GREEN}✓${NC} Old container stopped"

# --- Build and start new version ---
echo ""
echo "Building and starting new version..."
echo "(First build may take 2-5 minutes)"
echo ""
docker compose up -d --build

echo ""
echo "=========================================="
echo -e "${GREEN}  ✓ Update complete!${NC}"
echo "=========================================="
echo ""
echo "  Dashboard: http://localhost:8602"
echo "  (or http://YOUR_SERVER_IP:8602 on a VPS)"
echo ""
echo "  Your settings, trade history, and data have been preserved."
echo "  Check the dashboard to verify everything looks right."
echo ""
echo "  Tip: You can safely delete the old folder now:"
echo "    rm -rf $OLD_PATH"
echo ""
