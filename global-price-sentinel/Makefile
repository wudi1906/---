.PHONY: help install dev test clean docker-build docker-run lint format

help:  ## 显示帮助信息
	@echo "Global Price Sentinel - Make 命令"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## 安装依赖
	python -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	.venv/bin/playwright install chromium

dev:  ## 启动开发服务器
	.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8101 --reload

prod:  ## 启动生产服务器
	.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8101 --workers 2

test:  ## 运行测试
	.venv/bin/pytest tests/ -v --cov=app --cov-report=html

lint:  ## 代码检查
	.venv/bin/flake8 app/ tests/
	.venv/bin/mypy app/

format:  ## 代码格式化
	.venv/bin/black app/ tests/
	.venv/bin/isort app/ tests/

clean:  ## 清理临时文件
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov

docker-build:  ## 构建 Docker 镜像
	docker build -t global-price-sentinel:latest .

docker-run:  ## 运行 Docker 容器
	docker-compose up -d

docker-stop:  ## 停止 Docker 容器
	docker-compose down

docker-logs:  ## 查看 Docker 日志
	docker-compose logs -f

init-db:  ## 初始化数据库
	.venv/bin/python -c "from app.models import init_db; init_db()"

generate-report:  ## 生成报告
	.venv/bin/python -c "from app.reporter import ReportGenerator; ReportGenerator.generate_html_report(); ReportGenerator.generate_csv_report()"

