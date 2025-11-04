'use client'

import Link from 'next/link'
import { useMemo, useState, type ChangeEvent } from 'react'
import MetricCard from '@/components/MetricCard'
import TrendChart from '@/components/TrendChart'
import LanguageSwitcher from '@/components/LanguageSwitcher'
import { AVAILABLE_TEMPLATES, useDashboardStore } from '@/store/dashboardStore'
import type { TemplateId } from '@/lib/kpiTemplates'
import { useTranslation } from '@/lib/i18n'

const TIME_RANGES: Array<{ id: string; labelKey: string }> = [
  { id: '30d', labelKey: 'dashboard.controls.timeRanges.30d' },
  { id: '90d', labelKey: 'dashboard.controls.timeRanges.90d' },
  { id: '1y', labelKey: 'dashboard.controls.timeRanges.1y' },
]

export default function Dashboard() {
  const [timeRange, setTimeRange] = useState('30d')
  const { templateId, metrics, charts, datasetSummary, lastImportedAt, resetToTemplate } = useDashboardStore()
  const { t, lang } = useTranslation()
  const locale = lang === 'zh' ? 'zh-CN' : 'en-US'

  const activeTemplate = useMemo(() => AVAILABLE_TEMPLATES.find((tpl) => tpl.id === templateId), [templateId])

  const translatedMetrics = useMemo(() => (
    metrics.map((metric) => ({
      ...metric,
      title: t(`metrics.definitions.${metric.id}.title`, metric.title),
      subtitle: t(`metrics.definitions.${metric.id}.subtitle`, metric.subtitle),
    }))
  ), [metrics, t])

  const translatedCharts = useMemo(() => (
    charts.map((chart) => ({
      ...chart,
      title: t(`charts.${chart.id}`, chart.title),
    }))
  ), [charts, t])

  const handleTemplateChange = (event: ChangeEvent<HTMLSelectElement>) => {
    resetToTemplate(event.target.value as TemplateId)
  }

  const lastImportedLabel = useMemo(() => {
    if (!lastImportedAt) return null
    const formatted = new Date(lastImportedAt).toLocaleString(locale)
    return t('dashboard.lastImported', undefined, { timestamp: formatted })
  }, [lastImportedAt, locale, t])

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <header className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
          <div className="flex flex-1 flex-col gap-4">
            <div>
              <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-50">{t('dashboard.title')}</h1>
              <p className="mt-2 max-w-2xl text-sm text-slate-600 dark:text-slate-300">{t('dashboard.subtitle')}</p>
              {lastImportedLabel && (
                <p className="mt-3 text-xs text-slate-500 dark:text-slate-400" aria-live="polite">
                  {lastImportedLabel}
                </p>
              )}
            </div>
          </div>
          <div className="flex flex-col items-end gap-4">
            <LanguageSwitcher />
            <div
              className="flex w-full max-w-md flex-col gap-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-700 dark:bg-slate-900"
              role="group"
              aria-label={t('dashboard.controls.groupAria', 'Template and range controls')}
            >
              <label className="text-sm font-medium text-slate-700 dark:text-slate-200" htmlFor="template-select">
                {t('dashboard.controls.templateLabel')}
              </label>
              <select
                id="template-select"
                value={templateId}
                onChange={handleTemplateChange}
                className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100"
              >
                {AVAILABLE_TEMPLATES.map((template) => (
                  <option key={template.id} value={template.id}>
                    {t(`templates.${template.id}.name`, template.name)} · {t(`templates.${template.id}.category`, template.category)}
                  </option>
                ))}
              </select>
              <label className="text-sm font-medium text-slate-700 dark:text-slate-200" htmlFor="time-range">
                {t('dashboard.controls.timeRangeLabel')}
              </label>
              <div id="time-range" className="flex flex-wrap gap-2" role="radiogroup" aria-label={t('dashboard.controls.timeRangeLabel')}>
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
                    {t(range.labelKey)}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </header>

        {activeTemplate && (
          <section className="mt-8 rounded-xl border border-blue-100 bg-blue-50/60 p-5 text-sm text-blue-900 dark:border-blue-900/40 dark:bg-blue-950/50 dark:text-blue-100" aria-live="polite">
            <p className="font-semibold">{t(`templates.${activeTemplate.id}.name`, activeTemplate.name)}</p>
            <p className="mt-1 text-blue-800 dark:text-blue-200">{t(`templates.${activeTemplate.id}.description`, activeTemplate.description)}</p>
            <p className="mt-1 text-xs text-blue-700/80 dark:text-blue-300/80">
              {t('dashboard.template.sceneLabel')}{t(`templates.${activeTemplate.id}.recommendedFor`, activeTemplate.recommendedFor)}
            </p>
          </section>
        )}

        <section className="mt-8" aria-label={t('dashboard.sections.metrics')}>
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">
            {translatedMetrics.map((metric) => (
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
            {translatedMetrics.length === 0 && (
              <p className="col-span-full text-sm text-slate-500 dark:text-slate-400">{t('dashboard.emptyMetrics')}</p>
            )}
          </div>
        </section>

        <section className="mt-10" aria-label={t('dashboard.sections.charts')}>
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            {translatedCharts.map((chart) => (
              <TrendChart key={chart.id} title={chart.title} data={chart.data} height={320} />
            ))}
          </div>
        </section>

        <section className="mt-10" aria-label={t('dashboard.sections.dataset')}>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {datasetSummary.map((summary) => {
              const rowsText = t('dashboard.dataset.rows', undefined, { count: summary.rows.toLocaleString(locale) })
              const datasetLabel = t(`datasets.labels.${summary.dataset}`, summary.dataset.toUpperCase())
              const latestText = summary.lastDate ? t('dashboard.dataset.latestMonth', undefined, { value: summary.lastDate }) : null
              return (
                <div key={summary.dataset} className="rounded-xl border border-slate-200 bg-white p-4 text-sm dark:border-slate-700 dark:bg-slate-900">
                  <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200">{datasetLabel}</h3>
                  <p className="mt-2 text-slate-600 dark:text-slate-300">{rowsText}</p>
                  {latestText && <p className="text-xs text-slate-500 dark:text-slate-400">{latestText}</p>}
                </div>
              )
            })}
          </div>
        </section>

        <div className="mt-12 flex flex-col items-center justify-between gap-4 rounded-xl border border-dashed border-blue-300 bg-blue-50/60 p-6 text-center text-sm text-blue-900 dark:border-blue-800 dark:bg-blue-950/40 dark:text-blue-100 sm:flex-row sm:text-left">
          <div>
            <p className="font-semibold">{t('dashboard.cta.title')}</p>
            <p className="mt-1 text-xs text-blue-800/80 dark:text-blue-200/80">{t('dashboard.cta.subtitle')}</p>
          </div>
          <Link
            href="/import"
            className="inline-flex items-center rounded-lg bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500"
          >
            {t('dashboard.cta.button')}
          </Link>
        </div>
      </div>
    </div>
  )
}

