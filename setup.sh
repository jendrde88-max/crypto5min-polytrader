#!/usr/bin/env bash
set -euo pipefail

# ── Colour helpers ────────────────────────────────────────────────
G='\033[0;32m'; Y='\033[1;33m'; R='\033[0;31m'; NC='\033[0m'
ok()   { echo -e "${G}✔${NC} $*"; }
warn() { echo -e "${Y}!${NC} $*"; }
fail() { echo -e "${R}✖${NC} $*"; exit 1; }

echo ""
echo -e "${G}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${G}║        Crypto5min PolyTrader — One-Click Setup           ║${NC}"
echo -e "${G}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# ── Step 1: Docker ────────────────────────────────────────────────
if command -v docker &>/dev/null; then
  ok "Docker is already installed ($(docker --version | head -c 40))"
else
  warn "Docker not found — installing…"
  if [ -f /etc/debian_version ] || grep -qi ubuntu /etc/os-release 2>/dev/null; then
    apt-get update -qq
    apt-get install -y -qq ca-certificates curl gnupg lsb-release >/dev/null
    install -m 0755 -d /etc/apt/keyrings
    DISTRO_ID="$(. /etc/os-release && echo "$ID")"
    curl -fsSL "https://download.docker.com/linux/${DISTRO_ID}/gpg" \
      | gpg --dearmor -o /etc/apt/keyrings/docker.gpg 2>/dev/null
    chmod a+r /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
      https://download.docker.com/linux/${DISTRO_ID} \
      $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
    apt-get update -qq
    apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-compose-plugin >/dev/null
    ok "Docker installed via apt"
  elif [ -f /etc/redhat-release ]; then
    yum install -y -q yum-utils >/dev/null
    yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo >/dev/null
    yum install -y -q docker-ce docker-ce-cli containerd.io docker-compose-plugin >/dev/null
    systemctl start docker && systemctl enable docker
    ok "Docker installed via yum"
  else
    fail "Unsupported OS. Please install Docker manually: https://docs.docker.com/get-docker/"
  fi
fi

# ── Step 2: Docker Compose ────────────────────────────────────────
if docker compose version &>/dev/null; then
  ok "Docker Compose plugin ready"
elif command -v docker-compose &>/dev/null; then
  ok "docker-compose standalone found"
  # Create a shim so 'docker compose' works
  echo '#!/bin/sh' > /usr/local/bin/docker-compose-shim
  echo 'exec docker-compose "$@"' >> /usr/local/bin/docker-compose-shim
  chmod +x /usr/local/bin/docker-compose-shim
else
  fail "Docker Compose not found. Install: https://docs.docker.com/compose/install/"
fi

# ── Step 3: Directories ──────────────────────────────────────────
mkdir -p logs data config
ok "Directories ready (logs/ data/ config/)"

# ── Step 4: .env config ──────────────────────────────────────────
if [ -f config/.env ]; then
  ok "Found config/.env"
elif [ -f .env ]; then
  warn "Found legacy .env — moving it to config/.env"
  cp .env config/.env
else
  if [ -f .env.example ]; then
    cp .env.example config/.env
    ok "Created config/.env from .env.example"
  else
    # Minimal .env so docker compose doesn't fail
    cat > config/.env <<'EOF'
C5_DASHBOARD_PASSWORD=
C5_DASHBOARD_HOST=0.0.0.0
C5_DASHBOARD_PORT=8601
C5_DASHBOARD_PUBLIC_PORT=8602
C5_SYMBOL=BTC-USD
C5_GRANULARITY_SECONDS=300
C5_LOOKBACK_DAYS=30
C5_RETRAIN_MINUTES=60
C5_CONFIDENCE_THRESHOLD=0.55
C5_PAPER_ENABLED=true
EOF
    ok "Created minimal config/.env (configure via the Setup Wizard)"
  fi
fi

# ── Step 5: Build & launch ───────────────────────────────────────
echo ""
echo -e "${Y}Building and starting the container…${NC}"
docker compose up -d --build

echo ""
echo -e "${G}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${G}║  ✔  Bot is running!                                      ║${NC}"
echo -e "${G}║                                                           ║${NC}"
echo -e "${G}║  Open your browser:  http://localhost:8602                ║${NC}"
echo -e "${G}║  Complete the Setup Wizard to configure your wallet.      ║${NC}"
echo -e "${G}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
