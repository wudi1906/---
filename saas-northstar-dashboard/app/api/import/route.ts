import { NextRequest, NextResponse } from 'next/server'
import { processImport, type ImportPayload } from '@/lib/importService'

export const runtime = 'nodejs'

export async function POST(request: NextRequest) {
  try {
    const body = (await request.json()) as Partial<ImportPayload>
    if (!body || typeof body.templateId !== 'string') {
      return NextResponse.json({ success: false, error: '缺少 templateId。' }, { status: 400 })
    }

    const payload: ImportPayload = {
      templateId: body.templateId,
      datasets: body.datasets ?? {},
      mappings: body.mappings ?? {},
    }

    const result = processImport(payload)

    return NextResponse.json({
      success: true,
      importId: result.importId,
      createdAt: result.createdAt,
      calculation: result.calculation,
      warnings: result.warnings ?? [],
    })
  } catch (error) {
    console.error('[api/import] error', error)
    return NextResponse.json({ success: false, error: error instanceof Error ? error.message : '导入失败' }, { status: 400 })
  }
}
