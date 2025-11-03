import { Buffer } from 'node:buffer'
import ExcelJS from 'exceljs'
import { calculateTemplate, type CalculationResult, type TemplateDatasets, type TemplateMappings } from '@/lib/kpiCalculator'
import { getDb, withTransaction } from '@/lib/db'
import { KPI_TEMPLATES, type DatasetType, type TemplateId, getTemplateById } from '@/lib/kpiTemplates'

export interface ImportPayload {
  templateId: TemplateId
  datasets: TemplateDatasets
  mappings: TemplateMappings
}

export interface ValidationIssue {
  dataset: DatasetType | 'general'
  row?: number
  field?: string
  message: string
}

export interface ImportResponse {
  calculation: CalculationResult
  importId: number
  createdAt: string
  warnings?: ValidationIssue[]
}

const NUMERIC_FIELDS = new Set(['amount', 'cost', 'customers', 'visitors'])
const DATE_FIELDS = new Set(['date'])
const MAX_ERRORS = 20
const MAX_JSON_SIZE = 10 * 1024 * 1024

function ensureSizeLimit(payload: ImportPayload) {
  const approxSize = Buffer.byteLength(JSON.stringify(payload.datasets), 'utf8')
  if (approxSize > MAX_JSON_SIZE) {
    throw new Error('数据量超过 10MB 限制，请拆分文件后重试。')
  }
}

export function validateImportPayload(payload: ImportPayload): ValidationIssue[] {
  const template = getTemplateById(payload.templateId)
  const issues: ValidationIssue[] = []

  template.datasets.forEach((dataset) => {
    const records = payload.datasets[dataset.id]
    if ((!records || records.length === 0) && !(dataset.optional ?? false)) {
      issues.push({ dataset: dataset.id, message: '缺少必填数据集，请上传对应 CSV。' })
      return
    }

    if (!records) return

    const mapping = payload.mappings[dataset.id] ?? {}
    dataset.fields.forEach((field) => {
      if (field.required !== false && !mapping[field.id]) {
        issues.push({ dataset: dataset.id, message: `字段「${field.label}」未映射。` })
      }
    })

    records.some((row, index) => {
      if (issues.length >= MAX_ERRORS) return true
      dataset.fields.forEach((field) => {
        const column = mapping[field.id]
        if (!column) return
        const value = row[column]
        if (field.required !== false && (!value || value.trim() === '')) {
          issues.push({ dataset: dataset.id, row: index + 1, field: field.id, message: `第 ${index + 1} 行字段「${field.label}」为空。` })
          return
        }
        if (value && NUMERIC_FIELDS.has(field.id)) {
          const numeric = Number(value.toString().replace(/[^0-9.-]+/g, ''))
          if (!Number.isFinite(numeric)) {
            issues.push({ dataset: dataset.id, row: index + 1, field: field.id, message: `第 ${index + 1} 行字段「${field.label}」必须为数字。` })
          }
        }
        if (value && DATE_FIELDS.has(field.id)) {
          const parsed = Date.parse(value)
          if (Number.isNaN(parsed)) {
            issues.push({ dataset: dataset.id, row: index + 1, field: field.id, message: `第 ${index + 1} 行字段「${field.label}」不是有效日期 (YYYY-MM-DD)。` })
          }
        }
      })
      return issues.length >= MAX_ERRORS
    })
  })

  return issues
}

function persistImport(templateId: TemplateId, datasets: TemplateDatasets, mappings: TemplateMappings, calculation: CalculationResult) {
  const db = getDb()
  const createdAt = new Date().toISOString()
  const insert = db.prepare(`
    INSERT INTO imports (template_id, datasets_json, mappings_json, calculation_json, created_at)
    VALUES (@templateId, @datasets, @mappings, @calculation, @createdAt)
  `)
  const result = insert.run({
    templateId,
    datasets: JSON.stringify(datasets),
    mappings: JSON.stringify(mappings),
    calculation: JSON.stringify(calculation),
    createdAt,
  })
  return { id: Number(result.lastInsertRowid), createdAt }
}

