<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <div>
        <h1>Main Dashboard</h1>
        <p class="dashboard-subtitle">
          Summary of income, expenses, budgets, goals and debts.
        </p>
      </div>

      <div class="header-actions">
        <select v-model="period" class="period-select" aria-label="Dashboard period">
          <option value="7">Last 7 days</option>
          <option value="30">Last 30 days</option>
          <option value="90">Last 90 days</option>
          <option value="qtd">Quarter to date</option>
          <option value="all">All time</option>
        </select>
        <button type="button" class="refresh-btn" :disabled="loading" @click="loadDashboard">
          {{ loading ? 'Loading...' : 'Refresh' }}
        </button>
      </div>
    </header>

    <main class="dashboard-content">
      <div v-if="error" class="alert-card">
        {{ error }}
      </div>

      <section class="summary-grid" aria-label="Financial summary">
        <article class="summary-card balance-card">
          <span class="card-label">Net balance</span>
          <strong :class="{ negative: netBalance < 0 }">{{ formatMoney(netBalance) }}</strong>
          <small>Income minus expenses in selected period</small>
        </article>

        <article class="summary-card">
          <span class="card-label">Income</span>
          <strong class="positive">{{ formatMoney(totalIncome) }}</strong>
          <small>{{ incomeTransactions }} income transactions</small>
        </article>

        <article class="summary-card">
          <span class="card-label">Expenses</span>
          <strong class="negative">{{ formatMoney(totalExpenses) }}</strong>
          <small>{{ expenseTransactions }} expense transactions</small>
        </article>

        <article class="summary-card">
          <span class="card-label">Savings rate</span>
          <strong>{{ savingsRate }}%</strong>
          <small>{{ periodLabel }}</small>
        </article>
      </section>

      <section class="dashboard-grid">
        <article class="panel wide-panel">
          <div class="panel-heading">
            <div>
              <h2>Cash flow</h2>
              <p>Income and expenses during the last months.</p>
            </div>
          </div>

          <div v-if="monthlyTrend.length" class="bar-chart">
            <div
              v-for="month in monthlyTrend"
              :key="month.key"
              class="chart-month"
            >
              <div class="bars">
                <span
                  class="bar income-bar"
                  :style="{ height: getBarHeight(month.income) }"
                  :title="`Income: ${formatMoney(month.income)}`"
                ></span>
                <span
                  class="bar expense-bar"
                  :style="{ height: getBarHeight(month.expenses) }"
                  :title="`Expenses: ${formatMoney(month.expenses)}`"
                ></span>
              </div>
              <span class="month-label">{{ month.label }}</span>
            </div>
          </div>

          <div v-else class="empty-state compact">
            No transactions to chart yet.
          </div>

          <div class="chart-legend">
            <span><i class="legend-dot income-dot"></i> Income</span>
            <span><i class="legend-dot expense-dot"></i> Expenses</span>
          </div>
        </article>

        <article class="panel">
          <div class="panel-heading">
            <div>
              <h2>Expenses by category</h2>
              <p>Top categories in this period.</p>
            </div>
          </div>

          <div v-if="categoryBreakdown.length" class="donut-layout">
            <div class="donut-chart" :style="donutStyle">
              <span>{{ totalExpenseCategories }}</span>
            </div>
            <div class="category-list">
              <div
                v-for="item in categoryBreakdown"
                :key="item.category"
                class="category-item"
              >
                <span class="category-color" :style="{ background: item.color }"></span>
                <div>
                  <strong>{{ item.category }}</strong>
                  <small>{{ item.percentage }}% &middot; {{ formatMoney(item.amount) }}</small>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="empty-state compact">
            No expense categories yet.
          </div>
        </article>

        <article class="panel">
          <div class="panel-heading">
            <div>
              <h2>Budget health</h2>
              <p>Limits closest to their alert threshold.</p>
            </div>
          </div>

          <div v-if="budgetHealth.length" class="progress-list">
            <div v-for="budget in budgetHealth" :key="budget.id" class="progress-row">
              <div class="progress-meta">
                <strong>{{ budget.name }}</strong>
                <span>{{ budget.percentage }}%</span>
              </div>
              <div class="progress-bar">
                <span
                  class="progress-fill"
                  :class="{ warning: budget.percentage >= budget.alert }"
                  :style="{ width: budget.percentage + '%' }"
                ></span>
              </div>
              <small>{{ formatMoney(budget.spent) }} of {{ formatMoney(budget.limit) }}</small>
            </div>
          </div>

          <div v-else class="empty-state compact">
            No budgets available.
          </div>
        </article>

        <article class="panel">
          <div class="panel-heading">
            <div>
              <h2>Goals progress</h2>
              <p>Active goals ordered by progress.</p>
            </div>
          </div>

          <div v-if="goalProgress.length" class="progress-list">
            <div v-for="goal in goalProgress" :key="goal.id" class="progress-row">
              <div class="progress-meta">
                <strong>{{ goal.name }}</strong>
                <span>{{ goal.percentage }}%</span>
              </div>
              <div class="progress-bar">
                <span class="progress-fill success" :style="{ width: goal.percentage + '%' }"></span>
              </div>
              <small>{{ formatMoney(goal.saved) }} of {{ formatMoney(goal.target) }}</small>
            </div>
          </div>

          <div v-else class="empty-state compact">
            No active goals yet.
          </div>
        </article>

        <article class="panel">
          <div class="panel-heading">
            <div>
              <h2>Debt snapshot</h2>
              <p>Outstanding balance estimate.</p>
            </div>
          </div>

          <div class="debt-summary">
            <div>
              <span>Total debt</span>
              <strong>{{ formatMoney(totalDebt) }}</strong>
            </div>
            <div>
              <span>Paid</span>
              <strong>{{ formatMoney(totalDebtPaid) }}</strong>
            </div>
            <div>
              <span>Remaining</span>
              <strong :class="{ negative: remainingDebt > 0 }">{{ formatMoney(remainingDebt) }}</strong>
            </div>
          </div>
        </article>

        <article class="panel wide-panel">
          <div class="panel-heading">
            <div>
              <h2>Recent transactions</h2>
              <p>Latest movements for the selected period.</p>
            </div>
          </div>

          <div v-if="recentTransactions.length" class="transaction-list">
            <div
              v-for="transaction in recentTransactions"
              :key="transaction.id"
              class="transaction-row"
            >
              <div>
                <strong>{{ transaction.description || 'Transaction' }}</strong>
                <small>
                  {{ transaction.category_name || 'Uncategorized' }} &middot;
                  {{ formatDate(transaction.transaction_date) }}
                </small>
              </div>
              <span :class="transaction.type === 'income' ? 'positive' : 'negative'">
                {{ transaction.type === 'income' ? '+' : '-' }}{{ formatMoney(transaction.amount) }}
              </span>
            </div>
          </div>

          <div v-else class="empty-state compact">
            No recent transactions found.
          </div>
        </article>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, onActivated, onMounted, onUnmounted, ref } from 'vue';
