import { NextResponse } from 'next/server';

const HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  Vary: 'Origin',
};

export async function POST() {
  try {
    // 重置数据由前端localStorage处理
    // 这里只返回成功响应
    
    return NextResponse.json(
      {
        success: true,
        message: 'Data reset successful',
      },
      {
        status: 200,
        headers: HEADERS,
      }
    );
  } catch (error) {
    return NextResponse.json(
      { success: false, error: 'Failed to reset data' },
      { status: 500, headers: HEADERS }
    );
  }
}

export async function OPTIONS() {
  return new NextResponse(null, { status: 204, headers: HEADERS });
}

