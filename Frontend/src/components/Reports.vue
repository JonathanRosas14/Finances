<template>
  <div class="reports-container">
    <header class="reports-header">
      <h1>Reports</h1>
      <div class="header-actions">
        <button @click="exportToPDF" class="export-btn export-pdf" :disabled="loading">
          📄 Export to PDF
        </button>
        <button @click="exportToExcel" class="export-btn export-excel" :disabled="loading">
          📊 Export to Excel
        </button>
      </div>
    </header>
    <div class="reports-content">
      <!-- Filters -->
      <div class="filters-section">
        <div class="filter-group">
          <label for="date-from">From Date</label>
          <input
            type="date"
            id="date-from"
            v-model="filters.dateFrom"
            class="filter-input"
          />
        </div>
        <div class="filter-group">
          <label for="date-to">To Date</label>
          <input
            type="date"
            id="date-to"
            v-model="filters.dateTo"
            class="filter-input"
          />
        </div>
        <div class="filter-group">
          <label for="category">Category</label>
          <select v-model="filters.category" id="category" class="filter-input">
            <option value="">All Categories</option>
            <option
              v-for="category in categories"
              :key="category.id"
              :value="category.name"
            >
              {{ category.name }}
            </option>
          </select>
        </div>
        <button @click="applyFilters" class="apply-filters-btn">Apply Filters</button>
      </div>

      <!-- Summary Cards -->
      <div class="summary-cards">
        <div class="card income-card">
          <h3>Total Income</h3>
          <p class="amount">${{ totalIncome.toFixed(2) }}</p>
          <span class="label">Over selected period</span>
        </div>
        <div class="card expense-card">
          <h3>Total Expenses</h3>
          <p class="amount">${{ totalExpenses.toFixed(2) }}</p>
          <span class="label">Over selected period</span>
        </div>
        <div class="card balance-card">
          <h3>Net Balance</h3>
          <p class="amount" :class="{ negative: (totalIncome - totalExpenses) < 0 }">
            ${{ (totalIncome - totalExpenses).toFixed(2) }}
          </p>
          <span class="label">Income - Expenses</span>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="charts-section">
        <div class="chart-container">
          <h2>Expense by Category</h2>
          <div class="chart-content">
            <div class="pie-chart-mock">
              <div
                v-for="(item, index) in expenseByCategory"
                :key="index"
                class="category-bar"
              >
                <div class="category-info">
                  <span class="category-name">{{ item.category }}</span>
                  <span class="category-percentage">{{ item.percentage }}%</span>
                </div>
                <div class="progress-bar">
                  <div
                    class="progress-fill"
                    :style="{
                      width: item.percentage + '%',
                      backgroundColor: getCategoryColor(index),
                    }"
                  ></div>
                </div>
                <span class="category-amount">${{ item.amount.toFixed(2) }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="chart-container">
          <h2>Monthly Trend</h2>
          <div class="chart-content">
            <div class="trend-chart">
              <div
                v-for="month in monthlyTrend"
                :key="month.month"
                class="trend-item"
              >
                <div class="bars-container">
                  <div
                    class="bar income-bar"
                    :style="{ height: (month.income / maxMonthlyAmount) * 200 + 'px' }"
                  ></div>
                  <div
                    class="bar expense-bar"
                    :style="{ height: (month.expenses / maxMonthlyAmount) * 200 + 'px' }"
                  ></div>
                </div>
                <span class="month-label">{{ formatMonthLabel(month.month) }}</span>
              </div>
            </div>
            <div class="legend">
              <div class="legend-item">
                <div class="legend-color income-bar"></div>
                <span>Income</span>
              </div>
              <div class="legend-item">
                <div class="legend-color expense-bar"></div>
                <span>Expenses</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Top Transaction Table -->
      <div class="table-section">
        <h2>Recent Transactions</h2>
        <div class="table-wrapper">
          <table class="transactions-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Description</th>
                <th>Category</th>
                <th>Type</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredTransactions.length === 0">
                <td colspan="5" class="empty-row">No transactions found</td>
              </tr>
              <tr
                v-for="transaction in filteredTransactions.slice(0, 10)"
                :key="transaction.id"
                :class="{ 'income-row': transaction.type === 'income', 'expense-row': transaction.type === 'expense' }"
              >
                <td>{{ formatDate(transaction.transaction_date) }}</td>
                <td>{{ transaction.description }}</td>
                <td>{{ transaction.category_name }}</td>
                <td>{{ transaction.type }}</td>
                <td class="amount-cell">
                  <span :class="{ income: transaction.type === 'income', expense: transaction.type === 'expense' }">
                    {{ transaction.type === 'income' ? '+' : '-' }}${{ formatAmount(transaction.amount) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onActivated } from 'vue';
import axios from 'axios';

const transactions = ref([]);
const categories = ref([]);
const loading = ref(false);
const filters = ref({
  dateFrom: '',
  dateTo: '',
  category: '',
});

const categoryColors = [
  '#1a7f3a',
  '#2ca84f',
  '#39c75f',
  '#4ed570',
  '#63de81',
];

onMounted(() => {
  fetchData();
  setDefaultDates();

  // Listen for transaction update events from other components
  const handleTransactionUpdated = async () => {
    console.log("🔄 Reports: transactionUpdated event received");
    await fetchData();
    console.log("✅ Reports: Data reloaded");
  };
  window.addEventListener("transactionUpdated", handleTransactionUpdated);

  // Limpiar al desmontar el componente
  return () => {
    window.removeEventListener("transactionUpdated", handleTransactionUpdated);
  };
});

// Refetch data when component becomes visible again (from another route)
onActivated(() => {
  fetchData();
});

const setDefaultDates = () => {
  const today = new Date();
  const ninetyDaysAgo = new Date(today.getTime() - 90 * 24 * 60 * 60 * 1000);
  
  filters.value.dateTo = today.toISOString().split('T')[0];
  filters.value.dateFrom = ninetyDaysAgo.toISOString().split('T')[0];
  filters.value.category = ''; // Reset category filter
  console.log('📅 Default dates set (90 days):', {
    from: filters.value.dateFrom,
    to: filters.value.dateTo,
    category: filters.value.category
  });
};

const fetchData = async () => {
  try {
    loading.value = true;
    console.log('📡 Reports: Fetching transactions from API...');
    
    const token = localStorage.getItem('token');
    console.log('🔑 Token available:', !!token);
    
    const transactionsRes = await axios.get('http://localhost:8000/api/transactions', {
      headers: { Authorization: `Bearer ${token}` },
    });
    console.log('✅ Transactions received:', transactionsRes.data);
    transactions.value = transactionsRes.data || [];

    const categoriesRes = await axios.get('http://localhost:8000/api/categories', {
      headers: { Authorization: `Bearer ${token}` },
    });
    console.log('✅ Categories received:', categoriesRes.data);
    categories.value = categoriesRes.data || [];
    loading.value = false;
  } catch (error) {
    console.error('❌ Error fetching data:', error);
    console.error('Error response:', error.response?.data);
    console.error('Error status:', error.response?.status);
    loading.value = false;
    window.showNotification('Error loading data: ' + (error.response?.data?.message || error.message), 'error');
  }
};

const applyFilters = () => {
  // Refetch data when filters are applied
  fetchData();
};

const filteredTransactions = computed(() => {
  const result = transactions.value.filter(trans => {
    const transDate = new Date(trans.transaction_date).toISOString().split('T')[0];
    const fromDate = filters.value.dateFrom;
    const toDate = filters.value.dateTo;
    const categoryMatch = !filters.value.category || trans.category_name === filters.value.category;
    const dateMatch = transDate >= fromDate && transDate <= toDate;
    return categoryMatch && dateMatch;
  });
  
  console.log('📊 Filtered Transactions:', {
    total: transactions.value.length,
    filtered: result.length,
    dateFrom: filters.value.dateFrom,
    dateTo: filters.value.dateTo,
    category: filters.value.category,
    transactions: result.map(t => ({ date: t.transaction_date, amount: t.amount, type: t.type }))
  });
  
  return result;
});

const totalIncome = computed(() => {
  return filteredTransactions.value
    .filter(t => t.type === 'income')
    .reduce((sum, t) => sum + (parseFloat(t.amount) || 0), 0);
});

const totalExpenses = computed(() => {
  return filteredTransactions.value
    .filter(t => t.type === 'expense')
    .reduce((sum, t) => sum + (parseFloat(t.amount) || 0), 0);
});

const expenseByCategory = computed(() => {
  const categoryMap = {};
  filteredTransactions.value
    .filter(t => t.type === 'expense')
    .forEach(t => {
      const cat = t.category_name || 'Uncategorized';
      categoryMap[cat] = (categoryMap[cat] || 0) + (parseFloat(t.amount) || 0);
    });

  const total = totalExpenses.value;
  return Object.entries(categoryMap).map(([category, amount]) => ({
    category,
    amount,
    percentage: total > 0 ? Math.round((amount / total) * 100) : 0,
  }));
});

const monthlyTrend = computed(() => {
  const monthMap = {};
  filteredTransactions.value.forEach(t => {
    const date = new Date(t.transaction_date);
    const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
    
    if (!monthMap[monthKey]) {
      monthMap[monthKey] = { income: 0, expenses: 0, month: monthKey };
    }
    
    const amount = parseFloat(t.amount) || 0;
    if (t.type === 'income') {
      monthMap[monthKey].income += amount;
    } else {
      monthMap[monthKey].expenses += amount;
    }
  });

  return Object.values(monthMap).sort((a, b) => a.month.localeCompare(b.month));
});

const maxMonthlyAmount = computed(() => {
  let max = 0;
  monthlyTrend.value.forEach(month => {
    max = Math.max(max, month.income, month.expenses);
  });
  return max || 1;
});

const getCategoryColor = (index) => {
  return categoryColors[index % categoryColors.length];
};

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

const formatMonthLabel = (monthStr) => {
  const [year, month] = monthStr.split('-');
  const date = new Date(year, parseInt(month) - 1);
  return date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
};

const formatAmount = (amount) => {
  return (parseFloat(amount) || 0).toFixed(2);
};

const exportToPDF = async () => {
  try {
    const { jsPDF } = await import('jspdf');
    
    const pdf = new jsPDF('p', 'mm', 'a4');
    let yPosition = 20;
    const pageHeight = pdf.internal.pageSize.getHeight();
    const pageWidth = pdf.internal.pageSize.getWidth();
    const margin = 15;
    
    // Title
    pdf.setFontSize(20);
    pdf.setTextColor(26, 127, 58);
    pdf.text('Financial Report', margin, yPosition);
    yPosition += 15;
    
    // Date range
    pdf.setFontSize(10);
    pdf.setTextColor(100, 100, 100);
    pdf.text(`Report Period: ${filters.value.dateFrom} to ${filters.value.dateTo}`, margin, yPosition);
    yPosition += 10;
    
    // Summary
    pdf.setFontSize(12);
    pdf.setTextColor(26, 127, 58);
    pdf.text('Summary', margin, yPosition);
    yPosition += 8;
    
    pdf.setFontSize(10);
    pdf.setTextColor(0, 0, 0);
    pdf.text(`Total Income: $${totalIncome.value.toFixed(2)}`, margin + 5, yPosition);
    yPosition += 6;
    pdf.text(`Total Expenses: $${totalExpenses.value.toFixed(2)}`, margin + 5, yPosition);
    yPosition += 6;
    pdf.text(`Net Balance: $${(totalIncome.value - totalExpenses.value).toFixed(2)}`, margin + 5, yPosition);
    yPosition += 12;
    
    // Transactions table
    if (filteredTransactions.value.length > 0) {
      pdf.setFontSize(12);
      pdf.setTextColor(26, 127, 58);
      pdf.text('Transactions', margin, yPosition);
      yPosition += 10;
      
      pdf.setFontSize(9);
      pdf.setTextColor(0, 0, 0);
      
      // Table headers
      const headers = ['Date', 'Description', 'Category', 'Type', 'Amount'];
      const colWidths = [30, 50, 35, 25, 30];
      let xPosition = margin;
      
      pdf.setDrawColor(26, 127, 58);
      pdf.setFillColor(232, 245, 233);
      pdf.rect(margin, yPosition - 6, pageWidth - (2 * margin), 8, 'F');
      
      headers.forEach((header, index) => {
        pdf.text(header, xPosition, yPosition);
        xPosition += colWidths[index];
      });
      yPosition += 10;
      
      // Table rows
      filteredTransactions.value.forEach(trans => {
        if (yPosition > pageHeight - 20) {
          pdf.addPage();
          yPosition = 20;
        }
        
        xPosition = margin;
        pdf.text(formatDate(trans.transaction_date), xPosition, yPosition);
        xPosition += colWidths[0];
        
        const desc = trans.description.substring(0, 15);
        pdf.text(desc, xPosition, yPosition);
        xPosition += colWidths[1];
        
        pdf.text(trans.category_name, xPosition, yPosition);
        xPosition += colWidths[2];
        
        pdf.text(trans.type, xPosition, yPosition);
        xPosition += colWidths[3];
        
        pdf.text(`$${formatAmount(trans.amount)}`, xPosition, yPosition);
        yPosition += 8;
      });
    }
    
    pdf.save(`Financial_Report_${new Date().toISOString().split('T')[0]}.pdf`);
    alert('PDF exported successfully');
  } catch (error) {
    console.error('Error exporting to PDF:', error);
    alert('Error generating PDF: ' + error.message);
  }
};

const exportToExcel = async () => {
  try {
    const XLSX = await import('xlsx');
    
    const ws = XLSX.utils.json_to_sheet(
      filteredTransactions.value.map(t => ({
        Date: formatDate(t.transaction_date),
        Description: t.description,
        Category: t.category_name,
        Type: t.type,
        Amount: (parseFloat(t.amount) || 0).toFixed(2),
      }))
    );
    
    const wsSummary = XLSX.utils.sheet_add_aoa(
      XLSX.utils.book_new(),
      [
        ['Financial Report Summary'],
        [],
        ['Metric', 'Value'],
        ['Total Income', totalIncome.value.toFixed(2)],
        ['Total Expenses', totalExpenses.value.toFixed(2)],
        ['Net Balance', (totalIncome.value - totalExpenses.value).toFixed(2)],
        [],
        ['Expenses by Category'],
        ['Category', 'Amount', 'Percentage'],
        ...expenseByCategory.value.map(e => [e.category, e.amount.toFixed(2), `${e.percentage}%`]),
      ]
    );
    
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, wsSummary, 'Summary');
    XLSX.utils.book_append_sheet(wb, ws, 'Transactions');
    
    XLSX.writeFile(wb, `Financial_Report_${new Date().toISOString().split('T')[0]}.xlsx`);
    alert('Excel file exported successfully');
  } catch (error) {
    console.error('Error exporting to Excel:', error);
    alert('Error generating Excel file: ' + error.message);
  }
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.reports-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  font-family: manrope, sans-serif;
}

.reports-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #f8fdf8;
  color: #1a7f3a;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  padding: 20px 30px;
  border-bottom: 1px solid #e0e8e0;
  width: 100%;
}

