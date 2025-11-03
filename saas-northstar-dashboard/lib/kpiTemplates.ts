import { parseISO } from 'date-fns'

export type DatasetType = 'subscriptions' | 'churn' | 'acquisition'

export interface TemplateField {
  id: string
  label: string
  description: string
  example?: string
  required?: boolean
}

export interface DatasetTemplate {
  id: DatasetType
  label: string
  description: string
  optional?: boolean
  fields: TemplateField[]
  sample?: string
}

export type MetricFormat = 'currency' | 'percentage' | 'number'

export interface MetricDefinition {
  id: string
  title: string
  subtitle: string
  description: string
  format: MetricFormat
  currency?: string
}

export interface ChartDefinition {
  id: string
  title: string
  description: string
}

export interface KpiTemplate {
  id: string
  name: string
  category: string
  description: string
  recommendedFor: string
  datasets: DatasetTemplate[]
  metrics: MetricDefinition[]
  charts: ChartDefinition[]
}

export const KPI_TEMPLATES: KpiTemplate[] = [
  {
    id: 'b2b-saas',
    name: 'B2B SaaS Northstar',
    category: 'B2B / Enterprise',
    description:
      '跟踪经常性收入、流失与生命周期价值，适用于订阅制 B2B SaaS 团队，包含 MRR、ARR、Churn、LTV 等关键指标。',
    recommendedFor: '面向企业客户的订阅式产品、需要月度/年度收入与流失洞察的团队。',
    datasets: [
      {
        id: 'subscriptions',
        label: 'Subscription Revenue',
        description: '每条代表一笔订阅收入或续费记录。',
        fields: [
          { id: 'date', label: 'Date', description: '交易日期 (YYYY-MM-DD)', example: '2024-02-01', required: true },
          { id: 'customerId', label: 'Customer ID', description: '客户唯一标识', example: 'C0001', required: true },
          { id: 'plan', label: 'Plan', description: '订阅套餐名称', example: 'Pro Plan' },
          { id: 'amount', label: 'Amount', description: '收入金额（数字）', example: '129', required: true },
          { id: 'currency', label: 'Currency', description: '货币符号/代码', example: 'USD' },
        ],
        sample: `date,customer_id,plan,amount,currency
2024-01-01,C0001,Pro,129,USD
2024-01-01,C0002,Basic,49,USD`,
      },
      {
        id: 'churn',
        label: 'Churned Customers',
        description: '客户流失记录，用于计算 Churn 与 LTV。',
        optional: false,
        fields: [
          { id: 'date', label: 'Date', description: '流失日期', example: '2024-01-20', required: true },
          { id: 'customerId', label: 'Customer ID', description: '流失客户 ID', example: 'C0009', required: true },
          { id: 'reason', label: 'Reason', description: '流失原因', example: 'price' },
        ],
        sample: `date,customer_id,reason
2024-01-15,C0007,price
2024-01-28,C0008,missing feature`,
      },
      {
        id: 'acquisition',
        label: 'Acquisition Spend',
        description: '获客渠道成本与新增客户数，用于计算 CAC 与转化率。',
        optional: true,
        fields: [
          { id: 'date', label: 'Date', description: '获客时间', example: '2024-01-10', required: true },
          { id: 'channel', label: 'Channel', description: '渠道名称', example: 'Paid Ads', required: true },
          { id: 'cost', label: 'Cost', description: '渠道花费', example: '1200', required: true },
          { id: 'customers', label: 'Customers', description: '来源于该渠道的新增客户数', example: '15', required: true },
        ],
        sample: `date,channel,cost,customers
2024-01-01,Paid Ads,1200,12
2024-01-05,Webinar,400,8`,
      },
    ],
    metrics: [
      {
        id: 'mrr',
        title: '月度经常性收入',
        subtitle: 'MRR',
        description: '最近完整月的订阅收入总和。',
        format: 'currency',
        currency: 'USD',
      },
      {
        id: 'arr',
        title: '年度经常性收入',
        subtitle: 'ARR',
        description: 'MRR × 12，用于估算年度收入规模。',
        format: 'currency',
        currency: 'USD',
      },
      {
        id: 'churnRate',
        title: '客户流失率',
        subtitle: 'Churn Rate',
        description: '流失客户占总客户的比例。',
        format: 'percentage',
      },
      {
        id: 'ltv',
        title: '客户生命周期价值',
        subtitle: 'LTV',
        description: '根据 ARPU 与 Churn 估算的客户生命周期收益。',
        format: 'currency',
        currency: 'USD',
      },
    ],
    charts: [
      {
        id: 'revenueTrend',
        title: 'MRR 趋势',
        description: '按月展示订阅收入变动。',
      },
      {
        id: 'acquisitionTrend',
        title: '获客与流失对比',
        description: '对比每月新增客户与流失客户数量。',
      },
    ],
  },
  {
    id: 'b2c-product',
    name: 'B2C Growth Dashboard',
    category: 'B2C / Product-led',
    description:
      '聚焦用户规模、转化率与获客成本，适用于面向消费者的订阅或一次性购买类产品。',
    recommendedFor: '消费级产品、应用内订阅、增长团队需要统一可视化。',
    datasets: [
      {
        id: 'subscriptions',
        label: 'Revenue / Orders',
        description: '每条记录代表一个订单或订阅。',
        fields: [
          { id: 'date', label: 'Date', description: '订单日期', example: '2024-01-03', required: true },
          { id: 'customerId', label: 'User ID', description: '用户 ID', example: 'U1023', required: true },
          { id: 'amount', label: 'Order Amount', description: '订单金额', example: '59', required: true },
          { id: 'currency', label: 'Currency', description: '货币符号/代码', example: 'USD' },
        ],
      },
      {
        id: 'acquisition',
        label: 'Acquisition Channels',
        description: '各渠道花费与获客数量。',
        fields: [
          { id: 'date', label: 'Date', description: '日期', required: true },
          { id: 'channel', label: 'Channel', description: '渠道名称', required: true },
          { id: 'cost', label: 'Spend', description: '渠道花费', required: true },
          { id: 'visitors', label: 'Visitors', description: '访问量', example: '1200' },
          { id: 'customers', label: 'Conversions', description: '转化/购买用户数', required: true },
        ],
      },
    ],
    metrics: [
      {
        id: 'activeCustomers',
        title: '活跃用户',
        subtitle: 'Active Customers',
        description: '最近周期内有订单的独立用户数。',
        format: 'number',
      },
      {
        id: 'conversionRate',
        title: '转化率',
        subtitle: 'Conversion',
        description: '获客渠道转化用户占比。',
        format: 'percentage',
      },
      {
        id: 'averageOrderValue',
        title: '平均订单金额',
        subtitle: 'AOV',
        description: '总收入 / 订单数。',
        format: 'currency',
        currency: 'USD',
      },
      {
        id: 'cac',
        title: '获客成本',
        subtitle: 'CAC',
        description: '渠道总花费 / 新增客户数。',
        format: 'currency',
        currency: 'USD',
      },
    ],
    charts: [
      {
        id: 'revenueByMonth',
        title: '月度收入趋势',
        description: '按月汇总消费收入。',
      },
      {
        id: 'channelPerformance',
        title: '渠道获客表现',
        description: '展示各渠道转化与花费对比。',
      },
    ],
  },
]

