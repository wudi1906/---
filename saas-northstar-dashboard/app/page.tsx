'use client'

import Link from 'next/link'
import { useMemo, useState, type ChangeEvent } from 'react'
import MetricCard from '@/components/MetricCard'
import TrendChart from '@/components/TrendChart'
import { AVAILABLE_TEMPLATES, useDashboardStore } from '@/store/dashboardStore'
import type { TemplateId } from '@/lib/kpiTemplates'

const TIME_RANGES: Array<{ id: string; label: string }> = [
  { id: '30d', label: '近30天' },
  { id: '90d', label: '近90天' },
  { id: '1y', label: '近12个月' },
]

export default function Dashboard() {
  const [timeRange, setTimeRange] = useState('30d')
  const { templateId, metrics, charts, datasetSummary, lastImportedAt, resetToTemplate } = useDashboardStore()

  const activeTemplate = useMemo(() => AVAILABLE_TEMPLATES.find((tpl) => tpl.id === templateId), [templateId])

  const handleTemplateChange = (event: ChangeEvent<HTMLSelectElement>) => {
    resetToTemplate(event.target.value as TemplateId)
  }

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <header className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-50">SaaS Northstar Dashboard</h1>
            <p className="mt-2 max-w-2xl text-sm text-slate-600 dark:text-slate-300">
              自定义 KPI 模板、导入多份 CSV 数据并一键导出可视化报表。遵循 WCAG 2.1 AA，键盘可导航。
            </p>
            {lastImportedAt && (
              <p className="mt-3 text-xs text-slate-500 dark:text-slate-400" aria-live="polite">
                最近导入：{new Date(lastImportedAt).toLocaleString()}
              </p>
            )}
          </div>
          <div className="flex w-full max-w-md flex-col gap-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-700 dark:bg-slate-900" role="group" aria-label="模板与时间范围">
            <label className="text-sm font-medium text-slate-700 dark:text-slate-200" htmlFor="template-select">
              KPI 模板
            </label>
            <select
              id="template-select"
              value={templateId}
              onChange={handleTemplateChange}
              className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100"
            >
              {AVAILABLE_TEMPLATES.map((template) => (
                <option key={template.id} value={template.id}>
                  {template.name} · {template.category}
                </option>
              ))}
            </select>
            <label className="text-sm font-medium text-slate-700 dark:text-slate-200" htmlFor="time-range">
              时间范围
            </label>
            <div id="time-range" className="flex flex-wrap gap-2" role="radiogroup" aria-label="展示时间范围">
              {TIME_RANGES.map((range) => (
                <button
                  key={range.id}
                  type="button"
                  role="radio"
                  aria-checked={timeRange === range.id}
                  onClick={() => setTimeRange(range.id)}
                  className={`rounded-lg px-4 py-2 text-sm font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500 ${
                    timeRange === range.id
                      ? 'bg-blue-600 text-white'
                      : 'bg-slate-100 text-slate-700 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700'
                  }`}
                >
                  {range.label}
                </button>
              ))}
            </div>
          </div>
        </header>

        {activeTemplate && (
          <section className="mt-8 rounded-xl border border-blue-100 bg-blue-50/60 p-5 text-sm text-blue-900 dark:border-blue-900/40 dark:bg-blue-950/50 dark:text-blue-100" aria-live="polite">
            <p className="font-semibold">{activeTemplate.name}</p>
            <p className="mt-1 text-blue-800 dark:text-blue-200">{activeTemplate.description}</p>
            <p className="mt-1 text-xs text-blue-700/80 dark:text-blue-300/80">适用场景：{activeTemplate.recommendedFor}</p>
          </section>
        )}

        <section className="mt-8" aria-label="核心指标">
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">
            {metrics.map((metric) => (
              <MetricCard
                key={metric.id}
                title={metric.title}
                subtitle={metric.subtitle}
                value={metric.value}
                change={metric.change}
                currency={metric.currency}
                format={metric.format}
              />
            ))}
            {metrics.length === 0 && (
              <p className="col-span-full text-sm text-slate-500 dark:text-slate-400">
                尚未导入数据，请前往“导入向导”。
              </p>
            )}
          </div>
        </section>

        <section className="mt-10" aria-label="趋势图">
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            {charts.map((chart) => (
              <TrendChart key={chart.id} title={chart.title} data={chart.data} height={320} />
            ))}
          </div>
        </section>

        <section className="mt-10" aria-label="数据集摘要">
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {datasetSummary.map((summary) => (
              <div key={summary.dataset} className="rounded-xl border border-slate-200 bg-white p-4 text-sm dark:border-slate-700 dark:bg-slate-900">
                <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200">{summary.dataset.toUpperCase()}</h3>
                <p className="mt-2 text-slate-600 dark:text-slate-300">记录行数：{summary.rows.toLocaleString()}</p>
                {summary.lastDate && (
                  <p className="text-xs text-slate-500 dark:text-slate-400">最新月份：{summary.lastDate}</p>
                )}
              </div>
            ))}
          </div>
        </section>

        <div className="mt-12 flex flex-col items-center justify-between gap-4 rounded-xl border border-dashed border-blue-300 bg-blue-50/60 p-6 text-center text-sm text-blue-900 dark:border-blue-800 dark:bg-blue-950/40 dark:text-blue-100 sm:flex-row sm:text-left">
          <div>
            <p className="font-semibold">从 CSV 导入新的指标数据?</p>
            <p className="mt-1 text-xs text-blue-800/80 dark:text-blue-200/80">向导支持多 CSV、字段映射、导入后自动刷新本页指标与图表。</p>
          </div>
          <Link
            href="/import"
            className="inline-flex items-center rounded-lg bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500"
          >
            📥 打开导入向导
          </Link>
        </div>
      </div>
    </div>
  )
}

