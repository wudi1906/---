# Global Price Sentinel 演示脚本
# 用于展示项目功能

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Global Price Sentinel 功能演示" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$baseUrl = "http://localhost:8101"

# 1. 健康检查
Write-Host "[1] 健康检查..." -ForegroundColor Yellow
$health = Invoke-RestMethod -Uri "$baseUrl/api/health"
Write-Host "   状态: $($health.status)" -ForegroundColor Green
Write-Host "   版本: $($health.version)" -ForegroundColor Green
Write-Host ""

# 2. 查看现有监控记录
Write-Host "[2] 查看监控记录（最近5条）..." -ForegroundColor Yellow
$records = Invoke-RestMethod -Uri "$baseUrl/api/records?limit=5"
Write-Host "   总记录数: $($records.Count)" -ForegroundColor Green
foreach ($record in $records) {
    $status = if ($record.success) { "✓" } else { "✗" }
    Write-Host "   $status $($record.target_id) - $($record.created_at)" -ForegroundColor White
}
Write-Host ""

# 3. 执行一次测试监控
Write-Host "[3] 执行测试监控..." -ForegroundColor Yellow
$testConfig = @(
    @{
        id = "demo-test-" + (Get-Date -Format "HHmmss")
        url = "https://httpbin.org/html"
        name_selector = "h1"
        currency = "USD"
        enabled = $true
    }
) | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Uri "$baseUrl/api/monitor/run" `
        -Method POST `
        -Body $testConfig `
        -ContentType "application/json"
    
    Write-Host "   ✓ 监控完成" -ForegroundColor Green
    Write-Host "   记录数: $($result.records)" -ForegroundColor White
} catch {
    Write-Host "   ✗ 监控失败: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# 4. 获取价格趋势摘要
Write-Host "[4] 获取价格趋势摘要..." -ForegroundColor Yellow
$summary = Invoke-RestMethod -Uri "$baseUrl/api/summary?days=7"
Write-Host "   目标数量: $($summary.Count)" -ForegroundColor Green
Write-Host ""

# 5. 生成报告
Write-Host "[5] 生成 HTML 报告..." -ForegroundColor Yellow
$report = Invoke-RestMethod -Uri "$baseUrl/api/report/generate?days=7&format=html"
Write-Host "   ✓ 报告已生成" -ForegroundColor Green
Write-Host "   访问地址: $baseUrl$($report.report_url)" -ForegroundColor Cyan
Write-Host ""

# 6. 生成 CSV 报告
Write-Host "[6] 生成 CSV 报告..." -ForegroundColor Yellow
$csvReport = Invoke-RestMethod -Uri "$baseUrl/api/report/generate?days=7&format=csv"
Write-Host "   ✓ CSV 报告已生成" -ForegroundColor Green
Write-Host "   访问地址: $baseUrl$($csvReport.report_url)" -ForegroundColor Cyan
Write-Host ""

# 总结
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  演示完成！可访问的页面：" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  • 主页:     $baseUrl" -ForegroundColor White
Write-Host "  • API文档:  $baseUrl/api/docs" -ForegroundColor White
Write-Host "  • 最新报告: $baseUrl/reports/latest.html" -ForegroundColor White
Write-Host "  • 监控记录: $baseUrl/api/records" -ForegroundColor White
Write-Host "  • 统计摘要: $baseUrl/api/summary" -ForegroundColor White
Write-Host ""

