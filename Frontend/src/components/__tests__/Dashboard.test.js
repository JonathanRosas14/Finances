import { describe, it, expect } from 'vitest'

describe('Dashboard logic functions', () => {
  const toAmount = (value) => Number.parseFloat(value) || 0

  const getBudgetSpent = (budget, transactions) => {
    return transactions
      .filter((t) => {
        if (t.type !== 'expense') return false
        if (budget.category_id && t.category_id !== budget.category_id) return false
        if (!t.transaction_date || !budget.start_date) return true
        const txDate = new Date(t.transaction_date)
        const startDate = new Date(budget.start_date)
        const endDate = budget.end_date ? new Date(budget.end_date) : new Date()
        return txDate >= startDate && txDate <= endDate
      })
      .reduce((sum, t) => sum + toAmount(t.amount), 0)
  }

  const getGoalSaved = (goal, transactions) => {
    if (!goal.category_id) return 0
    return transactions
      .filter((t) => t.type === 'income' && t.category_id === goal.category_id)
      .reduce((sum, t) => sum + toAmount(t.amount), 0)
  }

  const getDebtPaid = (debt, transactions) => {
    if (!debt.category_id) return 0
    return transactions
      .filter((t) => t.type === 'expense' && t.category_id === debt.category_id)
      .reduce((sum, t) => sum + toAmount(t.amount), 0)
  }

  const getBarHeight = (amount, maxAmount) => {
    const height = (amount / maxAmount) * 170
    return `${Math.max(height, amount > 0 ? 12 : 0)}px`
  }

  const sumTransactions = (transactions, type) => {
    return transactions
      .filter((t) => t.type === type)
      .reduce((sum, t) => sum + toAmount(t.amount), 0)
  }

  const getPeriodTransactions = (transactions, period) => {
    if (period === 'all') return [...transactions]
    const today = new Date()
    const days = Number(period) || 30
    const startDate = new Date(today.getFullYear(), today.getMonth(), today.getDate() - days + 1)
    return transactions.filter((t) => {
      if (!t.transaction_date) return false
      return new Date(t.transaction_date) >= startDate
    })
  }

  it('toAmount converts string to number', () => {
    expect(toAmount('100.50')).toBe(100.5)
  })

  it('toAmount returns 0 for invalid input', () => {
    expect(toAmount('abc')).toBe(0)
  })

  it('toAmount returns 0 for null', () => {
    expect(toAmount(null)).toBe(0)
  })

  it('toAmount returns 0 for undefined', () => {
    expect(toAmount(undefined)).toBe(0)
  })

  it('sumTransactions sums income type', () => {
    const tx = [
      { type: 'income', amount: '100' },
      { type: 'income', amount: '200' },
      { type: 'expense', amount: '50' },
    ]
    expect(sumTransactions(tx, 'income')).toBe(300)
  })

  it('sumTransactions sums expense type', () => {
    const tx = [
      { type: 'income', amount: '100' },
      { type: 'expense', amount: '50' },
      { type: 'expense', amount: '25' },
    ]
    expect(sumTransactions(tx, 'expense')).toBe(75)
  })

  it('sumTransactions returns 0 for empty array', () => {
    expect(sumTransactions([], 'income')).toBe(0)
  })

  it('getBudgetSpent returns correct spent amount', () => {
    const budget = { id: 1, category_id: null, start_date: '2025-01-01', amount: 1000 }
    const tx = [
      { type: 'expense', amount: '200', category_id: 1, transaction_date: '2025-06-15' },
      { type: 'expense', amount: '100', category_id: 2, transaction_date: '2025-06-15' },
    ]
    expect(getBudgetSpent(budget, tx)).toBe(300)
  })

  it('getBudgetSpent filters by category', () => {
    const budget = { id: 1, category_id: 3, start_date: '2025-01-01', amount: 500 }
    const tx = [
      { type: 'expense', amount: '200', category_id: 3, transaction_date: '2025-06-15' },
      { type: 'expense', amount: '100', category_id: 4, transaction_date: '2025-06-15' },
    ]
    expect(getBudgetSpent(budget, tx)).toBe(200)
  })

  it('getBudgetSpent returns 0 for no matching expenses', () => {
    const budget = { id: 1, category_id: null, start_date: '2025-01-01', amount: 500 }
    const tx = [{ type: 'income', amount: '200', category_id: 1, transaction_date: '2025-06-15' }]
    expect(getBudgetSpent(budget, tx)).toBe(0)
  })

  it('getGoalSaved returns correct saved amount', () => {
    const goal = { id: 1, category_id: 5, target_amount: '1000' }
    const tx = [
      { type: 'income', amount: '300', category_id: 5 },
      { type: 'income', amount: '200', category_id: 5 },
      { type: 'expense', amount: '100', category_id: 5 },
    ]
    expect(getGoalSaved(goal, tx)).toBe(500)
  })

  it('getGoalSaved returns 0 when no category', () => {
    const goal = { id: 1, category_id: null, target_amount: '1000' }
    expect(getGoalSaved(goal, [])).toBe(0)
  })

  it('getDebtPaid returns correct paid amount', () => {
    const debt = { id: 1, category_id: 3, total_with_interest: '5000' }
    const tx = [
      { type: 'expense', amount: '500', category_id: 3 },
      { type: 'expense', amount: '250', category_id: 3 },
      { type: 'expense', amount: '100', category_id: 4 },
    ]
    expect(getDebtPaid(debt, tx)).toBe(750)
  })

  it('getDebtPaid returns 0 when no category', () => {
    const debt = { id: 1, category_id: null, total_with_interest: '5000' }
    expect(getDebtPaid(debt, [])).toBe(0)
  })

  it('getBarHeight returns correct height', () => {
    expect(getBarHeight(500, 1000)).toBe('85px')
  })

  it('getBarHeight returns minimum height for positive amount', () => {
    const height = getBarHeight(1, 1000)
    expect(height).toBe('12px')
  })

  it('getBarHeight returns 0px for zero amount', () => {
    expect(getBarHeight(0, 1000)).toBe('0px')
  })
})
