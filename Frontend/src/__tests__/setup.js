import { vi } from 'vitest'

class LocalStorageMock {
  constructor() { this.store = {} }
  getItem(key) { return this.store[key] ?? null }
  setItem(key, value) { this.store[key] = String(value) }
  removeItem(key) { delete this.store[key] }
  clear() { this.store = {} }
  get length() { return Object.keys(this.store).length }
  key(index) { return Object.keys(this.store)[index] ?? null }
}

Object.defineProperty(globalThis, 'localStorage', {
  value: new LocalStorageMock(),
  writable: true,
  configurable: true,
})
