import { describe, it, expect } from 'vitest'

describe('Budgets progress bar logic', () => {
  const getBudgetSpent = (budget, transactions) => {
    if (!budget || !transactions) return '0.00'
    const spent = transactions
      .filter((t) => {
        if (budget.category_id && t.category_id !== budget.category_id) return false
        if (t.type !== 'expense') return false
        const txDate = new Date(t.transaction_date)
        const startDate = new Date(budget.start_date)
        const endDate = budget.end_date ? new Date(budget.end_date) : new Date()
        return txDate >= startDate && txDate <= endDate
      })
      .reduce((sum, t) => sum + parseFloat(t.amount), 0)
    return spent.toFixed(2)
  }

  const getProgressPercentage = (budget, transactions) => {
    if (!budget) return 0
    const spent = parseFloat(getBudgetSpent(budget, transactions))
    const percentage = (spent / budget.amount) * 100
    return Math.min(Math.round(percentage), 100)
  }

  const isAlertActive = (budget, transactions) => {
    return getProgressPercentage(budget, transactions) >= budget.alert_percentage
  }

  it('getBudgetSpent returns 0.00 when no transactions', () => {
    const budget = { id: 1, amount: 500, start_date: '2025-01-01', category_id: null }
    expect(getBudgetSpent(budget, [])).toBe('0.00')
  })

  it('getBudgetSpent filters by category when specified', () => {
    const budget = { id: 1, amount: 500, start_date: '2025-01-01', end_date: '2025-12-31', category_id: 3 }
    const transactions = [
      { category_id: 3, type: 'expense', amount: '100', transaction_date: '2025-06-15' },
      { category_id: 4, type: 'expense', amount: '200', transaction_date: '2025-06-15' },
      { category_id: 3, type: 'income', amount: '300', transaction_date: '2025-06-15' },
    ]
    expect(getBudgetSpent(budget, transactions)).toBe('100.00')
  })

  it('getBudgetSpent includes all expenses when no category filter', () => {
    const budget = { id: 1, amount: 1000, start_date: '2025-01-01', end_date: '2025-12-31', category_id: null }
    const transactions = [
      { category_id: 1, type: 'expense', amount: '150', transaction_date: '2025-06-15' },
      { category_id: 2, type: 'expense', amount: '250', transaction_date: '2025-06-15' },
    ]
    expect(getBudgetSpent(budget, transactions)).toBe('400.00')
  })

  it('getBudgetSpent filters by date range', () => {
    const budget = { id: 1, amount: 500, start_date: '2025-03-01', end_date: '2025-04-30', category_id: null }
    const transactions = [
      { category_id: 1, type: 'expense', amount: '100', transaction_date: '2025-02-15' },
      { category_id: 1, type: 'expense', amount: '200', transaction_date: '2025-03-15' },
      { category_id: 1, type: 'expense', amount: '300', transaction_date: '2025-05-01' },
    ]
    expect(getBudgetSpent(budget, transactions)).toBe('200.00')
  })

  it('getProgressPercentage returns correct value', () => {
    const budget = { id: 1, amount: 500, start_date: '2025-01-01', category_id: null, alert_percentage: 80 }
    const transactions = [
      { category_id: 1, type: 'expense', amount: '250', transaction_date: '2025-06-15' },
    ]
    expect(getProgressPercentage(budget, transactions)).toBe(50)
  })

  it('getProgressPercentage caps at 100', () => {
    const budget = { id: 1, amount: 500, start_date: '2025-01-01', category_id: null, alert_percentage: 80 }
    const transactions = [
      { category_id: 1, type: 'expense', amount: '600', transaction_date: '2025-06-15' },
    ]
    expect(getProgressPercentage(budget, transactions)).toBe(100)
  })

  it('getProgressPercentage returns 0 when no budget', () => {
    expect(getProgressPercentage(null, [])).toBe(0)
  })

  it('isAlertActive returns true when percentage >= threshold', () => {
    const budget = { id: 1, amount: 100, start_date: '2025-01-01', category_id: null, alert_percentage: 80 }
    const transactions = [
      { category_id: 1, type: 'expense', amount: '85', transaction_date: '2025-06-15' },
    ]
    expect(isAlertActive(budget, transactions)).toBe(true)
  })

  it('isAlertActive returns false when percentage < threshold', () => {
    const budget = { id: 1, amount: 100, start_date: '2025-01-01', category_id: null, alert_percentage: 80 }
    const transactions = [
      { category_id: 1, type: 'expense', amount: '50', transaction_date: '2025-06-15' },
    ]
    expect(isAlertActive(budget, transactions)).toBe(false)
  })
})
