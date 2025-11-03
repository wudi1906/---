import { format, parseISO } from 'date-fns'
import type { DatasetType, KpiTemplate, MetricDefinition, TemplateId } from './kpiTemplates'
import { KPI_TEMPLATES, sortByMonthKey } from './kpiTemplates'

export interface DatasetMapping {
  [fieldId: string]: string
}

export type DatasetRecords = Record<string, string>[]

export type TemplateDatasets = Partial<Record<DatasetType, DatasetRecords>>

export type TemplateMappings = Partial<Record<DatasetType, DatasetMapping>>

export interface MetricValue {
  id: string
  title: string
  subtitle: string
  description: string
  value: number
  change: number
  format: MetricDefinition['format']
  currency?: string
}

export interface ChartConfig {
  id: string
  title: string
  data: {
    labels: string[]
    datasets: Array<{
      label: string
      data: number[]
      borderColor?: string
      backgroundColor?: string
    }>
  }
}

export interface DatasetSummary {
  dataset: DatasetType
  rows: number
  lastDate?: string
}

export interface CalculationResult {
  metrics: MetricValue[]
  charts: ChartConfig[]
  datasetSummary: DatasetSummary[]
  templateId: TemplateId
}

function toNumber(value: string | undefined | null): number {
  if (value === undefined || value === null || value === '') return 0
  const normalized = value.replace(/[^0-9.-]+/g, '')
  const parsed = Number(normalized)
  return Number.isFinite(parsed) ? parsed : 0
}

function toMonthKey(value: string): string {
  try {
    const date = parseISO(value)
    if (Number.isNaN(date.getTime())) {
      return 'Unknown'
    }
    return format(date, 'yyyy-MM')
  } catch {
    return 'Unknown'
  }
}

function groupByMonth(rows: DatasetRecords, dateField: string, amountField: string) {
  const groups: Record<string, number> = {}
  for (const row of rows) {
    const key = toMonthKey(row[dateField] ?? '')
    groups[key] = (groups[key] ?? 0) + toNumber(row[amountField])
  }
  return groups
}

function uniqueCount(rows: DatasetRecords, field: string): number {
  const set = new Set<string>()
  for (const row of rows) {
    const value = row[field]
    if (value) set.add(value)
  }
  return set.size
}

function getTemplate(templateId: TemplateId): KpiTemplate {
  const template = KPI_TEMPLATES.find((tpl) => tpl.id === templateId)
  if (!template) {
    throw new Error(`Unknown template: ${templateId}`)
  }
  return template
}

function computeChange(latest: number, previous: number): number {
  if (!Number.isFinite(latest) || !Number.isFinite(previous) || previous === 0) {
    return 0
  }
  const value = ((latest - previous) / Math.abs(previous)) * 100
  return Number(value.toFixed(1))
}

function createMetric(tpl: MetricDefinition, value: number, change: number): MetricValue {
  return {
    id: tpl.id,
    title: tpl.title,
    subtitle: tpl.subtitle,
    description: tpl.description,
    value,
    change,
    format: tpl.format,
    currency: tpl.currency,
  }
}

