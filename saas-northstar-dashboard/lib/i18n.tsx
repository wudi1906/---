'use client'

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'next/navigation'

import en from '@/locales/en.json'
import zh from '@/locales/zh.json'

type SupportedLang = 'en' | 'zh'

type TranslationRecord = Record<string, unknown>

interface TranslationContextValue {
  lang: SupportedLang
  setLang: (lang: SupportedLang) => void
  t: (key: string, fallback?: string, values?: Record<string, string | number>) => string
  formatCurrency: (value: number, currency?: string) => string
  formatNumber: (value: number) => string
  formatPercentage: (value: number, fractionDigits?: number) => string
}

const STORAGE_KEY = 'northstar-lang'
const SUPPORTED_LANGS: SupportedLang[] = ['en', 'zh']
const RESOURCES: Record<SupportedLang, TranslationRecord> = {
  en,
  zh,
}

const TranslationContext = createContext<TranslationContextValue | null>(null)

function resolveNestedValue(resource: TranslationRecord, key: string): unknown {
  return key.split('.').reduce<unknown>((accumulator, segment) => {
    if (accumulator && typeof accumulator === 'object' && segment in accumulator) {
      return (accumulator as Record<string, unknown>)[segment]
    }
    return undefined
  }, resource)
}

function applyInterpolation(content: string, values?: Record<string, string | number>): string {
  if (!values) return content
  return Object.keys(values).reduce((output, variable) => {
    const pattern = new RegExp(`{{\s*${variable}\s*}}`, 'g')
    return output.replace(pattern, String(values[variable]))
  }, content)
}

function normalizeLang(candidate?: string | null): SupportedLang {
  if (!candidate) return 'en'
  const normalized = candidate.toLowerCase()
  if (SUPPORTED_LANGS.includes(normalized as SupportedLang)) {
    return normalized as SupportedLang
  }
  if (normalized.startsWith('zh')) return 'zh'
  return 'en'
}

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const searchParams = useSearchParams()
  const [lang, setLangState] = useState<SupportedLang>('en')

  useEffect(() => {
    const paramLang = searchParams?.get('lang')
    const storedLang = typeof window !== 'undefined' ? window.localStorage.getItem(STORAGE_KEY) : null
    const browserLang = typeof navigator !== 'undefined' ? navigator.language : 'en'

    const initial = normalizeLang(paramLang ?? storedLang ?? browserLang)
    setLangState(initial)
    if (typeof document !== 'undefined') {
      document.documentElement.lang = initial === 'zh' ? 'zh-CN' : 'en'
    }
  }, [searchParams])

  const updateLang = useCallback((nextLang: SupportedLang) => {
    setLangState(nextLang)
    if (typeof window !== 'undefined') {
      window.localStorage.setItem(STORAGE_KEY, nextLang)
      const url = new URL(window.location.href)
      url.searchParams.set('lang', nextLang)
      window.history.replaceState({}, '', url.toString())
    }
    if (typeof document !== 'undefined') {
      document.documentElement.lang = nextLang === 'zh' ? 'zh-CN' : 'en'
    }
  }, [])

  const translations = useMemo(() => RESOURCES[lang], [lang])

  const translate = useCallback<TranslationContextValue['t']>((key, fallback, values) => {
    const resolved = resolveNestedValue(translations, key)
    if (typeof resolved === 'string') {
      return applyInterpolation(resolved, values)
    }
    if (fallback) {
      return applyInterpolation(fallback, values)
    }
    return key
  }, [translations])

  const formatCurrency = useCallback<TranslationContextValue['formatCurrency']>((value, currency = 'USD') => {
    const locale = lang === 'zh' ? 'zh-CN' : 'en-US'
    return new Intl.NumberFormat(locale, {
      style: 'currency',
      currency,
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value)
  }, [lang])

  const formatNumber = useCallback<TranslationContextValue['formatNumber']>((value) => {
    const locale = lang === 'zh' ? 'zh-CN' : 'en-US'
    return new Intl.NumberFormat(locale, {
      maximumFractionDigits: 1,
    }).format(value)
  }, [lang])

  const formatPercentage = useCallback<TranslationContextValue['formatPercentage']>((value, fractionDigits = 1) => {
    const locale = lang === 'zh' ? 'zh-CN' : 'en-US'
    return new Intl.NumberFormat(locale, {
      style: 'percent',
      minimumFractionDigits: fractionDigits,
      maximumFractionDigits: fractionDigits,
    }).format(value / 100)
  }, [lang])

  const contextValue = useMemo<TranslationContextValue>(() => ({
    lang,
    setLang: updateLang,
    t: translate,
    formatCurrency,
    formatNumber,
    formatPercentage,
  }), [lang, updateLang, translate, formatCurrency, formatNumber, formatPercentage])

  return <TranslationContext.Provider value={contextValue}>{children}</TranslationContext.Provider>
}

export function useTranslation(): TranslationContextValue {
  const context = useContext(TranslationContext)
  if (!context) {
    throw new Error('useTranslation must be used within LanguageProvider')
  }
  return context
}


