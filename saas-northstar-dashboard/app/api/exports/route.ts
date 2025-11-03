import { NextRequest, NextResponse } from 'next/server'
import { buildExport } from '@/lib/importService'

export const runtime = 'nodejs'

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const formatParam = (searchParams.get('format') ?? 'csv').toLowerCase()
  if (formatParam !== 'csv' && formatParam !== 'excel') {
    return NextResponse.json({ success: false, error: 'format 参数必须为 csv 或 excel。' }, { status: 400 })
  }

  try {
    const file = await buildExport(formatParam as 'csv' | 'excel')
    return new NextResponse(file.buffer, {
      headers: {
        'Content-Type': file.contentType,
        'Content-Disposition': `attachment; filename=${file.fileName}`,
        'Cache-Control': 'no-store',
      },
    })
  } catch (error) {
    const message = error instanceof Error ? error.message : '导出失败'
    const status = message.includes('没有可导出的') ? 404 : 500
    return NextResponse.json({ success: false, error: message }, { status })
  }
}
