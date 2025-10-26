# Global Price Sentinel - 简化启动脚本
# 适用于 Windows PowerShell

$ErrorActionPreference = 'Stop'

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Global Price Sentinel 启动脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[✓] Python 版本: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[✗] 未找到 Python，请先安装 Python 3.10+" -ForegroundColor Red
    exit 1
}

# 创建虚拟环境
if (-not (Test-Path ".venv")) {
    Write-Host "[*] 创建虚拟环境..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "[✓] 虚拟环境创建完成" -ForegroundColor Green
} else {
    Write-Host "[✓] 虚拟环境已存在" -ForegroundColor Green
}

# 激活虚拟环境
Write-Host "[*] 激活虚拟环境..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"

# 检查是否需要安装依赖
$needInstall = $false
if (-not (Test-Path ".\.venv\Lib\site-packages\fastapi")) {
    $needInstall = $true
}

if ($needInstall) {
    Write-Host "[*] 安装依赖（首次运行需要几分钟）..." -ForegroundColor Yellow
    
    python -m pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet
    
    Write-Host "[*] 安装 Playwright 浏览器..." -ForegroundColor Yellow
    playwright install chromium
    
    Write-Host "[✓] 依赖安装完成" -ForegroundColor Green
} else {
    Write-Host "[✓] 依赖已安装" -ForegroundColor Green
}

# 复制配置文件
if (-not (Test-Path ".env")) {
    Write-Host "[*] 创建配置文件 .env" -ForegroundColor Yellow
    Copy-Item "env.example" ".env"
}

if (-not (Test-Path "configs")) {
    New-Item -ItemType Directory -Path "configs" | Out-Null
}

if (-not (Test-Path "configs\targets.yml")) {
    Write-Host "[*] 创建监控目标配置" -ForegroundColor Yellow
    if (Test-Path "configs\targets.example.yml") {
        Copy-Item "configs\targets.example.yml" "configs\targets.yml"
    }
}

# 初始化数据库
Write-Host "[*] 初始化数据库..." -ForegroundColor Yellow
python -c "from app.models import init_db; init_db()"
Write-Host "[✓] 数据库初始化完成" -ForegroundColor Green

# 生成示例报告
if (-not (Test-Path "reports\latest.html")) {
    Write-Host "[*] 生成示例报告..." -ForegroundColor Yellow
    python -c "from app.reporter import ReportGenerator; ReportGenerator.generate_html_report()" 2>$null
    Write-Host "[✓] 示例报告生成完成" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  🚀 启动服务..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "访问地址:" -ForegroundColor Cyan
Write-Host "  • 主页:     http://localhost:8101" -ForegroundColor White
Write-Host "  • API文档:  http://localhost:8101/api/docs" -ForegroundColor White
Write-Host "  • 最新报告: http://localhost:8101/reports/latest.html" -ForegroundColor White
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

# 启动服务
uvicorn app.main:app --host 0.0.0.0 --port 8101 --reload

