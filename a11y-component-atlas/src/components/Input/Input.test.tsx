import { cleanup, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { axe } from 'vitest-axe'
import { describe, afterEach, it, expect, vi } from 'vitest'

import { Input } from './Input'

afterEach(() => {
  cleanup()
  document.body.innerHTML = ''
})

describe('Input', () => {
  it('associates label, helper text and error state accessibly', async () => {
    const { container, rerender } = render(
      <Input label="Email" placeholder="you@example.com" helperText="We never share your email" />
    )

    const field = screen.getByLabelText(/Email/)
    expect(field).toHaveAccessibleName('Email')
    expect(field).toHaveAttribute('aria-invalid', 'false')

    const helper = screen.getByText('We never share your email')
    expect(helper.id).toBe(field.getAttribute('aria-describedby'))

    let results = await axe(container)
    expect(results.violations).toHaveLength(0)

    rerender(<Input label="Email" error="Email is required" required />)

    const errorField = screen.getByLabelText(/Email/)
    expect(errorField).toHaveAttribute('aria-invalid', 'true')

    const errorMessage = screen.getByRole('alert')
    expect(errorMessage).toHaveTextContent('Email is required')
    expect(errorField).toHaveAttribute('aria-describedby', errorMessage.id)

    results = await axe(container)
    expect(results.violations).toHaveLength(0)
  })

  it('supports keyboard input and emits change events', async () => {
    const handleChange = vi.fn()
    const user = userEvent.setup()
    render(<Input label="Name" onChange={handleChange} />)

    const field = screen.getByLabelText('Name') as HTMLInputElement
    await user.type(field, 'Jane')

    expect(field.value).toBe('Jane')
    expect(handleChange).toHaveBeenCalled()
  })
})