import axios from 'axios';
import { readAppSettings } from '../lib/appSettings';

const API_BASE = 'http://localhost:8000/api';
const chartColors = ['#1a7f3a', '#2ca84f', '#8bd46d', '#f7c948', '#f97316', '#ef5350'];

const settings = readAppSettings();
const period = ref(settings.dashboardDefaultPeriod || '30');
const loading = ref(false);
const error = ref('');

const transactions = ref([]);
const budgets = ref([]);
const goals = ref([]);
const debts = ref([]);

function getToken() {
  return localStorage.getItem('token');
}

async function loadDashboard() {
  const token = getToken();
  if (!token) {
    error.value = 'Session token not found. Please log in again.';
    return;
  }

  loading.value = true;
  error.value = '';

  const headers = { Authorization: `Bearer ${token}` };
  const requests = await Promise.allSettled([
    axios.get(`${API_BASE}/transactions`, { headers }),
    axios.get(`${API_BASE}/budgets`, { headers }),
    axios.get(`${API_BASE}/goals/`, { headers }),
    axios.get(`${API_BASE}/debts/`, { headers }),
  ]);

  const [transactionsRes, budgetsRes, goalsRes, debtsRes] = requests;
  if (transactionsRes.status === 'fulfilled') transactions.value = transactionsRes.value.data || [];
  if (budgetsRes.status === 'fulfilled') budgets.value = budgetsRes.value.data || [];
  if (goalsRes.status === 'fulfilled') goals.value = goalsRes.value.data || [];
  if (debtsRes.status === 'fulfilled') debts.value = debtsRes.value.data || [];

  if (requests.some((request) => request.status === 'rejected')) {
    error.value = 'Some dashboard data could not be loaded.';
  }

  loading.value = false;
}

