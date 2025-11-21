export interface ComponentAudit {
  name: string
  description: string
  score: number
  badge: 'AAA' | 'AA' | 'A' | 'Needs work'
  lastRun: string
  metrics: {
    label: string
    score: number
    status: 'pass' | 'warn' | 'fail'
    description: string
  }[]
  checklist: {
    label: string
    status: 'pass' | 'warn' | 'fail'
    details?: string
  }[]
  notes?: string
}

export const componentAudits: ComponentAudit[] = [
  {
    name: 'Button',
    description: 'Primary action button with keyboard focus ring and ARIA support.',
    score: 98,
    badge: 'AAA',
    lastRun: 'Nov 12, 2025 · Axe DevTools',
    metrics: [
      {
        label: 'Color Contrast',
        score: 100,
        status: 'pass',
        description: 'Meets 7.1:1 ratio on primary + danger variants',
      },
      {
        label: 'Keyboard Support',
        score: 100,
        status: 'pass',
        description: 'Fully tab-navigable with visible focus ring',
      },
      {
        label: 'ARIA Labels',
        score: 95,
        status: 'pass',
        description: 'Supports aria-pressed for toggle usage',
      },
    ],
    checklist: [
      { label: 'Focusable & 44px target', status: 'pass' },
      { label: 'ARIA state mapping', status: 'pass' },
      { label: 'Loading state announced', status: 'warn', details: 'Recommend aria-live region for asynchronous actions' },
    ],
    notes: 'Include aria-live="polite" on parent container when using button to trigger asynchronous operations.',
  },
  {
    name: 'Input',
    description: 'Text input with built-in label, helper text and error states.',
    score: 91,
    badge: 'AA',
    lastRun: 'Nov 11, 2025 · Lighthouse',
    metrics: [
      {
        label: 'Label Association',
        score: 100,
        status: 'pass',
        description: 'Explicit label + helper & error states supported',
      },
      {
        label: 'Error Messaging',
        score: 88,
        status: 'warn',
        description: 'aria-describedby toggles between helper and error text',
      },
      {
        label: 'Touch Target',
        score: 85,
        status: 'warn',
        description: 'Recommend adding 12px padding on compact layouts',
      },
    ],
    checklist: [
      { label: 'Label + describedby wiring', status: 'pass' },
      { label: 'ARIA invalid state', status: 'pass' },
      { label: 'Input mask announcement', status: 'warn', details: 'Provide instructions before input for screen readers' },
    ],
  },
]
