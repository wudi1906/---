import { NextResponse } from 'next/server';

export async function POST() {
  try {
    // 重置数据由前端localStorage处理
    // 这里只返回成功响应
    
    return NextResponse.json({
      success: true,
      message: 'Data reset successful'
    });
  } catch (error) {
    return NextResponse.json(
      { success: false, error: 'Failed to reset data' },
      { status: 500 }
    );
  }
}

