Param(
  [string]$OutDir = "dist",
  [string]$Version = ""
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$product = Resolve-Path (Join-Path $root "..")

# Auto-read version from VERSION file if not provided
if (-not $Version) {
  $versionFile = Join-Path $product "VERSION"
  if (Test-Path $versionFile) {
    $Version = "v" + (Get-Content $versionFile -Raw).Trim()
  } else {
    $Version = "v0.0.0"
  }
}

$out = Join-Path $product $OutDir
New-Item -ItemType Directory -Force -Path $out | Out-Null

$zipName = "Crypto5min_PolyTrader_$Version.zip"
$zipPath = Join-Path $out $zipName
if (Test-Path $zipPath) { Remove-Item -Force $zipPath }

$exclude = @(
  ".env",
  ".git",
  # Keep config/logs/data folders (docker-compose bind mounts).
  # We'll remove secrets and runtime files inside them below.
  "__pycache__",
  ".pytest_cache",
  ".mypy_cache",
  ".venv",
  ".claude",
  "dist",
  "tools"
)

# Customer ZIP should include only customer-facing docs.
# Seller/internal docs stay in the repo.
$excludeFiles = @(
  "SALES_COPY.md",
  "WHOP_FORUM_PATCH_LOG.md",
  "RESEARCH.md",
  "deep-research-report.md"
)

$tmp = Join-Path $env:TEMP ("crypto5min-polytrader-release-" + [Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force -Path $tmp | Out-Null

Copy-Item -Recurse -Force -Path (Join-Path $product "*") -Destination $tmp

# Extra safety: remove any ad-hoc operator artifacts and secrets that might
# exist outside config/logs/data (e.g., scratch exports in repo root).
# Keep .env.example, but remove any other .env* files.
Get-ChildItem -Recurse -Force -File -Path $tmp -Filter ".env*" -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -ne ".env.example" } |
  Remove-Item -Force -ErrorAction SilentlyContinue

# Remove common scratch/temporary exports that could contain personal data.
$scratchGlobs = @(
  "_tmp_poly_*.json",
  "*_tmp*.json",
  "*snapshot*.json",
  "*equity*.json",
  "*state*.json",
  "*token*.txt"
)
foreach ($g in $scratchGlobs) {
  Get-ChildItem -Recurse -Force -File -Path $tmp -Filter $g -ErrorAction SilentlyContinue |
    Remove-Item -Force -ErrorAction SilentlyContinue
}

# Remove Python cache artifacts everywhere
Get-ChildItem -Recurse -Directory -Path $tmp -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -File -Path $tmp -Filter "*.pyc" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue

# Ensure required bind-mount folders exist (ZIPs don't preserve empty dirs)
New-Item -ItemType Directory -Force -Path (Join-Path $tmp "config") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $tmp "logs") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $tmp "data") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $tmp "releases") | Out-Null

# Never ship secrets/runtime state
Get-ChildItem -File -Path (Join-Path $tmp "config") -Filter ".env*" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Force -Path (Join-Path $tmp "logs") -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Force -Path (Join-Path $tmp "data") -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Force -Path (Join-Path $tmp "releases") -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# Placeholders so folders appear after unzip
Set-Content -Path (Join-Path $tmp "config\.keep") -Value "(placeholder)" -Encoding UTF8
Set-Content -Path (Join-Path $tmp "logs\.keep") -Value "(placeholder)" -Encoding UTF8
Set-Content -Path (Join-Path $tmp "data\.keep") -Value "(placeholder)" -Encoding UTF8
Set-Content -Path (Join-Path $tmp "releases\.keep") -Value "(placeholder)" -Encoding UTF8

# Never ship research PDFs in the paid ZIP (ship links instead)
Get-ChildItem -Recurse -File -Path $tmp -Filter "*.pdf" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue

foreach ($x in $exclude) {
  $p = Join-Path $tmp $x
  if (Test-Path $p) { Remove-Item -Recurse -Force $p }
}

foreach ($f in $excludeFiles) {
  $p = Join-Path $tmp $f
  if (Test-Path $p) { Remove-Item -Force $p }
}

# Exclude tests from customer ZIP
$testsPath = Join-Path $tmp "tests"
if (Test-Path $testsPath) { Remove-Item -Recurse -Force $testsPath }

# Customer ZIP should include caveats + security docs
# (Keep METRICS_AND_CAVEATS.md and SECURITY.md in the ZIP.)
$metricsPath = Join-Path $tmp "METRICS_AND_CAVEATS.md"
if (Test-Path $metricsPath) { }

# If seller wants to ship listing copy too, remove it from excludeFiles above.

Compress-Archive -Path (Join-Path $tmp "*") -DestinationPath $zipPath
Remove-Item -Recurse -Force $tmp

Write-Host "Created: $zipPath"
