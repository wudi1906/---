'use client'

import { useCallback, useEffect, useMemo, useState, type ChangeEvent } from 'react'
import Papa from 'papaparse'
import { useRouter } from 'next/navigation'
import MetricCard from '@/components/MetricCard'
import TrendChart from '@/components/TrendChart'
import {
  AVAILABLE_TEMPLATES,
  useDashboardStore,
} from '@/store/dashboardStore'
import type { TemplateId, DatasetType, DatasetTemplate, TemplateField } from '@/lib/kpiTemplates'
import { DEFAULT_TEMPLATE_ID, getTemplateById } from '@/lib/kpiTemplates'
import {
  calculateTemplate,
  type TemplateDatasets,
  type TemplateMappings,
  type CalculationResult,
} from '@/lib/kpiCalculator'

interface ParsedDataset {
  headers: string[]
  rows: string[][]
  records: Record<string, string>[]
}

interface ServerWarning {
  dataset: string
  row?: number
  field?: string
  message: string
}

const MAX_FILE_SIZE = 10 * 1024 * 1024
const MAX_WARNING_DISPLAY = 20

interface StepDefinition {
  id: string
  title: string
  description: string
}

const STEPS: StepDefinition[] = [
  { id: 'template', title: '选择 KPI 模板', description: '根据业务类型选择预置指标组合' },
  { id: 'upload', title: '上传 CSV 数据', description: '上传多个数据源，支持拖拽' },
  { id: 'mapping', title: '字段映射与清洗', description: '将 CSV 列映射至模板字段，可自动推荐' },
  { id: 'review', title: '预览并导入', description: '预览 KPI 与图表，确认后写入仪表盘' },
]

const DATASET_LABELS: Record<DatasetType, string> = {
  subscriptions: '订阅 / Revenue',
  churn: '流失 / Churn',
  acquisition: '获客 / Acquisition',
}

const PAGE_SIZE = 5

