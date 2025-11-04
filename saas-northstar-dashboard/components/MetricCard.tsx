'use client'

import { useMemo } from 'react'
import { useTranslation } from '@/lib/i18n'

interface MetricCardProps {
  title: string
  subtitle: string
  value: number
  change: number
  currency?: string
  format?: 'currency' | 'percentage' | 'number'
}

export default function MetricCard({
  title,
  subtitle,
  value,
  change,
  currency = 'USD',
  format = 'currency'
}: MetricCardProps) {
  const { t, formatCurrency, formatNumber, formatPercentage } = useTranslation()

  const formattedValue = useMemo(() => {
    if (format === 'currency') {
      return formatCurrency(value, currency)
    }
    if (format === 'percentage') {
      return formatPercentage(value)
    }
    return formatNumber(value)
  }, [format, value, currency, formatCurrency, formatNumber, formatPercentage])

  const isPositive = change >= 0
  const changeColor = isPositive ? 'text-green-600' : 'text-red-600'
  const changeBg = isPositive ? 'bg-green-50' : 'bg-red-50'
  const changeValue = formatNumber(Math.abs(change))
  const changeLabel = t(
    isPositive ? 'metrics.change.up' : 'metrics.change.down',
    `${isPositive ? 'Increase' : 'Decrease'} of ${changeValue}%`,
    { value: changeValue }
  )
  const changeDisplay = `${isPositive ? '↑' : '↓'} ${changeValue}%`

  return (
    <div className="rounded-xl bg-white p-6 shadow-sm transition-shadow hover:shadow-md dark:bg-gray-800">
      <div className="mb-2 flex items-center justify-between">
        <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">{title}</h3>
        <span
          className={`px-2 py-1 text-xs font-medium ${changeBg} ${changeColor} rounded-full`}
          aria-label={changeLabel}
        >
          {changeDisplay}
        </span>
      </div>
      <div className="flex items-baseline gap-2">
        <p className="text-3xl font-bold text-gray-900 dark:text-white">{formattedValue}</p>
        <span className="text-sm text-gray-500 dark:text-gray-400">{subtitle}</span>
      </div>
    </div>
  )
}