export function processImport(payload: ImportPayload): ImportResponse {
  ensureSizeLimit(payload)
  const validationIssues = validateImportPayload(payload)
  const fatalIssues = validationIssues.filter((issue) => issue.row === undefined && issue.dataset !== 'general')
  if (fatalIssues.length > 0) {
    throw new Error(fatalIssues[0].message)
  }

  const calculation = calculateTemplate(payload.templateId, payload.datasets, payload.mappings)

  let importId = 0
  let createdAt = new Date().toISOString()
  withTransaction(() => {
    const persisted = persistImport(payload.templateId, payload.datasets, payload.mappings, calculation)
    importId = persisted.id
    createdAt = persisted.createdAt
  })

  return {
    calculation,
    importId,
    createdAt,
    warnings: validationIssues.length > 0 ? validationIssues : undefined,
  }
}

export function getLatestImport(): { calculation: CalculationResult; templateId: TemplateId; createdAt: string } | null {
  const db = getDb()
  const row = db.prepare('SELECT template_id, calculation_json, created_at FROM imports ORDER BY id DESC LIMIT 1').get()
  if (!row) return null
  return {
    templateId: row.template_id as TemplateId,
    calculation: JSON.parse(row.calculation_json) as CalculationResult,
    createdAt: row.created_at as string,
  }
}

function buildMetricsCsv(calculation: CalculationResult) {
  const lines = ['Section,Metric,Value,Change,Format']
  calculation.metrics.forEach((metric) => {
    lines.push(`Metric,"${metric.title}",${metric.value},${metric.change},${metric.format}`)
  })
  lines.push('')
  lines.push('Section,Dataset,Rows,Last Date')
  calculation.datasetSummary.forEach((summary) => {
    lines.push(`Dataset,${summary.dataset.toUpperCase()},${summary.rows},${summary.lastDate ?? ''}`)
  })
  return lines.join('\r\n')
}

async function buildMetricsWorkbook(calculation: CalculationResult) {
  const workbook = new ExcelJS.Workbook()
  workbook.creator = 'SaaS Northstar Dashboard'
  workbook.created = new Date()

  const metricsSheet = workbook.addWorksheet('Metrics')
  metricsSheet.columns = [
    { header: 'Metric', key: 'metric', width: 28 },
    { header: 'Value', key: 'value', width: 15 },
    { header: 'Change', key: 'change', width: 12 },
    { header: 'Format', key: 'format', width: 12 },
    { header: 'Description', key: 'description', width: 50 },
  ]
  calculation.metrics.forEach((metric) => {
    metricsSheet.addRow({
      metric: metric.title,
      value: metric.value,
      change: metric.change,
      format: metric.format,
      description: metric.subtitle,
    })
  })

  const summarySheet = workbook.addWorksheet('Dataset Summary')
  summarySheet.columns = [
    { header: 'Dataset', key: 'dataset', width: 24 },
    { header: 'Rows', key: 'rows', width: 12 },
    { header: 'Last Date', key: 'lastDate', width: 18 },
  ]
  calculation.datasetSummary.forEach((summary) => {
    summarySheet.addRow({ dataset: summary.dataset.toUpperCase(), rows: summary.rows, lastDate: summary.lastDate ?? '' })
  })

  const chartsSheet = workbook.addWorksheet('Charts')
  chartsSheet.columns = [
    { header: 'Chart', key: 'chart', width: 32 },
    { header: 'Labels', key: 'labels', width: 50 },
    { header: 'Dataset', key: 'dataset', width: 24 },
    { header: 'Values', key: 'values', width: 50 },
  ]
  calculation.charts.forEach((chart) => {
    chart.data.datasets.forEach((dataset) => {
      chartsSheet.addRow({
        chart: chart.title,
        labels: chart.data.labels.join(', '),
        dataset: dataset.label,
        values: dataset.data.join(', '),
      })
    })
  })

  return workbook.xlsx.writeBuffer()
}

export async function buildExport(format: 'csv' | 'excel') {
  const latest = getLatestImport()
  if (!latest) {
    throw new Error('当前没有可导出的导入记录。')
  }

  if (format === 'csv') {
    const csv = buildMetricsCsv(latest.calculation)
    return {
      fileName: `northstar-metrics-${latest.createdAt.replace(/[:T]/g, '-').slice(0, 19)}.csv`,
      contentType: 'text/csv; charset=utf-8',
      buffer: Buffer.from(csv, 'utf8'),
    }
  }

  const excelBuffer = await buildMetricsWorkbook(latest.calculation)
  return {
    fileName: `northstar-metrics-${latest.createdAt.replace(/[:T]/g, '-').slice(0, 19)}.xlsx`,
    contentType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    buffer: Buffer.from(excelBuffer),
  }
}

export function listTemplates() {
  return KPI_TEMPLATES.map((template) => ({
    id: template.id,
    name: template.name,
  }))
}
