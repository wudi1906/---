'use client'

import { useMemo } from 'react'
import MetricCard from '@/components/MetricCard'
import TrendChart from '@/components/TrendChart'

export default function ShowcasePage() {
  const metrics = useMemo(
    () => ({
      mrr: { value: 125_000, change: 12.5, currency: 'USD' },
      arr: { value: 1_500_000, change: 15.2, currency: 'USD' },
      churn: { value: 3.2, change: -1.5, format: 'percentage' as const },
      ltv: { value: 24_500, change: 8.3, currency: 'USD' },
    }),
    []
  )

  const chartData = useMemo(
    () => ({
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [
        {
          label: 'MRR',
          data: [100_000, 105_000, 110_000, 115_000, 120_000, 125_000],
          borderColor: '#2563EB',
          backgroundColor: 'rgba(37, 99, 235, 0.1)',
        },
      ],
    }),
    []
  )

  const userGrowthData = useMemo(
    () => ({
      ...chartData,
      datasets: [
        {
          ...chartData.datasets[0],
          label: '活跃用户',
          data: [1200, 1350, 1500, 1680, 1850, 2000],
          borderColor: '#16A34A',
          backgroundColor: 'rgba(22, 163, 74, 0.1)',
        },
      ],
    }),
    [chartData]
  )

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50 dark:from-gray-900 dark:via-emerald-900/10 dark:to-gray-900 p-8">
      <div className="mx-auto max-w-7xl space-y-8">
        {/* Hero Section */}
        <div className="text-center space-y-4">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-100 dark:bg-emerald-900/30 rounded-full">
            <span className="text-2xl">📊</span>
            <span className="text-sm font-semibold text-emerald-800 dark:text-emerald-300 uppercase tracking-wide">
              Interactive Demo
            </span>
          </div>
          <h1 className="text-5xl font-extrabold bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
            SaaS Northstar Dashboard
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            实时业务指标仪表盘，展示 MRR、ARR、Churn、LTV 等核心 KPI，帮助 SaaS 企业数据驱动决策
          </p>
        </div>

        {/* Feature Highlights */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg border border-emerald-100 dark:border-emerald-900/30">
            <div className="text-3xl mb-3">📈</div>
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">实时数据监控</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              自动同步 Stripe、Chargebee 等支付平台数据，实时更新业务指标
            </p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg border border-teal-100 dark:border-teal-900/30">
            <div className="text-3xl mb-3">📊</div>
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">可视化图表</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              多维度趋势图表，支持时间范围筛选，历史数据对比分析
            </p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg border border-cyan-100 dark:border-cyan-900/30">
            <div className="text-3xl mb-3">📥</div>
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">CSV 数据导入</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              支持批量导入历史数据，灵活的数据接入方式满足不同需求
            </p>
          </div>
        </div>

        {/* Metrics Grid */}
        <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-3xl p-8 shadow-2xl border border-white dark:border-gray-700">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
            <span className="text-3xl">💰</span>
            核心业务指标
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <MetricCard title="月度经常性收入" subtitle="MRR" value={metrics.mrr.value} change={metrics.mrr.change} currency={metrics.mrr.currency} />
            <MetricCard title="年度经常性收入" subtitle="ARR" value={metrics.arr.value} change={metrics.arr.change} currency={metrics.arr.currency} />
            <MetricCard title="流失率" subtitle="Churn Rate" value={metrics.churn.value} change={metrics.churn.change} format="percentage" />
            <MetricCard title="客户生命周期价值" subtitle="LTV" value={metrics.ltv.value} change={metrics.ltv.change} currency={metrics.ltv.currency} />
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-3xl p-8 shadow-2xl border border-white dark:border-gray-700">
            <TrendChart title="MRR 趋势" data={chartData} height={300} />
          </div>
          <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-3xl p-8 shadow-2xl border border-white dark:border-gray-700">
            <TrendChart title="用户增长" data={userGrowthData} height={300} />
          </div>
        </div>

        {/* CTA Section */}
        <div className="bg-gradient-to-r from-emerald-500 to-teal-600 rounded-3xl p-12 text-center text-white shadow-2xl">
          <h2 className="text-3xl font-bold mb-4">准备好开始了吗？</h2>
          <p className="text-lg mb-8 opacity-90 max-w-2xl mx-auto">
            立即体验完整功能，导入您的业务数据，获取深度分析洞察
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <a
              href="/"
              className="inline-flex items-center gap-2 px-8 py-4 bg-white text-emerald-600 rounded-xl font-bold hover:bg-gray-50 transition-all shadow-lg hover:shadow-xl"
            >
              返回主页
            </a>
            <a
              href="/import"
              className="inline-flex items-center gap-2 px-8 py-4 bg-emerald-700 text-white rounded-xl font-bold hover:bg-emerald-800 transition-all shadow-lg hover:shadow-xl"
            >
              📥 导入数据
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
