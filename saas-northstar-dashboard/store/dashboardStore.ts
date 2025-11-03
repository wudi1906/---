import { create } from 'zustand'
import { DEFAULT_TEMPLATE_ID, KPI_TEMPLATES, SAMPLE_DATASETS, TemplateId, getTemplateById } from '@/lib/kpiTemplates'
import { calculateTemplate, TemplateDatasets, TemplateMappings, CalculationResult } from '@/lib/kpiCalculator'

export interface DashboardState {
  templateId: TemplateId
  metrics: CalculationResult['metrics']
  charts: CalculationResult['charts']
  datasetSummary: CalculationResult['datasetSummary']
  lastImportedAt?: string
  setFromCalculation: (result: CalculationResult) => void
  resetToTemplate: (templateId: TemplateId) => void
}

function buildInitialState(templateId: TemplateId): CalculationResult {
  const template = getTemplateById(templateId)
  const sample = SAMPLE_DATASETS[templateId] ?? []
  const datasets: TemplateDatasets = {}
  const mappings: TemplateMappings = {}

  sample.forEach((item) => {
    datasets[item.dataset] = item.rows
    mappings[item.dataset] = template.datasets
      .find((dataset) => dataset.id === item.dataset)?.fields.reduce((acc, field) => {
        acc[field.id] = field.id
        return acc
      }, {} as Record<string, string>) ?? {}
  })

  return calculateTemplate(templateId, datasets, mappings)
}

export const useDashboardStore = create<DashboardState>((set) => {
  const initial = buildInitialState(DEFAULT_TEMPLATE_ID)
  return {
    templateId: initial.templateId,
    metrics: initial.metrics,
    charts: initial.charts,
    datasetSummary: initial.datasetSummary,
    lastImportedAt: undefined,
    setFromCalculation: (result) =>
      set({
        templateId: result.templateId,
        metrics: result.metrics,
        charts: result.charts,
        datasetSummary: result.datasetSummary,
        lastImportedAt: new Date().toISOString(),
      }),
    resetToTemplate: (templateId) => {
      const fallback = buildInitialState(templateId)
      set({
        templateId,
        metrics: fallback.metrics,
        charts: fallback.charts,
        datasetSummary: fallback.datasetSummary,
        lastImportedAt: undefined,
      })
    },
  }
})

export const AVAILABLE_TEMPLATES = KPI_TEMPLATES