function getPeriodStartDate() {
  if (period.value === 'all') return null;

  const today = new Date();
  if (period.value === 'qtd') {
    const quarterStartMonth = Math.floor(today.getMonth() / 3) * 3;
    return new Date(today.getFullYear(), quarterStartMonth, 1);
  }

  const days = Number(period.value) || 30;
  return new Date(today.getFullYear(), today.getMonth(), today.getDate() - days + 1);
}

const periodTransactions = computed(() => {
  const startDate = getPeriodStartDate();
  if (!startDate) return [...transactions.value];

  return transactions.value.filter((transaction) => {
    if (!transaction.transaction_date) return false;
    return new Date(transaction.transaction_date) >= startDate;
  });
});

const periodLabel = computed(() => {
  if (period.value === 'all') return 'All time';
  if (period.value === 'qtd') return 'Quarter to date';
  return `Last ${period.value} days`;
});

const totalIncome = computed(() => sumTransactions('income'));
const totalExpenses = computed(() => sumTransactions('expense'));
const netBalance = computed(() => totalIncome.value - totalExpenses.value);

const incomeTransactions = computed(
  () => periodTransactions.value.filter((transaction) => transaction.type === 'income').length,
);
const expenseTransactions = computed(
  () => periodTransactions.value.filter((transaction) => transaction.type === 'expense').length,
);

const savingsRate = computed(() => {
  if (totalIncome.value <= 0) return 0;
  return Math.round((netBalance.value / totalIncome.value) * 100);
});

const monthlyTrend = computed(() => {
  const months = [];
  const now = new Date();

  for (let index = 5; index >= 0; index -= 1) {
    const date = new Date(now.getFullYear(), now.getMonth() - index, 1);
    const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
    months.push({
      key,
      label: date.toLocaleDateString('en-US', { month: 'short' }),
      income: 0,
      expenses: 0,
    });
  }

  transactions.value.forEach((transaction) => {
    if (!transaction.transaction_date) return;
    const date = new Date(transaction.transaction_date);
    const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
    const month = months.find((item) => item.key === key);
    if (!month) return;

    if (transaction.type === 'income') month.income += toAmount(transaction.amount);
    if (transaction.type === 'expense') month.expenses += toAmount(transaction.amount);
  });

  return months.filter((month) => month.income > 0 || month.expenses > 0);
});

const maxMonthlyAmount = computed(() => {
  const amounts = monthlyTrend.value.flatMap((month) => [month.income, month.expenses]);
  return Math.max(...amounts, 1);
});

const categoryBreakdown = computed(() => {
  const categoryTotals = new Map();

  periodTransactions.value
    .filter((transaction) => transaction.type === 'expense')
    .forEach((transaction) => {
      const category = transaction.category_name || 'Uncategorized';
      categoryTotals.set(category, (categoryTotals.get(category) || 0) + toAmount(transaction.amount));
    });

  return [...categoryTotals.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 6)
    .map(([category, amount], index) => ({
      category,
      amount,
      color: chartColors[index % chartColors.length],
      percentage: totalExpenses.value ? Math.round((amount / totalExpenses.value) * 100) : 0,
    }));
});

