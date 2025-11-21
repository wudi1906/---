import React from 'react'
import { cn } from '@/lib/utils'

export interface AuditMetric {
  label: string
  score: number // 0 - 100
  status: 'pass' | 'warn' | 'fail'
  description?: string
}

export interface AuditScoreCardProps {
  componentName: string
  overallScore: number
  audits: AuditMetric[]
  lastRun?: string
  notes?: string
}

const statusStyles: Record<AuditMetric['status'], string> = {
  pass: 'bg-emerald-50 text-emerald-700 border-emerald-100',
  warn: 'bg-amber-50 text-amber-700 border-amber-100',
  fail: 'bg-rose-50 text-rose-700 border-rose-100',
}

export function AuditScoreCard({
  componentName,
  overallScore,
  audits,
  lastRun,
  notes,
}: AuditScoreCardProps) {
  const normalizedScore = React.useMemo(() => Math.min(Math.max(overallScore, 0), 100), [overallScore])
  const ringColor = normalizedScore > 85 ? 'text-emerald-500' : normalizedScore > 60 ? 'text-amber-500' : 'text-rose-500'
  const badgeText = normalizedScore > 95 ? 'AAA Ready' : normalizedScore > 85 ? 'AA Ready' : 'Needs Attention'

  return (
    <section
      className="w-full rounded-2xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-900"
      aria-labelledby="a11y-audit-heading"
    >
      <div className="flex flex-col gap-6 lg:flex-row">
        <div className="flex flex-1 items-center gap-4">
          <div className="relative h-24 w-24" aria-hidden="true">
            <svg className="h-full w-full" viewBox="0 0 120 120">
              <circle
                className="text-gray-200"
                strokeWidth="12"
                stroke="currentColor"
                fill="transparent"
                r="52"
                cx="60"
                cy="60"
              />
              <circle
                className={cn('transition-all duration-500 ease-out', ringColor)}
                strokeWidth="12"
                stroke="currentColor"
                strokeLinecap="round"
                fill="transparent"
                r="52"
                cx="60"
                cy="60"
                style={{ strokeDasharray: 326.72, strokeDashoffset: 326.72 - (326.72 * normalizedScore) / 100 }}
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-3xl font-bold text-gray-900 dark:text-white">{normalizedScore}</span>
              <span className="text-xs text-gray-500">/100</span>
            </div>
          </div>
          <div>
            <p id="a11y-audit-heading" className="text-sm uppercase tracking-wide text-gray-500">
              Accessibility Audit
            </p>
            <h3 className="text-2xl font-semibold text-gray-900 dark:text-white">{componentName}</h3>
            <p className="mt-1 inline-flex items-center gap-2 rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700 dark:bg-indigo-900/40 dark:text-indigo-300">
              {badgeText}
            </p>
            {lastRun && <p className="mt-2 text-xs text-gray-500">Last audit: {lastRun}</p>}
          </div>
        </div>

        <div className="flex flex-1 flex-col gap-3" aria-live="polite">
          {audits.map((audit) => (
            <div
              key={audit.label}
              className={cn(
                'flex items-center justify-between rounded-xl border px-4 py-3 text-sm font-medium shadow-sm',
                statusStyles[audit.status]
              )}
            >
              <div>
                <p className="text-xs uppercase tracking-wide text-gray-500">{audit.label}</p>
                <p className="text-base text-gray-900 dark:text-white">{audit.description || 'Meets requirement'}</p>
              </div>
              <div className="text-2xl font-semibold">{audit.score}</div>
            </div>
          ))}
        </div>
      </div>

      {notes && (
        <div className="mt-4 rounded-xl bg-slate-50 p-4 text-sm text-slate-600 dark:bg-slate-800/60 dark:text-slate-300">
          <p className="font-semibold text-slate-800 dark:text-white">Notes</p>
          <p className="mt-1 leading-relaxed">{notes}</p>
        </div>
      )}
    </section>
  )
}

AuditScoreCard.displayName = 'AuditScoreCard'