function b2bCalculator(datasets: TemplateDatasets, mappings: TemplateMappings, template: KpiTemplate): CalculationResult {
  const subscriptions = datasets.subscriptions ?? []
  const churn = datasets.churn ?? []
  const acquisition = datasets.acquisition ?? []

  const subMapping = mappings.subscriptions ?? {}
  const churnMapping = mappings.churn ?? {}
  const acqMapping = mappings.acquisition ?? {}

  const revenueByMonth = groupByMonth(subscriptions, subMapping.date ?? 'date', subMapping.amount ?? 'amount')
  const months = sortByMonthKey(Object.keys(revenueByMonth))
  const latestMonthKey = months[months.length - 1]
  const previousMonthKey = months[months.length - 2]

  const latestMRR = latestMonthKey ? revenueByMonth[latestMonthKey] : 0
  const previousMRR = previousMonthKey ? revenueByMonth[previousMonthKey] : 0

  const churnedCustomers = uniqueCount(churn, churnMapping.customerId ?? 'customerId')
  const totalCustomers = uniqueCount(subscriptions, subMapping.customerId ?? 'customerId') || 1
  const churnRate = (churnedCustomers / totalCustomers) * 100

  const averageRevenuePerCustomer = totalCustomers ? (Object.values(revenueByMonth).reduce((sum, value) => sum + value, 0) / totalCustomers) : 0
  const churnFraction = churnRate / 100
  const ltv = churnFraction > 0 ? averageRevenuePerCustomer / churnFraction : averageRevenuePerCustomer

  const metrics = template.metrics.map((metric) => {
    switch (metric.id) {
      case 'mrr':
        return createMetric(metric, latestMRR, computeChange(latestMRR, previousMRR))
      case 'arr':
        return createMetric(metric, latestMRR * 12, computeChange(latestMRR * 12, previousMRR * 12))
      case 'churnRate':
        return createMetric(metric, Number(churnRate.toFixed(1)), 0)
      case 'ltv':
        return createMetric(metric, Number(ltv.toFixed(0)), 0)
      default:
        return createMetric(metric, 0, 0)
    }
  })

  const churnByMonth = groupByMonth(churn, churnMapping.date ?? 'date', churnMapping.customerId ?? 'customerId')
  const churnCounts = Object.fromEntries(Object.entries(churnByMonth).map(([key, value]) => [key, Math.round(value)]))
  const acquisitionByMonth = groupByMonth(acquisition, acqMapping.date ?? 'date', acqMapping.customers ?? 'customers')

  const chartMonths = sortByMonthKey(Array.from(new Set([...months, ...Object.keys(acquisitionByMonth)])))

  const charts: ChartConfig[] = [
    {
      id: 'revenueTrend',
      title: 'MRR 趋势',
      data: {
        labels: chartMonths,
        datasets: [
          {
            label: 'MRR',
            data: chartMonths.map((month) => revenueByMonth[month] ?? 0),
            borderColor: '#2563EB',
            backgroundColor: 'rgba(37, 99, 235, 0.15)',
          },
        ],
      },
    },
    {
      id: 'acquisitionTrend',
      title: '获客与流失',
      data: {
        labels: chartMonths,
        datasets: [
          {
            label: '新增客户',
            data: chartMonths.map((month) => acquisitionByMonth[month] ?? 0),
            borderColor: '#16A34A',
            backgroundColor: 'rgba(22, 163, 74, 0.15)',
          },
          {
            label: '流失客户',
            data: chartMonths.map((month) => churnCounts[month] ?? 0),
            borderColor: '#F97316',
            backgroundColor: 'rgba(249, 115, 22, 0.15)',
          },
        ],
      },
    },
  ]

  return {
    templateId: template.id as TemplateId,
    metrics,
    charts,
    datasetSummary: [
      { dataset: 'subscriptions', rows: subscriptions.length, lastDate: latestMonthKey },
      { dataset: 'churn', rows: churn.length },
      { dataset: 'acquisition', rows: acquisition.length },
    ],
  }
}