const totalExpenseCategories = computed(() => categoryBreakdown.value.length);

const donutStyle = computed(() => {
  if (!categoryBreakdown.value.length || totalExpenses.value <= 0) {
    return { background: '#eef7ef' };
  }

  let cursor = 0;
  const segments = categoryBreakdown.value.map((item) => {
    const start = cursor;
    const end = cursor + (item.amount / totalExpenses.value) * 100;
    cursor = end;
    return `${item.color} ${start}% ${end}%`;
  });

  return { background: `conic-gradient(${segments.join(', ')})` };
});

const budgetHealth = computed(() => {
  return budgets.value
    .map((budget) => {
      const spent = getBudgetSpent(budget);
      const limit = toAmount(budget.amount);
      const percentage = limit ? Math.min(Math.round((spent / limit) * 100), 100) : 0;
      return {
        id: budget.id,
        name: budget.name,
        spent,
        limit,
        percentage,
        alert: Number(budget.alert_percentage) || 80,
      };
    })
    .sort((a, b) => b.percentage - a.percentage)
    .slice(0, 4);
});

const goalProgress = computed(() => {
  return goals.value
    .filter((goal) => String(goal.status || '').toLowerCase() !== 'completed')
    .map((goal) => {
      const target = toAmount(goal.target_amount);
      const saved = getGoalSaved(goal);
      const percentage = target ? Math.min(Math.round((saved / target) * 100), 100) : 0;
      return { id: goal.id, name: goal.name, saved, target, percentage };
    })
    .sort((a, b) => b.percentage - a.percentage)
    .slice(0, 4);
});

const totalDebt = computed(() => debts.value.reduce((sum, debt) => sum + toAmount(debt.total_with_interest), 0));
const totalDebtPaid = computed(() => debts.value.reduce((sum, debt) => sum + getDebtPaid(debt), 0));
const remainingDebt = computed(() => Math.max(totalDebt.value - totalDebtPaid.value, 0));

const recentTransactions = computed(() => {
  return [...periodTransactions.value]
    .sort((a, b) => new Date(b.transaction_date) - new Date(a.transaction_date))
    .slice(0, 6);
});

function sumTransactions(type) {
  return periodTransactions.value
    .filter((transaction) => transaction.type === type)
    .reduce((sum, transaction) => sum + toAmount(transaction.amount), 0);
}

function getBudgetSpent(budget) {
  return transactions.value
    .filter((transaction) => {
      if (transaction.type !== 'expense') return false;
      if (budget.category_id && transaction.category_id !== budget.category_id) return false;
      if (!transaction.transaction_date || !budget.start_date) return true;

      const transactionDate = new Date(transaction.transaction_date);
      const startDate = new Date(budget.start_date);
      const endDate = budget.end_date ? new Date(budget.end_date) : new Date();
      return transactionDate >= startDate && transactionDate <= endDate;
    })
    .reduce((sum, transaction) => sum + toAmount(transaction.amount), 0);
}

function getGoalSaved(goal) {
  if (!goal.category_id) return 0;

  return transactions.value
    .filter(
      (transaction) =>
        transaction.type === 'income' && transaction.category_id === goal.category_id,
    )
    .reduce((sum, transaction) => sum + toAmount(transaction.amount), 0);
}

function getDebtPaid(debt) {
  if (!debt.category_id) return 0;

  return transactions.value
    .filter(
      (transaction) =>
        transaction.type === 'expense' && transaction.category_id === debt.category_id,
    )
    .reduce((sum, transaction) => sum + toAmount(transaction.amount), 0);
}

function getBarHeight(amount) {
  const height = (amount / maxMonthlyAmount.value) * 170;
  return `${Math.max(height, amount > 0 ? 12 : 0)}px`;
}

function toAmount(value) {
  return Number.parseFloat(value) || 0;
}

