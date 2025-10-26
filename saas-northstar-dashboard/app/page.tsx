'use client'

import { useState } from 'react'
import MetricCard from '@/components/MetricCard'
import TrendChart from '@/components/TrendChart'

export default function Dashboard() {
  const [timeRange, setTimeRange] = useState('30d')
  
  // 示例数据
  const metrics = {
    mrr: {
      value: 125000,
      change: 12.5,
      currency: 'USD'
    },
    arr: {
      value: 1500000,
      change: 15.2,
      currency: 'USD'
    },
    churn: {
      value: 3.2,
      change: -1.5,
      format: 'percentage'
    },
    ltv: {
      value: 24500,
      change: 8.3,
      currency: 'USD'
    }
  }
  
  const chartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'MRR',
        data: [100000, 105000, 110000, 115000, 120000, 125000],
        borderColor: '#2563EB',
        backgroundColor: 'rgba(37, 99, 235, 0.1)',
      }
    ]
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            SaaS Northstar Dashboard
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            关键业务指标一览
          </p>
        </div>

        {/* Time Range Selector */}
        <div className="mb-6 flex gap-2">
          {['7d', '30d', '90d', '1y'].map((range) => (
            <button
              key={range}
              onClick={() => setTimeRange(range)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                timeRange === range
                  ? 'bg-blue-600 text-white'
                  : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              {range === '7d' && '7天'}
              {range === '30d' && '30天'}
              {range === '90d' && '90天'}
              {range === '1y' && '1年'}
            </button>
          ))}
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <MetricCard
            title="月度经常性收入"
            subtitle="MRR"
            value={metrics.mrr.value}
            change={metrics.mrr.change}
            currency={metrics.mrr.currency}
          />
          <MetricCard
            title="年度经常性收入"
            subtitle="ARR"
            value={metrics.arr.value}
            change={metrics.arr.change}
            currency={metrics.arr.currency}
          />
          <MetricCard
            title="流失率"
            subtitle="Churn Rate"
            value={metrics.churn.value}
            change={metrics.churn.change}
            format="percentage"
          />
          <MetricCard
            title="客户生命周期价值"
            subtitle="LTV"
            value={metrics.ltv.value}
            change={metrics.ltv.change}
            currency={metrics.ltv.currency}
          />
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <TrendChart
            title="MRR 趋势"
            data={chartData}
            height={300}
          />
          <TrendChart
            title="用户增长"
            data={{
              ...chartData,
              datasets: [{
                ...chartData.datasets[0],
                label: '活跃用户',
                data: [1200, 1350, 1500, 1680, 1850, 2000],
                borderColor: '#16A34A',
                backgroundColor: 'rgba(22, 163, 74, 0.1)',
              }]
            }}
            height={300}
          />
        </div>

        {/* Import Link */}
        <div className="mt-8 text-center">
          <a
            href="/import"
            className="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            📥 导入 CSV 数据
          </a>
        </div>
      </div>
    </div>
  )
}

