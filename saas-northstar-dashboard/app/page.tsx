'use client'

import { useMemo, useState } from 'react'
import MetricCard from '@/components/MetricCard'
import TrendChart from '@/components/TrendChart'

const RANGE_LABELS: Record<string, string> = {
  '7d': '7天',
  '30d': '30天',
  '90d': '90天',
  '1y': '1年',
}

export default function DashboardPage() {
  const [timeRange, setTimeRange] = useState<'7d' | '30d' | '90d' | '1y'>('30d')

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
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">SaaS Northstar Dashboard</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">关键业务指标一览</p>
      </header>

      <section className="flex flex-wrap gap-2">
        {Object.keys(RANGE_LABELS).map((range) => (
          <button
            key={range}
            onClick={() => setTimeRange(range as keyof typeof RANGE_LABELS)}
            className={`rounded-lg px-4 py-2 text-sm font-medium transition-colors ${
              timeRange === range
                ? 'bg-blue-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-100 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700'
            }`}
            aria-pressed={timeRange === range}
          >
            {RANGE_LABELS[range]}
          </button>
        ))}
      </section>

      <section className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
        <MetricCard title="月度经常性收入" subtitle="MRR" value={metrics.mrr.value} change={metrics.mrr.change} currency={metrics.mrr.currency} />
        <MetricCard title="年度经常性收入" subtitle="ARR" value={metrics.arr.value} change={metrics.arr.change} currency={metrics.arr.currency} />
        <MetricCard title="流失率" subtitle="Churn Rate" value={metrics.churn.value} change={metrics.churn.change} format="percentage" />
        <MetricCard title="客户生命周期价值" subtitle="LTV" value={metrics.ltv.value} change={metrics.ltv.change} currency={metrics.ltv.currency} />
      </section>

      <section className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <TrendChart title="MRR 趋势" data={chartData} height={300} />
        <TrendChart title="用户增长" data={userGrowthData} height={300} />
      </section>

      <section className="rounded-2xl border border-dashed border-blue-300 bg-blue-50/60 p-6 text-center dark:border-blue-800 dark:bg-blue-900/30">
        <p className="mb-4 text-sm font-semibold uppercase tracking-wide text-blue-600 dark:text-blue-200">数据导入</p>
        <p className="mb-6 text-gray-600 dark:text-gray-300">上传 CSV 将自动刷新所有 KPI 与图表</p>
        <a
          href="/import"
          className="inline-flex items-center rounded-lg bg-blue-600 px-6 py-3 font-medium text-white transition-colors hover:bg-blue-700"
        >
          📥 导入 CSV 数据
        </a>
      </section>
    </div>
  )
}

