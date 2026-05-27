import { describe, it, expect } from 'vitest'

describe('Debts progress bar and interest logic', () => {
  const getDebtPaid = (debt, transactions) => {
    if (!debt.category_id) return 0
    return transactions
      .filter((t) => t.category_id === debt.category_id && t.type === 'expense')
      .reduce((sum, t) => sum + parseFloat(t.amount), 0)
  }

  const getDebtProgress = (debt, transactions) => {
    const paid = getDebtPaid(debt, transactions)
    const total = parseFloat(debt.total_with_interest)
    if (!total) return 0
    return Math.min(Math.round((paid / total) * 100), 100)
  }

  const calculatedTotal = (amount, interestRate, months) => {
    const amt = parseFloat(amount) || 0
    const rate = parseFloat(interestRate) || 0
    const m = parseInt(months) || 0
    if (amt <= 0) return 0
    if (rate <= 0 || m <= 0) return amt
    return amt * Math.pow(1 + rate / 100, m)
  }

  it('getDebtPaid returns 0 when no category_id', () => {
    const debt = { id: 1, category_id: null, total_with_interest: '1000' }
    expect(getDebtPaid(debt, [])).toBe(0)
  })

  it('getDebtPaid sums expense transactions for matching category', () => {
    const debt = { id: 1, category_id: 3, total_with_interest: '5000' }
    const transactions = [
      { category_id: 3, type: 'expense', amount: '200' },
      { category_id: 3, type: 'expense', amount: '300' },
      { category_id: 3, type: 'income', amount: '100' },
    ]
    expect(getDebtPaid(debt, transactions)).toBe(500)
  })

  it('getDebtPaid returns 0 when no matching expenses', () => {
    const debt = { id: 1, category_id: 3, total_with_interest: '5000' }
    const transactions = [{ category_id: 3, type: 'income', amount: '200' }]
    expect(getDebtPaid(debt, transactions)).toBe(0)
  })

  it('getDebtProgress calculates correct percentage', () => {
    const debt = { id: 1, category_id: 3, total_with_interest: '4000' }
    const transactions = [{ category_id: 3, type: 'expense', amount: '1000' }]
    expect(getDebtProgress(debt, transactions)).toBe(25)
  })

  it('getDebtProgress returns 0 for zero total', () => {
    const debt = { id: 1, category_id: 3, total_with_interest: '0' }
    expect(getDebtProgress(debt, [])).toBe(0)
  })

  it('getDebtProgress caps at 100', () => {
    const debt = { id: 1, category_id: 3, total_with_interest: '1000' }
    const transactions = [{ category_id: 3, type: 'expense', amount: '2000' }]
    expect(getDebtProgress(debt, transactions)).toBe(100)
  })

  it('calculatedTotal returns amount when no interest', () => {
    expect(calculatedTotal('1000', '0', '12')).toBe(1000)
  })

  it('calculatedTotal returns 0 when amount is 0', () => {
    expect(calculatedTotal('0', '10', '12')).toBe(0)
  })

  it('calculatedTotal returns amount when no months', () => {
    expect(calculatedTotal('1000', '10', '0')).toBe(1000)
  })

  it('calculatedTotal computes compound interest correctly', () => {
    const result = calculatedTotal('1000', '10', '12')
    const expected = 1000 * Math.pow(1 + 0.10, 12)
    expect(result).toBeCloseTo(expected, 1)
  })

  it('calculatedTotal handles varying rates', () => {
    const result = calculatedTotal('5000', '5', '24')
    const expected = 5000 * Math.pow(1 + 0.05, 24)
    expect(result).toBeCloseTo(expected, 1)
  })
})
