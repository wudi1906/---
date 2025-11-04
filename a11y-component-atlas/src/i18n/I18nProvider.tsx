'use client'

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'

import en from './en.json'
import zh from './zh.json'

export type SupportedLang = 'en' | 'zh'

type TranslationRecord = Record<string, unknown>

interface I18nContextValue {
  lang: SupportedLang
  setLang: (lang: SupportedLang) => void
  t: (key: string, fallback?: string, values?: Record<string, string | number>) => string
}

const defaultLang: SupportedLang = 'en'
const RESOURCES: Record<SupportedLang, TranslationRecord> = {
  en,
  zh,
}

const I18nContext = createContext<I18nContextValue | null>(null)

function resolveKey(resource: TranslationRecord, key: string): unknown {
  return key.split('.').reduce<unknown>((acc, segment) => {
    if (acc && typeof acc === 'object' && segment in acc) {
      return (acc as Record<string, unknown>)[segment]
    }
    return undefined
  }, resource)
}

function interpolate(template: string, values?: Record<string, string | number>): string {
  if (!values) return template
  return Object.keys(values).reduce((acc, variable) => {
    const matcher = new RegExp(`{{\s*${variable}\s*}}`, 'g')
    return acc.replace(matcher, String(values[variable]))
  }, template)
}

export function I18nProvider({ children, lang: externalLang }: { children: ReactNode; lang?: SupportedLang }) {
  const [lang, setLang] = useState<SupportedLang>(externalLang ?? defaultLang)

  useEffect(() => {
    if (externalLang && externalLang !== lang) {
      setLang(externalLang)
    }
  }, [externalLang, lang])

  const translations = useMemo(() => RESOURCES[lang] ?? RESOURCES[defaultLang], [lang])

  const translate = useCallback< I18nContextValue['t'] >((key, fallback, values) => {
    const resolved = resolveKey(translations, key)
    if (typeof resolved === 'string') {
      return interpolate(resolved, values)
    }
    if (Array.isArray(resolved)) {
      return resolved.join('\n')
    }
    if (fallback) {
      return interpolate(fallback, values)
    }
    return key
  }, [translations])

  const contextValue = useMemo<I18nContextValue>(() => ({
    lang,
    setLang,
    t: translate,
  }), [lang, translate])

  return <I18nContext.Provider value={contextValue}>{children}</I18nContext.Provider>
}

export function useI18n(): I18nContextValue {
  const context = useContext(I18nContext)
  if (!context) {
    throw new Error('useI18n must be used inside I18nProvider')
  }
  return context
}


