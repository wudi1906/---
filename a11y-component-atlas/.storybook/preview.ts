import type { Decorator, Preview } from '@storybook/react'
import React from 'react'
import '../src/styles/globals.css'
import { I18nProvider, type SupportedLang } from '@/i18n'

const withI18n: Decorator = (Story, context) => {
  const lang = (context.globals.locale as SupportedLang) ?? 'en'
  return React.createElement(I18nProvider, {
    lang,
    children: React.createElement(Story, context.args as Record<string, unknown>),
  })
}

const preview: Preview = {
  globalTypes: {
    locale: {
      name: 'Language',
      description: 'Switch between supported languages',
      defaultValue: 'en',
      toolbar: {
        icon: 'globe',
        dynamicTitle: true,
        items: [
          { value: 'en', title: 'English' },
          { value: 'zh', title: '中文' },
        ],
      },
    },
  },
  decorators: [withI18n],
  parameters: {
    actions: { argTypesRegex: '^on[A-Z].*' },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/,
      },
    },
  },
}

export default preview