function formatMoney(value) {
  return new Intl.NumberFormat(settings.locale || 'en-US', {
    style: 'currency',
    currency: settings.currencyCode || 'USD',
    maximumFractionDigits: 2,
  }).format(toAmount(value));
}

function formatDate(date) {
  if (!date) return 'No date';
  return new Date(date).toLocaleDateString(settings.locale || 'en-US', {
    month: 'short',
    day: '2-digit',
  });
}

function handleTransactionUpdated() {
  loadDashboard();
}

onMounted(() => {
  loadDashboard();
  window.addEventListener('transactionUpdated', handleTransactionUpdated);
});

onActivated(() => {
  loadDashboard();
});

onUnmounted(() => {
  window.removeEventListener('transactionUpdated', handleTransactionUpdated);
});
</script>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.dashboard-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  color: #1f2933;
}

.dashboard-header {
  align-items: center;
  background: linear-gradient(135deg, #f8fdf8 0%, #eef9ef 100%);
  border: 1px solid #e0e8e0;
  border-radius: 18px;
  box-shadow: 0 10px 30px rgba(26, 127, 58, 0.08);
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 24px 28px;
  width: 100%;
}

.eyebrow {
  color: #1a7f3a;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.12em;
  margin-bottom: 6px;
  text-transform: uppercase;
}

.dashboard-header h1 {
  color: #14532d;
  font-size: 30px;
  font-weight: 800;
}

.dashboard-subtitle {
  color: #667085;
  font-size: 14px;
  margin-top: 6px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.period-select,
.refresh-btn {
  border: 1px solid #d9eadc;
  border-radius: 12px;
  font: inherit;
  min-height: 42px;
  padding: 0 14px;
}

.period-select {
  background: #ffffff;
  color: #344054;
}

.refresh-btn {
  background: #1a7f3a;
  color: #ffffff;
  cursor: pointer;
  font-weight: 700;
}

.refresh-btn:disabled {
  cursor: not-allowed;
  opacity: 0.65;
}

.dashboard-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px 0 0;
}

.alert-card {
  background: #fff7ed;
  border: 1px solid #fed7aa;
  border-radius: 14px;
  color: #9a3412;
  margin-bottom: 18px;
  padding: 14px 16px;
}

.summary-grid,
.dashboard-grid {
  display: grid;
  gap: 18px;
}

.summary-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
  margin-bottom: 18px;
}

.summary-card,
.panel {
  background: #ffffff;
  border: 1px solid #e6efe7;
  border-radius: 18px;
  box-shadow: 0 12px 28px rgba(15, 23, 42, 0.06);
}

.summary-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-height: 150px;
  padding: 22px;
}

