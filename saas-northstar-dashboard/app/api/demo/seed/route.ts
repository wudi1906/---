import { NextResponse } from 'next/server';

const HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Vary': 'Origin',
};

// 示例KPI数据(30天)
function generateSeedData() {
  const data = [];
  const baseDate = new Date();
  
  for (let i = 30; i >= 0; i--) {
    const date = new Date(baseDate);
    date.setDate(date.getDate() - i);
    
    data.push({
      date: date.toISOString().split('T')[0],
      mrr: 45000 + Math.random() * 10000,
      arr: (45000 + Math.random() * 10000) * 12,
      activeUsers: 1200 + Math.floor(Math.random() * 300),
      churnRate: 2 + Math.random() * 3,
      nps: 45 + Math.floor(Math.random() * 20),
      ltv: 12000 + Math.random() * 5000,
      cac: 800 + Math.random() * 400,
    });
  }
  
  return data;
}

export async function POST() {
  try {
    const seedData = generateSeedData();
    
    // 存储到localStorage将由前端处理
    // 这里只返回数据供前端使用
    
    return NextResponse.json(
      {
        success: true,
        data: seedData,
        count: seedData.length,
      },
      {
        status: 200,
        headers: HEADERS,
      }
    );
  } catch (error) {
    return NextResponse.json(
      { success: false, error: 'Failed to seed data' },
      { status: 500, headers: HEADERS }
    );
  }
}

export async function OPTIONS() {
  return new NextResponse(null, { status: 204, headers: HEADERS });
}

