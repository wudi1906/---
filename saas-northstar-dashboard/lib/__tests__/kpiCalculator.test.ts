import { describe, expect, it } from 'vitest'
import { calculateTemplate } from '@/lib/kpiCalculator'
import { SAMPLE_DATASETS, DEFAULT_TEMPLATE_ID, getTemplateById } from '@/lib/kpiTemplates'

describe('kpiCalculator', () => {
  it('calculates B2B SaaS template correctly with sample data', () => {
    const templateId = DEFAULT_TEMPLATE_ID
    const sample = SAMPLE_DATASETS[templateId]
    const template = getTemplateById(templateId)
    const datasets: Record<string, Record<string, string>[]> = {}
    sample.forEach((item) => {
      datasets[item.dataset] = item.rows
    })
    const mappings: Record<string, Record<string, string>> = {}
    template.datasets.forEach((dataset) => {
      mappings[dataset.id] = dataset.fields.reduce<Record<string, string>>((acc, field) => {
        acc[field.id] = field.id
        return acc
      }, {})
    })

    const result = calculateTemplate(templateId, datasets, mappings)

    const mrrMetric = result.metrics.find((metric) => metric.id === 'mrr')
    const churnMetric = result.metrics.find((metric) => metric.id === 'churnRate')

    expect(mrrMetric).toBeDefined()
    expect(mrrMetric?.value).toBeGreaterThan(0)
    expect(churnMetric?.value).toBeGreaterThanOrEqual(0)
    expect(result.charts).toHaveLength(2)
  })

  it('calculates B2C template metrics', () => {
    const templateId = 'b2c-product'
    const sample = SAMPLE_DATASETS[templateId]
    const template = getTemplateById(templateId)
    const datasets: Record<string, Record<string, string>[]> = {}
    sample.forEach((item) => {
      datasets[item.dataset] = item.rows
    })
    const mappings: Record<string, Record<string, string>> = {}
    template.datasets.forEach((dataset) => {
      mappings[dataset.id] = dataset.fields.reduce<Record<string, string>>((acc, field) => {
        acc[field.id] = field.id
        return acc
      }, {})
    })

    const result = calculateTemplate(templateId, datasets, mappings)

    expect(result.metrics.find((metric) => metric.id === 'activeCustomers')?.value).toBeGreaterThan(0)
    expect(result.metrics.find((metric) => metric.id === 'cac')?.value).toBeGreaterThanOrEqual(0)
    expect(result.charts[0].data.labels.length).toBeGreaterThan(0)
  })
})