function b2cCalculator(datasets: TemplateDatasets, mappings: TemplateMappings, template: KpiTemplate): CalculationResult {
  const subscriptions = datasets.subscriptions ?? []
  const acquisition = datasets.acquisition ?? []
  const subMapping = mappings.subscriptions ?? {}
  const acqMapping = mappings.acquisition ?? {}

  const revenueByMonth = groupByMonth(subscriptions, subMapping.date ?? 'date', subMapping.amount ?? 'amount')
  const months = sortByMonthKey(Object.keys(revenueByMonth))
  const latestMonthKey = months[months.length - 1]
  const previousMonthKey = months[months.length - 2]
  const latestRevenue = latestMonthKey ? revenueByMonth[latestMonthKey] : 0
  const previousRevenue = previousMonthKey ? revenueByMonth[previousMonthKey] : 0

  const activeCustomers = uniqueCount(subscriptions, subMapping.customerId ?? 'customerId')
  const totalRevenue = Object.values(revenueByMonth).reduce((sum, value) => sum + value, 0)
  const avgOrderValue = subscriptions.length ? totalRevenue / subscriptions.length : 0

  const totalAcquisitionCost = acquisition.reduce((sum, row) => sum + toNumber(row[acqMapping.cost ?? 'cost']), 0)
  const totalAcquiredCustomers = acquisition.reduce((sum, row) => sum + toNumber(row[acqMapping.customers ?? 'customers']), 0)
  const visits = acquisition.reduce((sum, row) => sum + toNumber(row[acqMapping.visitors ?? 'visitors']), 0)

  const conversionRate = visits > 0 ? (totalAcquiredCustomers / visits) * 100 : 0
  const cac = totalAcquiredCustomers > 0 ? totalAcquisitionCost / totalAcquiredCustomers : 0

  const metrics = template.metrics.map((metric) => {
    switch (metric.id) {
      case 'activeCustomers':
        return createMetric(metric, activeCustomers, 0)
      case 'conversionRate':
        return createMetric(metric, Number(conversionRate.toFixed(2)), 0)
      case 'averageOrderValue':
        return createMetric(metric, Number(avgOrderValue.toFixed(2)), computeChange(latestRevenue, previousRevenue))
      case 'cac':
        return createMetric(metric, Number(cac.toFixed(2)), 0)
      default:
        return createMetric(metric, 0, 0)
    }
  })

  const acquisitionByMonth = groupByMonth(acquisition, acqMapping.date ?? 'date', acqMapping.customers ?? 'customers')
  const spendByMonth = groupByMonth(acquisition, acqMapping.date ?? 'date', acqMapping.cost ?? 'cost')
  const chartMonths = sortByMonthKey(Array.from(new Set([...months, ...Object.keys(acquisitionByMonth)])))

  const charts: ChartConfig[] = [
    {
      id: 'revenueByMonth',
      title: '月度收入趋势',
      data: {
        labels: chartMonths,
        datasets: [
          {
            label: 'Revenue',
            data: chartMonths.map((month) => revenueByMonth[month] ?? 0),
            borderColor: '#2563EB',
            backgroundColor: 'rgba(37, 99, 235, 0.15)',
          },
        ],
      },
    },
    {
      id: 'channelPerformance',
      title: '渠道获客表现',
      data: {
        labels: chartMonths,
        datasets: [
          {
            label: '新增客户',
            data: chartMonths.map((month) => acquisitionByMonth[month] ?? 0),
            borderColor: '#16A34A',
            backgroundColor: 'rgba(22, 163, 74, 0.15)',
          },
          {
            label: '渠道花费',
            data: chartMonths.map((month) => spendByMonth[month] ?? 0),
            borderColor: '#F97316',
            backgroundColor: 'rgba(249, 115, 22, 0.15)',
          },
        ],
      },
    },
  ]

  return {
    templateId: template.id as TemplateId,
    metrics,
    charts,
    datasetSummary: [
      { dataset: 'subscriptions', rows: subscriptions.length, lastDate: latestMonthKey },
      { dataset: 'acquisition', rows: acquisition.length },
    ],
  }
}

export function calculateTemplate(
  templateId: TemplateId,
  datasets: TemplateDatasets,
  mappings: TemplateMappings,
): CalculationResult {
  const template = getTemplate(templateId)
  switch (templateId) {
    case 'b2b-saas':
      return b2bCalculator(datasets, mappings, template)
    case 'b2c-product':
      return b2cCalculator(datasets, mappings, template)
    default:
      return b2bCalculator(datasets, mappings, template)
  }
}

export function buildSummary(datasets: TemplateDatasets, mappings: TemplateMappings) {
  const summary: Record<DatasetType, DatasetSummary> = {
    subscriptions: { dataset: 'subscriptions', rows: datasets.subscriptions?.length ?? 0 },
    churn: { dataset: 'churn', rows: datasets.churn?.length ?? 0 },
    acquisition: { dataset: 'acquisition', rows: datasets.acquisition?.length ?? 0 },
  }

  if (datasets.subscriptions && datasets.subscriptions.length > 0) {
    const dateField = mappings.subscriptions?.date ?? 'date'
    const months = datasets.subscriptions
      .map((row) => row[dateField])
      .filter(Boolean)
      .map((date) => toMonthKey(date as string))
      .filter((key) => key !== 'Unknown')
    const lastMonth = sortByMonthKey(months).pop()
    summary.subscriptions.lastDate = lastMonth
  }

  return Object.values(summary)
}