.balance-card {
  background: linear-gradient(135deg, #1a7f3a 0%, #2ca84f 100%);
  border: none;
  color: #ffffff;
}

.balance-card .card-label,
.balance-card small,
.balance-card strong {
  color: #ffffff;
}

.card-label {
  color: #667085;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
}

.summary-card strong {
  color: #111827;
  font-size: 28px;
  line-height: 1.1;
}

.summary-card small,
.panel-heading p,
.progress-row small,
.transaction-row small,
.category-item small {
  color: #667085;
  font-size: 13px;
}

.dashboard-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.panel {
  min-height: 310px;
  padding: 22px;
}

.wide-panel {
  grid-column: span 2;
}

.panel-heading {
  align-items: flex-start;
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.panel-heading h2 {
  color: #14532d;
  font-size: 20px;
  margin-bottom: 4px;
}

.bar-chart {
  align-items: end;
  display: grid;
  gap: 14px;
  grid-template-columns: repeat(6, minmax(46px, 1fr));
  min-height: 215px;
}

.chart-month {
  align-items: center;
  display: flex;
  flex-direction: column;
  gap: 10px;
  justify-content: end;
}

.bars {
  align-items: end;
  display: flex;
  gap: 7px;
  height: 180px;
}

.bar {
  border-radius: 10px 10px 3px 3px;
  display: block;
  min-width: 17px;
  transition: height 0.2s ease;
}

.income-bar {
  background: linear-gradient(180deg, #39c75f, #1a7f3a);
}

.expense-bar {
  background: linear-gradient(180deg, #f97316, #ef5350);
}

.month-label {
  color: #667085;
  font-size: 12px;
  font-weight: 700;
}

.chart-legend {
  display: flex;
  gap: 16px;
  margin-top: 18px;
}

.chart-legend span {
  align-items: center;
  color: #475467;
  display: flex;
  font-size: 13px;
  gap: 7px;
}

.legend-dot,
.category-color {
  border-radius: 999px;
  display: inline-block;
  height: 10px;
  width: 10px;
}

.income-dot {
  background: #1a7f3a;
}

.expense-dot {
  background: #ef5350;
}

.donut-layout {
  align-items: center;
  display: grid;
  gap: 22px;
  grid-template-columns: 150px 1fr;
}

.donut-chart {
  align-items: center;
  border-radius: 999px;
  display: flex;
  height: 150px;
  justify-content: center;
  position: relative;
  width: 150px;
}

.donut-chart::after {
  background: #ffffff;
  border-radius: 999px;
  content: '';
  height: 92px;
  position: absolute;
  width: 92px;
}

.donut-chart span {
  color: #14532d;
  font-size: 30px;
  font-weight: 800;
  position: relative;
  z-index: 1;
}

.category-list,
.progress-list,
.transaction-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.category-item {
  align-items: center;
  display: flex;
  gap: 10px;
}

.category-item strong,
.progress-meta strong,
.transaction-row strong {
  color: #1f2933;
  font-size: 14px;
}

.category-item div,
.transaction-row div {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.progress-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.progress-meta,
.transaction-row,
.debt-summary div {
  align-items: center;
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.progress-meta span {
  color: #1a7f3a;
  font-size: 13px;
  font-weight: 800;
}

.progress-bar {
  background: #eef7ef;
  border-radius: 999px;
  height: 10px;
  overflow: hidden;
}

.progress-fill {
  background: #1a7f3a;
  border-radius: inherit;
  display: block;
  height: 100%;
}

.progress-fill.warning {
  background: #f97316;
}

.progress-fill.success {
  background: linear-gradient(90deg, #2ca84f, #8bd46d);
}

.debt-summary {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.debt-summary div {
  background: #f8fdf8;
  border: 1px solid #e0e8e0;
  border-radius: 14px;
  padding: 16px;
}

.debt-summary span {
  color: #667085;
  font-size: 13px;
  font-weight: 700;
}

.debt-summary strong {
  color: #111827;
  font-size: 18px;
}

.transaction-row {
  border-bottom: 1px solid #edf2ee;
  padding-bottom: 12px;
}

.transaction-row:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.transaction-row > span {
  font-weight: 800;
  white-space: nowrap;
}

.positive {
  color: #1a7f3a !important;
}

.negative {
  color: #ef5350 !important;
}

.empty-state {
  align-items: center;
  background: #f8fdf8;
  border: 1px dashed #c7ddcc;
  border-radius: 14px;
  color: #667085;
  display: flex;
  justify-content: center;
  min-height: 160px;
  padding: 20px;
  text-align: center;
}

.empty-state.compact {
  min-height: 180px;
}

@media (max-width: 1200px) {
  .summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .dashboard-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 860px) {
  .dashboard-header,
  .header-actions {
    align-items: stretch;
    flex-direction: column;
  }

  .summary-grid,
  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .wide-panel {
    grid-column: span 1;
  }

  .donut-layout {
    grid-template-columns: 1fr;
    justify-items: center;
  }

  .category-list {
    width: 100%;
  }
}

@media (max-width: 560px) {
  .dashboard-header,
  .summary-card,
  .panel {
    border-radius: 14px;
    padding: 18px;
  }

  .dashboard-header h1 {
    font-size: 24px;
  }

  .summary-card strong {
    font-size: 24px;
  }

  .bar-chart {
    gap: 8px;
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
