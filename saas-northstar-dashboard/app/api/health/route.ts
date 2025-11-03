import { NextResponse } from 'next/server'

export const dynamic = 'force-static'

export async function GET() {
  return new NextResponse(
    JSON.stringify({
      status: 'healthy',
      app: 'saas-northstar-dashboard',
      version: '1.0.0',
      timestamp: new Date().toISOString(),
    }),
    {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=15',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
      },
    }
  )
}

