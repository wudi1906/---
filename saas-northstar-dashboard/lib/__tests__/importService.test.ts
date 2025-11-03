import { beforeEach, describe, expect, it } from 'vitest'
import { processImport, getLatestImport, buildExport } from '@/lib/importService'
import { getDb } from '@/lib/db'
import { SAMPLE_DATASETS, getTemplateById, type TemplateId } from '@/lib/kpiTemplates'
import type { TemplateDatasets, TemplateMappings } from '@/lib/kpiCalculator'

const TEMPLATE_ID = 'b2b-saas' as TemplateId

function buildPayload() {
  const template = getTemplateById(TEMPLATE_ID)
  const datasets: TemplateDatasets = {}
  const mappings: TemplateMappings = {}

  SAMPLE_DATASETS[TEMPLATE_ID].forEach((sample) => {
    datasets[sample.dataset] = sample.rows
  })

  template.datasets.forEach((dataset) => {
    mappings[dataset.id] = dataset.fields.reduce<Record<string, string>>((acc, field) => {
      acc[field.id] = field.id
      return acc
    }, {})
  })

  return { datasets, mappings }
}

beforeEach(() => {
  const db = getDb()
  db.exec('DELETE FROM imports')
})

describe('importService', () => {
  it('persists calculation results with valid payload', () => {
    const { datasets, mappings } = buildPayload()
    const result = processImport({ templateId: TEMPLATE_ID, datasets, mappings })

    expect(result.importId).toBeGreaterThan(0)
    expect(result.warnings).toBeUndefined()
    expect(result.calculation.metrics.length).toBeGreaterThan(0)

    const latest = getLatestImport()
    expect(latest).not.toBeNull()
    expect(latest?.templateId).toBe(TEMPLATE_ID)
  })

  it('returns warnings for invalid numeric values but still saves data', () => {
    const { datasets, mappings } = buildPayload()
    const corrupted = { ...datasets }
    if (corrupted.subscriptions) {
      corrupted.subscriptions = corrupted.subscriptions.map((row, index) => (
        index === 0 ? { ...row, amount: 'invalid-number' } : row
      ))
    }

    const result = processImport({ templateId: TEMPLATE_ID, datasets: corrupted, mappings })

    expect(result.importId).toBeGreaterThan(0)
    expect(result.warnings).toBeDefined()
    expect(result.warnings?.length).toBeGreaterThan(0)
  })

  it('throws when required mappings are missing', () => {
    const { datasets } = buildPayload()
    expect(() =>
      processImport({ templateId: TEMPLATE_ID, datasets, mappings: { subscriptions: {} } }),
    ).toThrow(/未映射|缺少/)
  })

  it('exports CSV and Excel after successful import', async () => {
    const { datasets, mappings } = buildPayload()
    processImport({ templateId: TEMPLATE_ID, datasets, mappings })

    const csv = await buildExport('csv')
    expect(csv.contentType).toContain('text/csv')
    expect(csv.buffer.byteLength).toBeGreaterThan(0)

    const excel = await buildExport('excel')
    expect(excel.contentType).toContain('spreadsheetml')
    expect(excel.buffer.byteLength).toBeGreaterThan(0)
  })
})
