import { describe, it, expect, beforeEach } from 'vitest'
import { showConfirm, completeConfirm, confirmDialogState } from '../confirmDialog'

describe('confirmDialog', () => {
  beforeEach(() => {
    confirmDialogState.visible = false
    confirmDialogState.title = ''
    confirmDialogState.message = ''
  })

  it('showConfirm sets default state', async () => {
    const promise = showConfirm()
    expect(confirmDialogState.visible).toBe(true)
    expect(confirmDialogState.title).toBe('Confirm')
    expect(confirmDialogState.confirmText).toBe('Confirm')
    expect(confirmDialogState.cancelText).toBe('Cancel')
    expect(confirmDialogState.variant).toBe('danger')
    completeConfirm(false)
    await expect(promise).resolves.toBe(false)
  })

  it('showConfirm respects custom options', async () => {
    const promise = showConfirm({
      title: 'Delete?',
      message: 'Are you sure?',
      confirmText: 'Yes',
      cancelText: 'No',
      variant: 'primary',
    })
    expect(confirmDialogState.title).toBe('Delete?')
    expect(confirmDialogState.message).toBe('Are you sure?')
    expect(confirmDialogState.confirmText).toBe('Yes')
    expect(confirmDialogState.cancelText).toBe('No')
    expect(confirmDialogState.variant).toBe('primary')
    completeConfirm(true)
    await expect(promise).resolves.toBe(true)
  })

  it('completeConfirm with true resolves promise to true', async () => {
    const promise = showConfirm()
    completeConfirm(true)
    await expect(promise).resolves.toBe(true)
    expect(confirmDialogState.visible).toBe(false)
  })

  it('completeConfirm with false resolves promise to false', async () => {
    const promise = showConfirm()
    completeConfirm(false)
    await expect(promise).resolves.toBe(false)
  })

  it('subsequent showConfirm rejects previous pending', async () => {
    const first = showConfirm()
    showConfirm()  // second call should reject first
    completeConfirm(true)
    await expect(first).resolves.toBe(false)
  })
})