.reports-header h1 {
  font-size: 28px;
  font-weight: 600;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.export-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  font-size: 14px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.export-pdf {
  background-color: #1a7f3a;
  color: white;
}

.export-pdf:hover {
  background-color: #156830;
  box-shadow: 0 4px 8px rgba(26, 127, 58, 0.2);
  transform: translateY(-2px);
}

.export-excel {
  background-color: #e8f5e9;
  color: #1a7f3a;
  border: 1px solid #1a7f3a;
}

.export-excel:hover {
  background-color: #d4edda;
  box-shadow: 0 4px 8px rgba(26, 127, 58, 0.15);
  transform: translateY(-2px);
}

.reports-content {
  flex: 1;
  overflow-y: auto;
  padding: 30px;
  background-color: #ffffff;
}

.filters-section {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f8fdf8;
  border-radius: 8px;
  border: 1px solid #e0e8e0;
  flex-wrap: wrap;
  align-items: flex-end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  font-size: 14px;
  font-weight: 500;
  color: #1a7f3a;
}

.filter-input {
  padding: 10px 12px;
  border: 1px solid #e0e8e0;
  border-radius: 6px;
  font-size: 14px;
  min-width: 180px;
  background-color: white;
  color: #333;
}

.filter-input:focus {
  outline: none;
  border-color: #1a7f3a;
  box-shadow: 0 0 0 3px rgba(26, 127, 58, 0.1);
}

.apply-filters-btn {
  padding: 10px 20px;
  background-color: #1a7f3a;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.apply-filters-btn:hover {
  background-color: #156830;
  box-shadow: 0 4px 8px rgba(26, 127, 58, 0.2);
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.card {
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e0e8e0;
  background-color: #f8fdf8;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.card h3 {
  font-size: 14px;
  font-weight: 500;
  color: #666;
}

.card .amount {
  font-size: 28px;
  font-weight: 700;
  color: #1a7f3a;
}

.card .amount.negative {
  color: #d32f2f;
}

.card .label {
  font-size: 12px;
  color: #999;
}
.charts-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.chart-container {
  background-color: #f8fdf8;
  border: 1px solid #e0e8e0;
  border-radius: 8px;
  padding: 20px;
}

.chart-container h2 {
  font-size: 16px;
  font-weight: 600;
  color: #1a7f3a;
  margin-bottom: 20px;
}

.chart-content {
  min-height: 250px;
}

.pie-chart-mock {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.category-bar {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.category-info {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

.category-name {
  font-weight: 500;
  color: #333;
}

.category-percentage {
  color: #1a7f3a;
  font-weight: 600;
}

.progress-bar {
  height: 8px;
  background-color: #e0e8e0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.category-amount {
  font-size: 12px;
  color: #666;
}

.trend-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 250px;
  gap: 10px;
}

.trend-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.bars-container {
  display: flex;
  align-items: flex-end;
  gap: 5px;
  height: 200px;
}

.bar {
  width: 15px;
  border-radius: 4px 4px 0 0;
  min-height: 5px;
}

.income-bar {
  background-color: #2ca84f;
}

.expense-bar {
  background-color: #d32f2f;
}

.month-label {
  font-size: 12px;
  color: #666;
  font-weight: 500;
}

.legend {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-top: 15px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.table-section {
  background-color: #f8fdf8;
  border: 1px solid #e0e8e0;
  border-radius: 8px;
  padding: 20px;
  margin-top: 30px;
}

.table-section h2 {
  font-size: 16px;
  font-weight: 600;
  color: #1a7f3a;
  margin-bottom: 20px;
}

.table-wrapper {
  overflow-x: auto;
}

.transactions-table {
  width: 100%;
  border-collapse: collapse;
}

.transactions-table thead {
  background-color: #e8f5e9;
}

.transactions-table th {
  padding: 12px;
  text-align: left;
  font-weight: 600;
  color: #1a7f3a;
  font-size: 14px;
}

.transactions-table td {
  padding: 12px;
  border-bottom: 1px solid #e0e8e0;
  font-size: 14px;
  color: #333;
}

.transactions-table tbody tr:hover {
  background-color: #f0f7f0;
}

.empty-row {
  text-align: center;
  color: #999;
  font-style: italic;
}

.income-row {
  background-color: #f5fff6;
}

.expense-row {
  background-color: #fdf5f5;
}

.amount-cell .income {
  color: #2ca84f;
  font-weight: 600;
}

.amount-cell .expense {
  color: #d32f2f;
  font-weight: 600;
}

@media (max-width: 1024px) {
  .charts-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .header-actions {
    flex-direction: column;
    width: 100%;
  }

  .export-btn {
    width: 100%;
    justify-content: center;
  }

  .filters-section {
    flex-direction: column;
  }

  .filter-input {
    width: 100%;
  }

  .summary-cards {
    grid-template-columns: 1fr;
  }

  .trend-chart {
    flex-wrap: wrap;
  }

  .reports-content {
    padding: 15px;
  }
}
</style>