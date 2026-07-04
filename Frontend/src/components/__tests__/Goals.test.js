import { describe, it, expect } from 'vitest'

describe('Goals progress bar logic', () => {
  const getGoalSaved = (goal, transactions) => {
    if (!goal.category_id) return 0
    return transactions
      .filter((t) => t.category_id === goal.category_id && t.type === 'income')
      .reduce((sum, t) => sum + parseFloat(t.amount), 0)
  }

  const getGoalProgress = (goal, transactions) => {
    const saved = getGoalSaved(goal, transactions)
    const target = parseFloat(goal.target_amount)
    if (!target) return 0
    return Math.min(Math.round((saved / target) * 100), 100)
  }

  it('getGoalSaved returns 0 when no category_id', () => {
    const goal = { id: 1, category_id: null, target_amount: '1000' }
    expect(getGoalSaved(goal, [])).toBe(0)
  })

  it('getGoalSaved sums income transactions for matching category', () => {
    const goal = { id: 1, category_id: 5, target_amount: '1000' }
    const transactions = [
      { category_id: 5, type: 'income', amount: '200' },
      { category_id: 5, type: 'income', amount: '300' },
      { category_id: 5, type: 'expense', amount: '100' },
      { category_id: 3, type: 'income', amount: '500' },
    ]
    expect(getGoalSaved(goal, transactions)).toBe(500)
  })

  it('getGoalSaved returns 0 when no matching income', () => {
    const goal = { id: 1, category_id: 5, target_amount: '1000' }
    const transactions = [
      { category_id: 5, type: 'expense', amount: '200' },
    ]
    expect(getGoalSaved(goal, transactions)).toBe(0)
  })

  it('getGoalProgress returns 0 for zero target', () => {
    const goal = { id: 1, category_id: null, target_amount: '0' }
    expect(getGoalProgress(goal, [])).toBe(0)
  })

  it('getGoalProgress calculates correct percentage', () => {
    const goal = { id: 1, category_id: 5, target_amount: '1000' }
    const transactions = [
      { category_id: 5, type: 'income', amount: '250' },
    ]
    expect(getGoalProgress(goal, transactions)).toBe(25)
  })

  it('getGoalProgress caps at 100%', () => {
    const goal = { id: 1, category_id: 5, target_amount: '1000' }
    const transactions = [
      { category_id: 5, type: 'income', amount: '2000' },
    ]
    expect(getGoalProgress(goal, transactions)).toBe(100)
  })

  it('getGoalProgress returns 0 for 0 saved and 0 target', () => {
    const goal = { id: 1, category_id: null, target_amount: '0' }
    expect(getGoalProgress(goal, [])).toBe(0)
  })

  it('getGoalSaved handles decimal amounts', () => {
    const goal = { id: 1, category_id: 3, target_amount: '500.50' }
    const transactions = [
      { category_id: 3, type: 'income', amount: '123.45' },
      { category_id: 3, type: 'income', amount: '67.89' },
    ]
    expect(parseFloat(getGoalSaved(goal, transactions).toFixed(2))).toBe(191.34)
  })
})
