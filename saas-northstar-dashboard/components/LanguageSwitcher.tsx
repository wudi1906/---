'use client'

import { useMemo, useState } from 'react'
import { useTranslation } from '@/lib/i18n'

export default function LanguageSwitcher() {
  const { lang, setLang, t } = useTranslation()
  const [open, setOpen] = useState(false)

  const options = useMemo(() => (
    [
      { code: 'en' as const, label: t('lang.options.en', 'English') },
      { code: 'zh' as const, label: t('lang.options.zh', '中文') },
    ]
  ), [t])

  return (
    <div className="relative" role="navigation" aria-label={t('lang.aria', 'Language selector')}>
      <button
        type="button"
        className="inline-flex items-center gap-2 rounded-full border border-slate-300 bg-white px-3 py-1.5 text-sm font-semibold text-slate-700 shadow-sm transition hover:border-blue-400 hover:text-blue-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:border-blue-400"
        onClick={() => setOpen((prev) => !prev)}
        aria-haspopup="true"
        aria-expanded={open}
      >
        <span aria-hidden>🌐</span>
        <span>{t('lang.toggle', lang === 'zh' ? '中文' : 'English')}</span>
      </button>
      {open && (
        <div
          className="absolute right-0 z-20 mt-2 w-40 overflow-hidden rounded-xl border border-slate-200 bg-white shadow-xl dark:border-slate-700 dark:bg-slate-900"
          role="menu"
        >
          {options.map((option) => (
            <button
              key={option.code}
              type="button"
              role="menuitemradio"
              aria-checked={lang === option.code}
              onClick={() => {
                setLang(option.code)
                setOpen(false)
              }}
              className={`flex w-full items-center justify-between px-4 py-2 text-sm font-medium transition hover:bg-slate-100 dark:hover:bg-slate-800 ${
                lang === option.code ? 'text-blue-600 dark:text-blue-300' : 'text-slate-600 dark:text-slate-200'
              }`}
            >
              <span>{option.label}</span>
              {lang === option.code && <span aria-hidden>✓</span>}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}


