import { NextResponse } from 'next/server'
import { KPI_TEMPLATES } from '@/lib/kpiTemplates'

export const dynamic = 'force-static'

export async function GET() {
  const templates = KPI_TEMPLATES.map((template) => ({
    id: template.id,
    name: template.name,
    category: template.category,
    description: template.description,
    recommendedFor: template.recommendedFor,
    datasets: template.datasets.map((dataset) => ({
      id: dataset.id,
      label: dataset.label,
      description: dataset.description,
      optional: dataset.optional ?? false,
      fields: dataset.fields.map((field) => ({
        id: field.id,
        label: field.label,
        description: field.description,
        required: field.required !== false,
      })),
    })),
    metrics: template.metrics.map((metric) => ({
      id: metric.id,
      title: metric.title,
      subtitle: metric.subtitle,
      format: metric.format,
    })),
  }))

  return NextResponse.json({ templates })
}

