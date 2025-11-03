import { cleanup, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { axe } from 'vitest-axe'
import { describe, afterEach, it, expect, vi } from 'vitest'

import { Button } from './Button'

afterEach(() => {
  cleanup()
  document.body.innerHTML = ''
})

describe('Button', () => {
  it('passes axe accessibility check across primary variants', async () => {
    const { container, rerender } = render(
      <div className="flex gap-4">
        <Button>Primary</Button>
        <Button variant="secondary">Secondary</Button>
        <Button variant="danger">Danger</Button>
        <Button variant="outline">Outline</Button>
      </div>
    )

    let results = await axe(container)
    expect(results.violations).toHaveLength(0)

    rerender(
      <div className="flex gap-4">
        <Button size="sm">Small</Button>
        <Button size="md">Medium</Button>
        <Button size="lg">Large</Button>
      </div>
    )

    results = await axe(container)
    expect(results.violations).toHaveLength(0)
  })

  it('supports keyboard activation for Enter and Space', async () => {
    const handleClick = vi.fn()
    const user = userEvent.setup()
    render(
      <Button onClick={handleClick} aria-label="Submit">
        Submit
      </Button>
    )

    const button = screen.getByRole('button', { name: /submit/i })
    button.focus()
    expect(button).toHaveFocus()

    await user.keyboard('{Enter}')
    await user.keyboard(' ')

    expect(handleClick).toHaveBeenCalledTimes(2)
  })

  it('respects disabled state and prevents interaction', async () => {
    const handleClick = vi.fn()
    const user = userEvent.setup()
    render(
      <Button disabled onClick={handleClick} aria-label="Disabled">
        Disabled
      </Button>
    )

    const button = screen.getByRole('button', { name: /disabled/i })
    expect(button).toBeDisabled()

    await user.click(button)
    await user.keyboard('{Enter}')

    expect(handleClick).not.toHaveBeenCalled()
  })
})

