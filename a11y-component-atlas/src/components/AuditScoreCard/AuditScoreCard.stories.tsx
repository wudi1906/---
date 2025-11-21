import type { Meta, StoryObj } from '@storybook/react'
import { AuditScoreCard } from './AuditScoreCard'
import { componentAudits } from '@/data/audits'

const meta: Meta<typeof AuditScoreCard> = {
  title: 'A11y/AuditScoreCard',
  component: AuditScoreCard,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'Highlights automated accessibility audit results (contrast, keyboard support, ARIA labels) so Fiverr clients can quickly evaluate compliance readiness.',
      },
    },
  },
}

export default meta

type Story = StoryObj<typeof AuditScoreCard>

export const ButtonAudit: Story = {
  args: {
    componentName: componentAudits[0].name,
    overallScore: componentAudits[0].score,
    audits: componentAudits[0].metrics,
    lastRun: componentAudits[0].lastRun,
    notes: componentAudits[0].notes,
  },
  render: (args) => (
    <div className="max-w-5xl mx-auto p-6 bg-slate-100 min-h-screen">
      <AuditScoreCard {...args} />
    </div>
  ),
}

export const InputAudit: Story = {
  args: {
    componentName: componentAudits[1].name,
    overallScore: componentAudits[1].score,
    audits: componentAudits[1].metrics,
    lastRun: componentAudits[1].lastRun,
    notes: componentAudits[1].notes,
  },
  render: ButtonAudit.render,
}
