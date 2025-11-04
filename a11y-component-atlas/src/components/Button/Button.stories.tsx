import type { Meta, StoryObj } from '@storybook/react'
import type { ComponentProps } from 'react'
import { Button } from './Button'
import { useI18n } from '@/i18n'

type ButtonProps = ComponentProps<typeof Button>

interface TranslatedButtonProps extends Omit<ButtonProps, 'children'> {
  labelKey: string
}

function TranslatedButton({ labelKey, ...rest }: TranslatedButtonProps) {
  const { t } = useI18n()
  return <Button {...rest}>{t(labelKey)}</Button>
}

const meta: Meta<typeof TranslatedButton> = {
  title: 'Components/Button',
  component: TranslatedButton,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'danger', 'outline'],
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
    },
    labelKey: {
      control: false,
      table: { disable: true },
    },
  },
}

export default meta
type Story = StoryObj<typeof TranslatedButton>

export const Primary: Story = {
  args: {
    labelKey: 'button.labels.primary',
    variant: 'primary',
  },
}

export const Secondary: Story = {
  args: {
    labelKey: 'button.labels.secondary',
    variant: 'secondary',
  },
}

export const Danger: Story = {
  args: {
    labelKey: 'button.labels.danger',
    variant: 'danger',
  },
}

export const Outline: Story = {
  args: {
    labelKey: 'button.labels.outline',
    variant: 'outline',
  },
}

export const Small: Story = {
  args: {
    labelKey: 'button.labels.small',
    size: 'sm',
  },
}

export const Large: Story = {
  args: {
    labelKey: 'button.labels.large',
    size: 'lg',
  },
}

export const Disabled: Story = {
  args: {
    labelKey: 'button.labels.disabled',
    disabled: true,
  },
}

