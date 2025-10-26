# Global Price Sentinel 启动脚本 (Windows PowerShell)

param(
    [switch]$Prod,
    [switch]$Install
)

$ErrorActionPreference = 'Stop'

Write-Host "🔍 Global Price Sentinel - 启动脚本" -ForegroundColor Cyan
Write-Host ""

# 检查虚拟环境
if (-not (Test-Path ".venv")) {
    Write-Host "[!] 未找到虚拟环境，正在创建..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "[✓] 虚拟环境创建完成" -ForegroundColor Green
}

# 激活虚拟环境
$activate = ".\.venv\Scripts\Activate.ps1"
if (Test-Path $activate) {
    . $activate
    Write-Host "[✓] 虚拟环境已激活" -ForegroundColor Green
} else {
    Write-Host "[!] 无法激活虚拟环境" -ForegroundColor Red
    exit 1
}

# 安装依赖
if ($Install -or -not (Test-Path ".\.venv\Lib\site-packages\fastapi")) {
    Write-Host "[*] 正在安装依赖..." -ForegroundColor Yellow
    pip install --upgrade pip
    pip install -r requirements.txt
    playwright install chromium
    Write-Host "[✓] 依赖安装完成" -ForegroundColor Green
}

# 检查配置文件
if (-not (Test-Path ".env")) {
    Write-Host "[!] 未找到 .env 文件，复制示例配置..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "[!] 请编辑 .env 文件填写配置" -ForegroundColor Yellow
}

if (-not (Test-Path "configs\targets.yml")) {
    Write-Host "[!] 未找到 targets.yml，复制示例配置..." -ForegroundColor Yellow
    Copy-Item "configs\targets.example.yml" "configs\targets.yml"
    Write-Host "[!] 请编辑 configs\targets.yml 配置监控目标" -ForegroundColor Yellow
}

# 初始化数据库
Write-Host "[*] 初始化数据库..." -ForegroundColor Yellow
python -c "from app.models import init_db; init_db(); print('[✓] 数据库初始化完成')"

# 生成示例报告
Write-Host "[*] 生成示例报告..." -ForegroundColor Yellow
if (-not (Test-Path "reports\latest.html")) {
    python -c "from app.reporter import ReportGenerator; ReportGenerator.generate_html_report(); print('[✓] 示例报告生成完成')"
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  启动服务..." -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "访问地址: http://localhost:8101" -ForegroundColor Green
Write-Host "API 文档: http://localhost:8101/api/docs" -ForegroundColor Green
Write-Host "最新报告: http://localhost:8101/reports/latest.html" -ForegroundColor Green
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

# 启动服务
if ($Prod) {
    uvicorn app.main:app --host 0.0.0.0 --port 8101 --workers 2
} else {
    uvicorn app.main:app --host 0.0.0.0 --port 8101 --reload
}

