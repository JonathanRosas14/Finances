import { describe, it, expect, beforeEach } from 'vitest'
import {
  readAppSettings,
  writeAppSettings,
  resetAppSettingsToDefaults,
  defaultSettings,
  STORAGE_KEY,
} from '../appSettings'

describe('appSettings', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('readAppSettings returns defaults when nothing stored', () => {
    const settings = readAppSettings()
    expect(settings).toEqual(defaultSettings)
  })

  it('readAppSettings returns stored values merged with defaults', () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ theme: 'dark' }))
    const settings = readAppSettings()
    expect(settings.theme).toBe('dark')
    expect(settings.locale).toBe('en-US')
    expect(settings.currencyCode).toBe('USD')
  })

  it('writeAppSettings stores and merges correctly', () => {
    writeAppSettings({ currencyCode: 'EUR' })
    const stored = JSON.parse(localStorage.getItem(STORAGE_KEY))
    expect(stored.currencyCode).toBe('EUR')
    expect(stored.theme).toBe('light')
  })

  it('readAppSettings returns defaults when storage has invalid JSON', () => {
    localStorage.setItem(STORAGE_KEY, 'not-json')
    const settings = readAppSettings()
    expect(settings).toEqual(defaultSettings)
  })

  it('resetAppSettingsToDefaults clears storage', () => {
    writeAppSettings({ theme: 'dark', locale: 'de-DE' })
    resetAppSettingsToDefaults()
    const settings = readAppSettings()
    expect(settings.theme).toBe('light')
    expect(settings.locale).toBe('en-US')
  })

  it('writeAppSettings dispatches fp-settings-changed event', () => {
    let dispatched = null
    window.addEventListener('fp-settings-changed', (e) => {
      dispatched = e.detail
    })
    writeAppSettings({ currencyCode: 'GBP' })
    expect(dispatched).not.toBeNull()
    expect(dispatched.currencyCode).toBe('GBP')
  })

  it('defaultSettings has expected structure', () => {
    expect(defaultSettings).toHaveProperty('theme')
    expect(defaultSettings).toHaveProperty('locale')
    expect(defaultSettings).toHaveProperty('currencyCode')
    expect(defaultSettings).toHaveProperty('dashboardDefaultPeriod')
  })
})
