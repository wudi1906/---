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
  const formatValue = (val: number) => {
    if (format === 'currency') {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
      }).format(val)
    } else if (format === 'percentage') {
      return `${val.toFixed(1)}%`
    }
    return val.toLocaleString()
  }

  const isPositive = change >= 0
  const changeColor = isPositive ? 'text-green-600' : 'text-red-600'
  const changeBg = isPositive ? 'bg-green-50' : 'bg-red-50'

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
          {title}
        </h3>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${changeBg} ${changeColor}`}>
          {isPositive ? '↑' : '↓'} {Math.abs(change)}%
        </span>
      </div>
      <div className="flex items-baseline gap-2">
        <p className="text-3xl font-bold text-gray-900 dark:text-white">
          {formatValue(value)}
        </p>
        <span className="text-sm text-gray-500 dark:text-gray-400">
          {subtitle}
        </span>
      </div>
    </div>
  )
}