export type TemplateId = (typeof KPI_TEMPLATES)[number]['id']

export const DEFAULT_TEMPLATE_ID: TemplateId = 'b2b-saas'

export interface SampleDataset {
  dataset: DatasetType
  rows: Record<string, string>[]
}

export const SAMPLE_DATASETS: Record<TemplateId, SampleDataset[]> = {
  'b2b-saas': [
    {
      dataset: 'subscriptions',
      rows: [
        { date: '2024-01-01', customerId: 'C0001', plan: 'Pro', amount: '129', currency: 'USD' },
        { date: '2024-01-10', customerId: 'C0002', plan: 'Growth', amount: '249', currency: 'USD' },
        { date: '2024-02-02', customerId: 'C0001', plan: 'Pro', amount: '129', currency: 'USD' },
        { date: '2024-02-15', customerId: 'C0003', plan: 'Starter', amount: '79', currency: 'USD' },
        { date: '2024-03-05', customerId: 'C0002', plan: 'Growth', amount: '249', currency: 'USD' },
        { date: '2024-03-16', customerId: 'C0004', plan: 'Starter', amount: '79', currency: 'USD' },
      ],
    },
    {
      dataset: 'churn',
      rows: [
        { date: '2024-02-20', customerId: 'C0005', reason: 'budget' },
        { date: '2024-03-12', customerId: 'C0003', reason: 'missing feature' },
      ],
    },
    {
      dataset: 'acquisition',
      rows: [
        { date: '2024-01-01', channel: 'Paid Ads', cost: '1200', customers: '12' },
        { date: '2024-01-15', channel: 'Webinar', cost: '450', customers: '8' },
        { date: '2024-02-03', channel: 'Partner', cost: '600', customers: '10' },
        { date: '2024-03-01', channel: 'Paid Ads', cost: '1500', customers: '14' },
      ],
    },
  ],
  'b2c-product': [
    {
      dataset: 'subscriptions',
      rows: [
        { date: '2024-01-04', customerId: 'U1001', amount: '59', currency: 'USD' },
        { date: '2024-01-06', customerId: 'U1002', amount: '39', currency: 'USD' },
        { date: '2024-02-11', customerId: 'U1010', amount: '69', currency: 'USD' },
        { date: '2024-02-21', customerId: 'U1022', amount: '49', currency: 'USD' },
        { date: '2024-03-08', customerId: 'U1001', amount: '59', currency: 'USD' },
      ],
    },
    {
      dataset: 'acquisition',
      rows: [
        { date: '2024-01-01', channel: 'Paid Ads', cost: '800', customers: '20', visitors: '1200' },
        { date: '2024-01-12', channel: 'Influencer', cost: '300', customers: '11', visitors: '500' },
        { date: '2024-02-03', channel: 'Organic', cost: '0', customers: '18', visitors: '1400' },
        { date: '2024-03-09', channel: 'Referral', cost: '150', customers: '9', visitors: '400' },
      ],
    },
  ],
}

export function getTemplateById(templateId: TemplateId): KpiTemplate {
  const template = KPI_TEMPLATES.find((tpl) => tpl.id === templateId)
  if (!template) {
    throw new Error(`Template ${templateId} not found`)
  }
  return template
}

export function sortByMonthKey(keys: string[]): string[] {
  return [...keys].sort((a, b) => {
    const dateA = parseISO(`${a}-01`)
    const dateB = parseISO(`${b}-01`)
    return dateA.getTime() - dateB.getTime()
  })
}