export default function ImportWizardPage() {
  const router = useRouter()
  const setFromCalculation = useDashboardStore((state) => state.setFromCalculation)

  const [stepIndex, setStepIndex] = useState(0)
  const [selectedTemplateId, setSelectedTemplateId] = useState<TemplateId>(DEFAULT_TEMPLATE_ID)
  const [datasets, setDatasets] = useState<Record<DatasetType, ParsedDataset | undefined>>(() => ({
    subscriptions: undefined,
    churn: undefined,
    acquisition: undefined,
  }))
  const [mappings, setMappings] = useState<TemplateMappings>(() => ({} as TemplateMappings))
  const [activeDataset, setActiveDataset] = useState<DatasetType | null>(null)
  const [page, setPage] = useState(0)
  const [calculation, setCalculation] = useState<CalculationResult | null>(null)
  const [parseError, setParseError] = useState<string | null>(null)
  const [processing, setProcessing] = useState(false)
  const [serverWarnings, setServerWarnings] = useState<ServerWarning[]>([])
  const [serverError, setServerError] = useState<string | null>(null)
  const [saving, setSaving] = useState(false)
  const [importSuccess, setImportSuccess] = useState(false)
  const [exporting, setExporting] = useState<'csv' | 'excel' | null>(null)
  const [exportError, setExportError] = useState<string | null>(null)
  const [exportMessage, setExportMessage] = useState<string | null>(null)

  const template = useMemo(() => getTemplateById(selectedTemplateId), [selectedTemplateId])

  const handleTemplateSwitch = (event: ChangeEvent<HTMLInputElement>) => {
    const nextTemplate = event.target.value as TemplateId
    setSelectedTemplateId(nextTemplate)
    setDatasets({ subscriptions: undefined, churn: undefined, acquisition: undefined })
    setMappings({} as TemplateMappings)
    setActiveDataset(null)
    setPage(0)
    setCalculation(null)
    setParseError(null)
    setServerWarnings([])
    setServerError(null)
    setExportError(null)
    setExportMessage(null)
    setImportSuccess(false)
    setStepIndex(1)
  }

  const handleFileParse = useCallback(
    (datasetId: DatasetType, file: File) => {
      setServerError(null)
      setServerWarnings([])
      setExportError(null)
      setExportMessage(null)
      setImportSuccess(false)
      Papa.parse<Record<string, string>>(file, {
        header: true,
        skipEmptyLines: true,
        transform: (value) => value?.trim?.() ?? value,
        complete: (result) => {
          const headers = (result.meta.fields && result.meta.fields.length > 0)
            ? result.meta.fields
            : Object.keys(result.data?.[0] ?? {})

          const records = (Array.isArray(result.data) ? result.data : []).filter((row) => row && Object.keys(row).length > 0)
          const rows = records.map((record) => headers.map((header) => record?.[header] ?? ''))

          setDatasets((prev) => ({
            ...prev,
            [datasetId]: {
              headers,
              rows,
              records: records.map((row) => {
                const sanitized: Record<string, string> = {}
                headers.forEach((header) => {
                  const value = row?.[header]
                  sanitized[header] = value === undefined || value === null ? '' : String(value)
                })
                return sanitized
              }),
            },
          }))
          setActiveDataset(datasetId)
          setPage(0)
          setParseError(null)
        },
        error: (error) => {
          console.error(error)
          setParseError(`解析 ${file.name} 失败：${error.message}`)
        },
      })
    },
    [],
  )

  const handleFileSelect = useCallback((datasetId: DatasetType, file: File) => {
    if (file.size > MAX_FILE_SIZE) {
      setParseError(`文件 ${file.name} 超过 10MB 限制，请拆分后再试。`)
      return
    }
    setParseError(null)
    handleFileParse(datasetId, file)
  }, [handleFileParse])

  const buildPayloadDatasets = useCallback(() => {
    const payload: TemplateDatasets = {}
    template.datasets.forEach((dataset) => {
      const parsed = datasets[dataset.id]
      if (parsed) {
        payload[dataset.id] = parsed.records
      }
    })
    return payload
  }, [datasets, template])

  const handleFileChange = (datasetId: DatasetType) => (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      handleFileSelect(datasetId, file)
    }
  }

  useEffect(() => {
    setMappings((previous) => {
      const nextMappings: TemplateMappings = ({ ...previous } as TemplateMappings)
      template.datasets.forEach((dataset) => {
        const parsed = datasets[dataset.id]
        if (!parsed) return
        const headersLower = parsed.headers.map((header) => header.toLowerCase())
        const existing = { ...(nextMappings[dataset.id] ?? {}) }

        dataset.fields.forEach((field) => {
          if (existing[field.id]) return
          const candidateIndex = headersLower.findIndex((header) => header === field.id.toLowerCase())
          if (candidateIndex >= 0) {
            existing[field.id] = parsed.headers[candidateIndex]
          }
        })

        nextMappings[dataset.id] = existing
      })
      return nextMappings
    })
  }, [datasets, template.datasets])

  const goToStep = (nextIndex: number) => {
    if (nextIndex < 0 || nextIndex >= STEPS.length) return
    if (nextIndex < 3) {
      setImportSuccess(false)
      setServerWarnings([])
      setServerError(null)
      setExportError(null)
      setExportMessage(null)
    }
    setStepIndex(nextIndex)
  }

  const canProceedUpload = useMemo(() => {
    return template.datasets
      .filter((dataset) => !dataset.optional)
      .every((dataset) => Boolean(datasets[dataset.id]))
  }, [template.datasets, datasets])

  const canProceedMapping = useMemo(() => {
    return template.datasets.every((dataset) => {
      if (!datasets[dataset.id]) {
        return dataset.optional ?? false
      }
      const mapping = mappings[dataset.id] ?? {}
      return dataset.fields
        .filter((field) => field.required !== false)
        .every((field) => Boolean(mapping[field.id]))
    })
  }, [template.datasets, datasets, mappings])

  const handleReview = async () => {
    if (!canProceedMapping) return
    setProcessing(true)
    setServerError(null)
    setServerWarnings([])
    setExportError(null)
    setExportMessage(null)
    setImportSuccess(false)
    try {
      const payloadDatasets = buildPayloadDatasets()
      const result = calculateTemplate(selectedTemplateId, payloadDatasets, mappings)
      setCalculation(result)
      setStepIndex(3)
    } finally {
      setProcessing(false)
    }
  }

  const handleApply = async () => {
    if (!calculation) return
    setSaving(true)
    setServerError(null)
    setExportError(null)
    setExportMessage(null)
    try {
      const payload = {
        templateId: selectedTemplateId,
        datasets: buildPayloadDatasets(),
        mappings,
      }
      const response = await fetch('/api/import', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })
      const data = await response.json()
      if (!response.ok || !data.success) {
        throw new Error(data.error ?? '导入失败，请稍后重试。')
      }
      setServerWarnings(data.warnings ?? [])
      setCalculation(data.calculation)
      setFromCalculation(data.calculation)
      setImportSuccess(true)
    } catch (error) {
      setServerWarnings([])
      setServerError(error instanceof Error ? error.message : '导入失败，请稍后重试。')
    } finally {
      setSaving(false)
    }
  }

  const handleExport = useCallback(async (format: 'csv' | 'excel') => {
    setExportError(null)
    setExportMessage(null)
    setExporting(format)
    try {
      const response = await fetch(`/api/exports?format=${format}`)
      if (!response.ok) {
        let message = `${format === 'csv' ? 'CSV' : 'Excel'} 导出失败，请稍后重试。`
        try {
          const data = await response.json()
          if (data?.error) message = data.error
        } catch {
          // ignore JSON parse errors
        }
        throw new Error(message)
      }
      const blob = await response.blob()
      let fileName = `northstar-metrics-${Date.now()}.${format === 'csv' ? 'csv' : 'xlsx'}`
      const disposition = response.headers.get('Content-Disposition')
      if (disposition) {
        const match = disposition.match(/filename="?([^";]+)"?/i)
        if (match && match[1]) {
          fileName = decodeURIComponent(match[1])
        }
      }
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = fileName
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      setExportMessage(`${format === 'csv' ? 'CSV' : 'Excel'} 导出开始下载。`)
    } catch (error) {
      setExportError(error instanceof Error ? error.message : '导出失败，请稍后重试。')
    } finally {
      setExporting(null)
    }
  }, [])

  const handleNavigateDashboard = useCallback(() => {
    router.push('/')
  }, [router])

  const preview = activeDataset ? datasets[activeDataset] : undefined
  const totalRows = preview?.rows.length ?? 0
  const totalPages = preview ? Math.max(1, Math.ceil(totalRows / PAGE_SIZE)) : 1
  const safePage = Math.min(page, totalPages - 1)
  const paginatedRows = useMemo(() => {
    if (!preview) return []
    const start = safePage * PAGE_SIZE
    return preview.rows.slice(start, start + PAGE_SIZE)
  }, [preview, safePage])

  useEffect(() => {
    if (preview && page > totalPages - 1) {
      setPage(Math.max(totalPages - 1, 0))
    }
  }, [preview, page, totalPages])

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6 lg:px-8">
        <header className="mb-10">
          <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-50">CSV 导入向导</h1>
          <p className="mt-2 max-w-3xl text-sm text-slate-600 dark:text-slate-300">
            支持多模板、多文件导入、字段映射与图表预览。数据仅保存在浏览器内存，确保安全。
          </p>
        </header>

        <nav aria-label="导入步骤" className="mb-8">
          <ol className="flex flex-col gap-3 sm:flex-row sm:items-center">
            {STEPS.map((step, index) => {
              const isActive = index === stepIndex
              const isCompleted = index < stepIndex
              return (
                <li key={step.id} className="flex-1">
                  <button
                    type="button"
                    onClick={() => goToStep(index)}
                    className={`flex w-full flex-col rounded-xl border px-4 py-3 text-left transition focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 ${
                      isActive
                        ? 'border-blue-500 bg-blue-50 text-blue-900 dark:border-blue-400 dark:bg-blue-900/30 dark:text-blue-100'
                        : isCompleted
                          ? 'border-emerald-400 bg-emerald-50 text-emerald-900 dark:border-emerald-400/60 dark:bg-emerald-950/40 dark:text-emerald-200'
                          : 'border-slate-200 bg-white text-slate-700 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200'
                    }`}
                  >
                    <span className="text-xs font-semibold uppercase tracking-wide">Step {index + 1}</span>
                    <span className="mt-1 text-sm font-medium">{step.title}</span>
                    <span className="mt-1 text-xs text-slate-500 dark:text-slate-400">{step.description}</span>
                  </button>
                </li>
              )
            })}
          </ol>
        </nav>

        {stepIndex === 0 && (
          <section className="grid gap-4 sm:grid-cols-2" aria-label="模板列表">
            {AVAILABLE_TEMPLATES.map((tpl) => (
              <label
                key={tpl.id}
                className={`flex flex-col rounded-xl border p-5 transition focus-within:ring-2 focus-within:ring-blue-500 ${
                  tpl.id === selectedTemplateId
                    ? 'border-blue-500 bg-blue-50/40 dark:border-blue-500 dark:bg-blue-900/40'
                    : 'border-slate-200 bg-white dark:border-slate-700 dark:bg-slate-900'
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <span className="text-xs font-semibold uppercase tracking-wide text-blue-600 dark:text-blue-300">{tpl.category}</span>
                    <h2 className="mt-1 text-lg font-semibold text-slate-900 dark:text-slate-50">{tpl.name}</h2>
                  </div>
                  <input
                    type="radio"
                    name="template"
                    value={tpl.id}
                    checked={selectedTemplateId === tpl.id}
                    onChange={handleTemplateSwitch}
                    className="mt-1 h-4 w-4"
                    aria-label={`选择模板 ${tpl.name}`}
                  />
                </div>
                <p className="mt-3 text-sm text-slate-600 dark:text-slate-300">{tpl.description}</p>
                <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">适用：{tpl.recommendedFor}</p>
                <ul className="mt-3 space-y-1 text-xs text-slate-500 dark:text-slate-400">
                  {tpl.datasets.map((dataset) => (
                    <li key={`${tpl.id}-${dataset.id}`}>• {DATASET_LABELS[dataset.id]} {dataset.optional && '(可选)'}</li>
                  ))}
                </ul>
              </label>
            ))}
          </section>
        )}

        {stepIndex === 1 && (
          <section className="space-y-6" aria-label="上传 CSV">
            {template.datasets.map((dataset) => (
              <UploadField
                key={dataset.id}
                dataset={dataset}
                parsed={datasets[dataset.id]}
                onFileChange={handleFileChange(dataset.id)}
              />
            ))}
            <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-slate-200 bg-white p-4 text-xs text-slate-500 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300">
              <p>提示：CSV 必须包含表头；字段顺序不重要，可在下一步映射。</p>
              <button
                type="button"
                disabled={!canProceedUpload}
                onClick={() => goToStep(2)}
                className={`rounded-lg px-4 py-2 text-sm font-semibold transition focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 ${
                  canProceedUpload
                    ? 'bg-blue-600 text-white hover:bg-blue-700'
                    : 'bg-slate-200 text-slate-500'
                }`}
              >
                下一步：字段映射
              </button>
            </div>
          </section>
        )}

        {stepIndex === 2 && (
          <section className="space-y-6" aria-label="字段映射">
            {template.datasets.map((dataset) => (
              <MappingCard
                key={dataset.id}
                dataset={dataset}
                parsed={datasets[dataset.id]}
                mapping={mappings[dataset.id] ?? {}}
                onChange={(fieldId, column) => {
                  setMappings((prev) => ({
                    ...prev,
                    [dataset.id]: {
                      ...(prev[dataset.id] ?? {}),
                      [fieldId]: column,
                    },
                  }))
                }}
              />
            ))}

            <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-slate-200 bg-white p-4 text-xs text-slate-500 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300">
              <p>系统会自动推荐同名字段，仍可手动调整。</p>
              <button
                type="button"
                disabled={!canProceedMapping || processing}
                onClick={handleReview}
                className={`rounded-lg px-4 py-2 text-sm font-semibold transition focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 ${
                  canProceedMapping && !processing
                    ? 'bg-blue-600 text-white hover:bg-blue-700'
                    : 'bg-slate-200 text-slate-500'
                }`}
              >
                {processing ? '计算中…' : '预览 KPI'}
              </button>
            </div>
          </section>
        )}

        {stepIndex === 3 && calculation && (
          <section className="space-y-10" aria-label="导入预览">
            <div className="rounded-xl border border-emerald-200 bg-emerald-50/60 p-4 text-sm text-emerald-900 dark:border-emerald-400/40 dark:bg-emerald-950/50 dark:text-emerald-100">
              数据已解析完成，可在确认无误后写入仪表盘并导出报表。
            </div>

            {serverError && (
              <div
                role="alert"
                className="rounded-xl border border-red-200 bg-red-50/70 p-4 text-sm text-red-700 dark:border-red-500/40 dark:bg-red-950/40 dark:text-red-200"
              >
                {serverError}
              </div>
            )}

            {importSuccess && (
              <div
                role="status"
                className="rounded-xl border border-emerald-300 bg-emerald-100/70 p-4 text-sm text-emerald-900 dark:border-emerald-400/40 dark:bg-emerald-950/40 dark:text-emerald-100"
              >
                <p>✅ 数据已写入仪表盘，可返回首页查看最新 KPI。</p>
                {exportMessage && <p className="mt-1 text-xs text-emerald-700 dark:text-emerald-200">{exportMessage}</p>}
              </div>
            )}

            {exportError && (
              <div
                role="alert"
                className="rounded-xl border border-red-200 bg-red-50/70 p-4 text-sm text-red-700 dark:border-red-500/40 dark:bg-red-950/40 dark:text-red-200"
              >
                {exportError}
              </div>
            )}

            {serverWarnings.length > 0 && (
              <div className="rounded-xl border border-amber-200 bg-amber-50/80 p-4 text-sm text-amber-900 dark:border-amber-400/40 dark:bg-amber-950/40 dark:text-amber-100">
                <p className="font-semibold">⚠️ 下列项已被跳过，不影响写入：</p>
                <ul className="mt-2 space-y-1 text-xs">
                  {serverWarnings.slice(0, MAX_WARNING_DISPLAY).map((warning, index) => {
                    const datasetLabel = warning.dataset !== 'general'
                      ? DATASET_LABELS[warning.dataset as DatasetType] ?? warning.dataset
                      : null
                    return (
                      <li key={`${warning.dataset}-${warning.row ?? 'global'}-${index}`}>
                        {datasetLabel ? `${datasetLabel}：` : ''}
                        {warning.row ? `第 ${warning.row} 行` : ''}
                        {warning.field ? `（${warning.field}）` : ''}
                        {warning.row || warning.field ? ' · ' : ''}
                        {warning.message}
                      </li>
                    )
                  })}
                  {serverWarnings.length > MAX_WARNING_DISPLAY && (
                    <li className="text-amber-700/80 dark:text-amber-200/70">… 仅展示前 {MAX_WARNING_DISPLAY} 条警告，详见导出结果。</li>
                  )}
                </ul>
              </div>
            )}

            <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">
              {calculation.metrics.map((metric) => (
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
            </div>

            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              {calculation.charts.map((chart) => (
                <TrendChart key={chart.id} title={chart.title} data={chart.data} height={320} />
              ))}
            </div>

            <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-slate-200 bg-white p-4 text-sm text-slate-700 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200">
              <div>
                <p className="font-semibold">导入摘要</p>
                <ul className="mt-2 text-xs text-slate-500 dark:text-slate-400">
                  {calculation.datasetSummary.map((summary) => (
                    <li key={summary.dataset}>
                      {summary.dataset.toUpperCase()} · {summary.rows} 条记录{summary.lastDate ? ` · 最新月份 ${summary.lastDate}` : ''}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="flex flex-wrap gap-2">
                <button
                  type="button"
                  onClick={() => goToStep(1)}
                  className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-100 dark:border-slate-600 dark:text-slate-300 dark:hover:bg-slate-800"
                >
                  返回修改
                </button>
                <button
                  type="button"
                  onClick={handleApply}
                  disabled={saving}
                  aria-busy={saving}
                  className={`rounded-lg px-4 py-2 text-sm font-semibold text-white shadow-sm transition focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-emerald-500 ${
                    saving ? 'bg-emerald-400 cursor-not-allowed' : 'bg-emerald-600 hover:bg-emerald-700'
                  }`}
                >
                  {saving ? '写入中…' : importSuccess ? '重新写入' : '应用到仪表盘'}
                </button>
                <button
                  type="button"
                  onClick={() => handleExport('csv')}
                  disabled={!importSuccess || exporting === 'csv'}
                  className={`rounded-lg px-4 py-2 text-sm font-semibold transition focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500 ${
                    !importSuccess || exporting === 'csv'
                      ? 'cursor-not-allowed border border-slate-300 bg-slate-200 text-slate-500 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-400'
                      : 'border border-blue-500 bg-white text-blue-600 hover:bg-blue-50 dark:border-blue-400 dark:bg-slate-900 dark:text-blue-200'
                  }`}
                >
                  {exporting === 'csv' ? '导出 CSV…' : '导出 CSV'}
                </button>
                <button
                  type="button"
                  onClick={() => handleExport('excel')}
                  disabled={!importSuccess || exporting === 'excel'}
                  className={`rounded-lg px-4 py-2 text-sm font-semibold transition focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500 ${
                    !importSuccess || exporting === 'excel'
                      ? 'cursor-not-allowed border border-slate-300 bg-slate-200 text-slate-500 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-400'
                      : 'border border-blue-500 bg-white text-blue-600 hover:bg-blue-50 dark:border-blue-400 dark:bg-slate-900 dark:text-blue-200'
                  }`}
                >
                  {exporting === 'excel' ? '导出 Excel…' : '导出 Excel'}
                </button>
                {importSuccess && (
                  <button
                    type="button"
                    onClick={handleNavigateDashboard}
                    className="rounded-lg border border-emerald-400 bg-emerald-100 px-4 py-2 text-sm font-semibold text-emerald-800 transition hover:bg-emerald-200 dark:border-emerald-400/60 dark:bg-emerald-950/40 dark:text-emerald-200"
                  >
                    查看仪表盘
                  </button>
                )}
              </div>
            </div>
          </section>
        )}

        {(stepIndex === 1 || stepIndex === 2) && (
          <section className="mt-12 rounded-xl border border-slate-200 bg-white p-6 dark:border-slate-700 dark:bg-slate-900" aria-label="数据预览">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">数据预览</h2>
                <p className="text-sm text-slate-500 dark:text-slate-400">最多展示前 {PAGE_SIZE} 条数据，完整数据会参与计算。</p>
              </div>
              {parseError && <p className="text-xs text-red-500" role="alert">{parseError}</p>}
            </div>

            <div className="mt-4 flex flex-wrap items-center gap-2" role="tablist" aria-label="数据源切换">
              {template.datasets.map((dataset) => {
                const parsed = datasets[dataset.id]
                const isActive = activeDataset === dataset.id
                return (
                  <button
                    key={dataset.id}
                    type="button"
                    role="tab"
                    aria-selected={isActive}
                    onClick={() => {
                      if (parsed) {
                        setActiveDataset(dataset.id)
                        setPage(0)
                      }
                    }}
                    disabled={!parsed}
                    className={`rounded-lg px-4 py-2 text-sm font-medium focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 ${
                      parsed
                        ? isActive
                          ? 'bg-blue-600 text-white shadow'
                          : 'bg-slate-100 text-slate-700 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700'
                        : 'bg-slate-200 text-slate-400'
                    }`}
                  >
                    {DATASET_LABELS[dataset.id]}
                    {!parsed && <span className="ml-2 text-xs">(未上传)</span>}
                  </button>
                )
              })}
            </div>

            {preview && preview.rows.length > 0 ? (
              <div className="mt-6 overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-700">
                <table className="min-w-full divide-y divide-slate-200 text-sm dark:divide-slate-700">
                  <thead className="bg-slate-100 text-left text-xs font-semibold uppercase tracking-wide text-slate-600 dark:bg-slate-800 dark:text-slate-300">
                    <tr>
                      {preview.headers.map((header) => (
                        <th key={header} className="px-4 py-2">{header || '—'}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="bg-white text-slate-700 dark:bg-slate-950 dark:text-slate-200">
                    {paginatedRows.map((row, rowIndex) => (
                      <tr key={`${activeDataset}-${safePage}-${rowIndex}`} className={rowIndex % 2 === 0 ? 'bg-white dark:bg-slate-950' : 'bg-slate-50 dark:bg-slate-900/60'}>
                        {row.map((cell, cellIndex) => (
                          <td key={`${rowIndex}-${cellIndex}`} className="whitespace-nowrap px-4 py-2 text-xs">{cell || '—'}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
                <footer className="flex items-center justify-between px-4 py-3 text-xs text-slate-500 dark:text-slate-400">
                  <span>
                    显示 {safePage * PAGE_SIZE + 1}-{Math.min((safePage + 1) * PAGE_SIZE, totalRows)} / {totalRows}
                  </span>
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={() => setPage(Math.max(safePage - 1, 0))}
                      disabled={safePage === 0}
                      className="rounded-lg border border-slate-300 px-3 py-1.5 text-xs hover:bg-slate-100 disabled:cursor-not-allowed disabled:border-slate-200 disabled:text-slate-400 dark:border-slate-600 dark:hover:bg-slate-800"
                    >
                      Prev
                    </button>
                    <span aria-live="polite">Page {safePage + 1} / {totalPages}</span>
                    <button
                      type="button"
                      onClick={() => setPage(Math.min(safePage + 1, totalPages - 1))}
                      disabled={safePage >= totalPages - 1}
                      className="rounded-lg border border-slate-300 px-3 py-1.5 text-xs hover:bg-slate-100 disabled:cursor-not-allowed disabled:border-slate-200 disabled:text-slate-400 dark:border-slate-600 dark:hover:bg-slate-800"
                    >
                      Next
                    </button>
                  </div>
                </footer>
              </div>
            ) : (
              <p className="mt-6 text-sm text-slate-500 dark:text-slate-400">暂无可预览数据，请先上传 CSV。</p>
            )}
          </section>
        )}
      </div>
    </div>
  )
}

function UploadField({ dataset, parsed, onFileChange }: { dataset: DatasetTemplate; parsed?: ParsedDataset; onFileChange: (event: ChangeEvent<HTMLInputElement>) => void }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-700 dark:bg-slate-900">
      <label className="block text-sm font-semibold text-slate-900 dark:text-slate-100">
        {dataset.optional ? '可选 · ' : ''}{DATASET_LABELS[dataset.id]}
      </label>
      <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">{dataset.description}</p>
      <input
        type="file"
        accept=".csv"
        onChange={onFileChange}
        className="mt-3 block w-full cursor-pointer rounded-lg border border-dashed border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-700 transition hover:border-blue-400 hover:bg-blue-50 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200 dark:hover:border-blue-400 dark:hover:bg-slate-800/60"
      />
      {parsed && (
        <p className="mt-2 text-xs text-emerald-600 dark:text-emerald-300" role="status">
          已加载 {parsed.rows.length} 条记录 · {parsed.headers.length} 列
        </p>
      )}
      {dataset.sample && (
        <details className="mt-3 text-xs text-slate-500 dark:text-slate-400">
          <summary className="cursor-pointer text-blue-600 underline dark:text-blue-300">查看示例</summary>
          <pre className="mt-2 max-h-48 overflow-auto rounded-lg bg-slate-900/90 p-3 text-[11px] text-slate-100">
            {dataset.sample}
          </pre>
        </details>
      )}
    </div>
  )
}

function MappingCard({
  dataset,
  parsed,
  mapping,
  onChange,
}: {
  dataset: DatasetTemplate
  parsed?: ParsedDataset
  mapping: Record<string, string>
  onChange: (fieldId: string, column: string) => void
}) {
  const hasData = Boolean(parsed)
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-700 dark:bg-slate-900">
      <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
        {DATASET_LABELS[dataset.id]}
        {!hasData && <span className="ml-2 text-xs text-slate-500">(未上传)</span>}
      </h3>
      <div className="mt-3 grid gap-4 md:grid-cols-2">
        {dataset.fields.map((field) => (
          <FieldMappingRow
            key={field.id}
            field={field}
            headers={parsed?.headers ?? []}
            value={mapping[field.id] ?? ''}
            onChange={(column) => onChange(field.id, column)}
          />
        ))}
      </div>
    </div>
  )
}

function FieldMappingRow({
  field,
  headers,
  value,
  onChange,
}: {
  field: TemplateField
  headers: string[]
  value: string
  onChange: (column: string) => void
}) {
  return (
    <label className="flex flex-col gap-1 text-sm text-slate-700 dark:text-slate-200">
      <span className="font-medium">
        {field.label}
        {field.required !== false ? <span className="ml-1 text-red-500">*</span> : <span className="ml-1 text-xs text-slate-400">(可选)</span>}
      </span>
      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-100"
      >
        <option value="">选择 CSV 列</option>
        {headers.map((header) => (
          <option key={header} value={header}>
            {header}
          </option>
        ))}
      </select>
      <span className="text-xs text-slate-500 dark:text-slate-400">{field.description}</span>
    </label>
  )
}
