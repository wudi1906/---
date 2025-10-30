'use client'

import { useMemo, useRef, useState } from 'react'
import { Line } from 'react-chartjs-2'
import type { ChartData, ChartOptions } from 'chart.js'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'
import html2canvas from 'html2canvas'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

interface TrendChartProps {
  title: string
  data: ChartData<'line'>
  height?: number
}

const palette = {
  light: {
    background: 'rgba(37, 99, 235, 0.15)',
    border: '#2563eb',
    grid: 'rgba(148, 163, 184, 0.25)',
    text: '#0f172a',
    tooltipBg: 'rgba(15, 23, 42, 0.9)',
    card: 'bg-white text-gray-900 border-gray-100',
  },
  dark: {
    background: 'rgba(96, 165, 250, 0.25)',
    border: '#60a5fa',
    grid: 'rgba(148, 163, 184, 0.2)',
    text: '#e2e8f0',
    tooltipBg: 'rgba(15, 23, 42, 0.95)',
    card: 'bg-slate-900 text-slate-100 border-slate-700',
  },
}

export default function TrendChart({ title, data, height = 300 }: TrendChartProps) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light')
  const [exporting, setExporting] = useState(false)
  const chartContainerRef = useRef<HTMLDivElement | null>(null)

  const themedData = useMemo<ChartData<'line'>>(() => {
    const activePalette = palette[theme]
    const datasets = (data.datasets ?? []).map(dataset => ({
      fill: dataset.fill ?? true,
      tension: dataset.tension ?? 0.4,
      pointRadius: dataset.pointRadius ?? 0,
      borderWidth: dataset.borderWidth ?? 2,
      ...dataset,
      borderColor: dataset.borderColor ?? activePalette.border,
      backgroundColor: dataset.backgroundColor ?? activePalette.background,
    }))

    return {
      ...data,
      datasets,
    }
  }, [data, theme])

  const options = useMemo<ChartOptions<'line'>>(() => {
    const activePalette = palette[theme]
    return {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
          labels: {
            color: activePalette.text,
          },
        },
        tooltip: {
          mode: 'index',
          intersect: false,
          backgroundColor: activePalette.tooltipBg,
          padding: 12,
          titleColor: '#fff',
          bodyColor: '#fff',
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1,
        },
        title: {
          color: activePalette.text,
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: activePalette.grid,
          },
          ticks: {
            color: activePalette.text,
            callback: (value) => {
              const numeric = typeof value === 'string' ? Number(value) : value
              return Number.isFinite(numeric) ? `$${Number(numeric).toLocaleString()}` : value
            },
          },
        },
        x: {
          grid: {
            color: theme === 'dark' ? 'rgba(148, 163, 184, 0.15)' : 'rgba(226, 232, 240, 0.6)',
          },
          ticks: {
            color: activePalette.text,
          },
        },
      },
      interaction: {
        mode: 'nearest',
        axis: 'x',
        intersect: false,
      },
    }
  }, [theme])

  const handleExport = async () => {
    if (!chartContainerRef.current) return
    try {
      setExporting(true)
      const canvas = await html2canvas(chartContainerRef.current, {
        backgroundColor: theme === 'dark' ? '#0f172a' : '#ffffff',
        scale: window.devicePixelRatio || 2,
      })
      const link = document.createElement('a')
      link.href = canvas.toDataURL('image/png')
      link.download = `${title.replace(/\s+/g, '-').toLowerCase()}-${Date.now()}.png`
      link.click()
    } catch (error) {
      console.error('Failed to export chart', error)
      alert('Failed to export chart. Please try again.')
    } finally {
      setExporting(false)
    }
  }

  return (
    <div className={`rounded-xl shadow-sm p-6 border transition-colors ${palette[theme].card}`}>
      <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
        <h3 className="text-lg font-semibold">{title}</h3>
        <div className="flex items-center gap-2">
          <div role="group" aria-label="Toggle chart theme" className="flex rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
            <button
              type="button"
              onClick={() => setTheme('light')}
              aria-pressed={theme === 'light'}
              className={`px-3 py-2 text-sm font-medium focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500 ${
                theme === 'light' ? 'bg-blue-600 text-white' : 'bg-transparent text-current'
              }`}
            >
              Light
            </button>
            <button
              type="button"
              onClick={() => setTheme('dark')}
              aria-pressed={theme === 'dark'}
              className={`px-3 py-2 text-sm font-medium focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500 ${
                theme === 'dark' ? 'bg-blue-600 text-white' : 'bg-transparent text-current'
              }`}
            >
              Dark
            </button>
          </div>
          <button
            type="button"
            onClick={handleExport}
            disabled={exporting}
            aria-label="导出图表为 PNG"
            className={`px-3 py-2 rounded-lg text-sm font-medium border focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500 ${
              exporting
                ? 'border-gray-200 dark:border-gray-700 text-gray-400 cursor-not-allowed'
                : 'border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-800'
            }`}
          >
            {exporting ? 'Exporting…' : 'Export PNG'}
          </button>
        </div>
      </div>
      <div ref={chartContainerRef} style={{ height: `${height}px` }}>
        <Line options={options} data={themedData} />
      </div>
    </div>
  )
}

