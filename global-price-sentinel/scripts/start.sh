#!/bin/bash
# Global Price Sentinel 启动脚本 (Linux/macOS)

set -e

PROD_MODE=false
INSTALL_DEPS=false

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --prod)
            PROD_MODE=true
            shift
            ;;
        --install)
            INSTALL_DEPS=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

echo "🔍 Global Price Sentinel - 启动脚本"
echo ""

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "[!] 未找到虚拟环境，正在创建..."
    python3 -m venv .venv
    echo "[✓] 虚拟环境创建完成"
fi

# 激活虚拟环境
source .venv/bin/activate
echo "[✓] 虚拟环境已激活"

# 安装依赖
if [ "$INSTALL_DEPS" = true ] || [ ! -f ".venv/bin/uvicorn" ]; then
    echo "[*] 正在安装依赖..."
    pip install --upgrade pip
    pip install -r requirements.txt
    playwright install chromium
    echo "[✓] 依赖安装完成"
fi

# 检查配置文件
if [ ! -f ".env" ]; then
    echo "[!] 未找到 .env 文件，复制示例配置..."
    cp .env.example .env
    echo "[!] 请编辑 .env 文件填写配置"
fi

if [ ! -f "configs/targets.yml" ]; then
    echo "[!] 未找到 targets.yml，复制示例配置..."
    cp configs/targets.example.yml configs/targets.yml
    echo "[!] 请编辑 configs/targets.yml 配置监控目标"
fi

# 初始化数据库
echo "[*] 初始化数据库..."
python -c "from app.models import init_db; init_db(); print('[✓] 数据库初始化完成')"

# 生成示例报告
echo "[*] 生成示例报告..."
if [ ! -f "reports/latest.html" ]; then
    python -c "from app.reporter import ReportGenerator; ReportGenerator.generate_html_report(); print('[✓] 示例报告生成完成')"
fi

echo ""
echo "====================================="
echo "  启动服务..."
echo "====================================="
echo ""
echo "访问地址: http://localhost:8101"
echo "API 文档: http://localhost:8101/api/docs"
echo "最新报告: http://localhost:8101/reports/latest.html"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 启动服务
if [ "$PROD_MODE" = true ]; then
    uvicorn app.main:app --host 0.0.0.0 --port 8101 --workers 2
else
    uvicorn app.main:app --host 0.0.0.0 --port 8101 --reload
fi

