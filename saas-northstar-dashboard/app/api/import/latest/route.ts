import { NextResponse } from 'next/server'
import { getLatestImport } from '@/lib/importService'

export const runtime = 'nodejs'

export async function GET() {
  const latest = getLatestImport()
  if (!latest) {
    return NextResponse.json({ success: false, error: '暂无导入记录' }, { status: 404 })
  }

  return NextResponse.json({
    success: true,
    calculation: latest.calculation,
    templateId: latest.templateId,
    createdAt: latest.createdAt,
  })
}
