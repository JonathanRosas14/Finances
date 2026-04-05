<template>
  <div class="debts-container">
    <header class="debts-header">
      <h1>Debts Management</h1>
    </header>
    <div class="debts-content">
      <div class="button-group">
        <button @click="openModal()" class="btn-create">+ Create Debt</button>
      </div>

      <div v-if="debts.length === 0" class="empty-state">
        <p>No debts registered. Create your first debt.</p>
      </div>

      <div v-else class="debts-grid">
        <div
          v-for="debt in debts"
          :key="debt.id"
          class="debt-card"
        >
          <div class="card-header">
            <div class="card-title-section">
              <h3>{{ debt.name }}</h3>
              <span v-if="debt.creditor_name" class="creditor-badge">{{ debt.creditor_name }}</span>
            </div>
            <button @click="openMenu(debt.id)" class="menu-btn">⋮</button>
            <div
              v-if="activeMenu === debt.id"
              class="dropdown-menu"
              @click.stop
            >
              <button @click="editDebt(debt.id)" class="menu-item">Edit</button>
              <button @click="deleteDebt(debt.id)" class="menu-item delete">Delete</button>
            </div>
          </div>

          <div class="card-amounts">
            <div class="amount-row">
              <span class="label">Paid:</span>
              <span class="paid-amount">${{ getDebtPaid(debt).toFixed(2) }}</span>
            </div>
            <div class="amount-row">
              <span class="label">Total:</span>
              <span class="total-amount">${{ parseFloat(debt.total_with_interest).toFixed(2) }}</span>
            </div>
          </div>

          <div class="card-progress">
            <div class="progress-bar">
              <div
                class="progress-fill"
                :style="{ width: getDebtProgress(debt) + '%' }"
                :class="{ 'progress-complete': getDebtProgress(debt) >= 100 }"
              ></div>
            </div>
            <div class="progress-percentage">{{ getDebtProgress(debt) }}%</div>
          </div>

          <div class="card-details">
            <div class="detail-row">
              <span class="detail-label">Status:</span>
              <span class="status-badge" :class="'status-' + debt.status.toLowerCase()">
                {{ debt.status.toUpperCase() }}
              </span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Due Date:</span>
              <span class="detail-value">{{ formatDate(debt.due_date) }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Interest:</span>
              <span class="detail-value">{{ debt.interest_rate }}%</span>
            </div>
            <div v-if="debt.months > 0" class="detail-row">
              <span class="detail-label">Months:</span>
              <span class="detail-value">{{ debt.months }}</span>
            </div>
            <div v-if="debt.category_name" class="detail-row">
              <span class="detail-label">Category:</span>
              <span class="category-tag">{{ debt.category_name }}</span>
            </div>
          </div>

          <div v-if="debt.description" class="card-description">
            {{ debt.description }}
          </div>
        </div>
      </div>
    </div>

    <!-- Notificación -->
    <transition name="notif-fade">
      <div v-if="notification.show" class="notification">
        <span>✓ {{ notification.message }}</span>
        <button @click="notification.show = false" class="notif-close">×</button>
      </div>
    </transition>

    <!-- Modal crear/editar deuda -->
    <transition name="modal-fade">
      <div v-if="showModal" class="modal" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <div>
              <h2>{{ isEditMode ? 'Edit Debt' : 'Create Debt' }}</h2>
              <p class="modal-subtitle">Manage your debts and track payments</p>
            </div>
            <button type="button" class="modal-close" @click="closeModal">×</button>
          </div>

          <form @submit.prevent="isEditMode ? updateDebt() : addDebt()" class="debt-form">
            <div class="form-group">
              <label for="name">Debt Name *</label>
              <input
                type="text"
                id="name"
                v-model="form.name"
                required
                placeholder="e.g., Tarjeta de crédito"
                class="form-input"
              />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="creditor_name">Creditor Name</label>
                <input
                  type="text"
                  id="creditor_name"
                  v-model="form.creditor_name"
                  placeholder="e.g., Bancolombia"
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label for="interest_rate">Interest Rate (%)</label>
                <input
                  type="number"
                  id="interest_rate"
                  v-model="form.interest_rate"
                  step="0.01"
                  min="0"
                  placeholder="0"
                  class="form-input"
                  @input="recalculate"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="amount">Total Amount *</label>
                <div class="amount-input-wrapper">
                  <span class="currency">$</span>
                  <input
                    type="number"
                    id="amount"
                    v-model="form.amount"
                    step="0.01"
                    min="0.01"
                    required
                    placeholder="0"
                    class="form-input"
                    @input="recalculate"
                  />
                </div>
              </div>
              <div class="form-group">
                <label for="months">Months</label>
                <input
                  type="number"
                  id="months"
                  v-model="form.months"
                  min="0"
                  placeholder="0"
                  class="form-input"
                  @input="recalculate"
                />
              </div>
            </div>

            <!-- Preview del cálculo de interés compuesto -->
            <div v-if="calculatedTotal > 0" class="interest-preview">
              <div class="preview-row">
                <span>Principal:</span>
                <span>${{ parseFloat(form.amount || 0).toLocaleString('es-CO') }}</span>
              </div>
              <div v-if="form.interest_rate > 0 && form.months > 0" class="preview-row">
                <span>Interest ({{ form.interest_rate }}% × {{ form.months }} meses):</span>
                <span class="interest-value">
                  +${{ (calculatedTotal - parseFloat(form.amount || 0)).toLocaleString('es-CO', { minimumFractionDigits: 2 }) }}
                </span>
              </div>
              <div class="preview-row preview-total">
                <span>Total with interest:</span>
                <span>${{ calculatedTotal.toLocaleString('es-CO', { minimumFractionDigits: 2 }) }}</span>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="due_date">Due Date *</label>
                <input
                  type="date"
                  id="due_date"
                  v-model="form.due_date"
                  required
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label for="category">Category</label>
                <select id="category" v-model="form.category_id" class="form-input">
                  <option value="">General Debt</option>
                  <option
                    v-for="category in categories"
                    :key="category.id"
                    :value="category.id"
                  >
                    {{ category.name }}
                  </option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label for="description">Description</label>
              <textarea
                id="description"
                v-model="form.description"
                placeholder="Add notes about this debt..."
                rows="3"
                class="form-input"
              ></textarea>
            </div>

            <div class="form-group">
              <label for="status">Status</label>
              <select id="status" v-model="form.status" class="form-input">
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="paid">Paid</option>
              </select>
            </div>

            <div class="form-actions">
              <button type="button" @click="closeModal" class="btn-cancel">Cancel</button>
              <button type="submit" class="btn-submit">
                {{ isEditMode ? 'Update' : 'Create' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const debts = ref([])
const categories = ref([])
const transactions = ref([])
const showModal = ref(false)
const isEditMode = ref(false)
const editingId = ref(null)
const activeMenu = ref(null)

const notification = ref({ show: false, message: '' })

const form = ref({
  name: '',
  creditor_name: '',
  amount: '',
  interest_rate: 0,
  months: 0,
  due_date: '',
  category_id: '',
  description: '',
  status: 'pending',
})

const getToken = () => localStorage.getItem('token')

const showNotification = (message) => {
  notification.value = { show: true, message }
  setTimeout(() => { notification.value.show = false }, 3500)
}

// ── Cálculo de interés compuesto ────────────────────────────────
// Fórmula: total = monto * (1 + tasa/100) ^ meses
const calculatedTotal = computed(() => {
  const amount = parseFloat(form.value.amount) || 0
  const rate   = parseFloat(form.value.interest_rate) || 0
  const months = parseInt(form.value.months) || 0
  if (amount <= 0) return 0
  if (rate <= 0 || months <= 0) return amount
  return amount * Math.pow(1 + rate / 100, months)
})

// Disparado en cada cambio de input para mantener el preview vivo
const recalculate = () => { /* reactivo automáticamente via computed */ }

// ── Carga de datos ──────────────────────────────────────────────
const loadCategories = async () => {
  try {
    const token = getToken()
    if (!token) return
    const response = await axios.get('http://localhost:8000/api/categories/', {
      headers: { Authorization: `Bearer ${token}` },
    })
    categories.value = response.data
  } catch (error) {
    console.error('Error al cargar categorías:', error)
  }
}

const loadDebts = async () => {
  try {
    const token = getToken()
    if (!token) return
    const response = await axios.get('http://localhost:8000/api/debts/', {
      headers: { Authorization: `Bearer ${token}` },
    })
    debts.value = response.data
  } catch (error) {
    console.error('Error al cargar deudas:', error)
  }
}

const loadTransactions = async () => {
  try {
    const token = getToken()
    if (!token) return
    const response = await axios.get('http://localhost:8000/api/transactions/', {
      headers: { Authorization: `Bearer ${token}` },
    })
    transactions.value = response.data
  } catch (error) {
    console.error('Error al cargar transacciones:', error)
  }
}

// ── Lógica de progreso de deuda ─────────────────────────────────
// Suma transacciones de tipo 'expense' (pagos) de la categoría asociada
const getDebtPaid = (debt) => {
  if (!debt.category_id) return 0
  return transactions.value
    .filter(
      (t) =>
        t.category_id === debt.category_id &&
        t.type === 'expense'
    )
    .reduce((sum, t) => sum + parseFloat(t.amount), 0)
}

const getDebtProgress = (debt) => {
  const paid  = getDebtPaid(debt)
  const total = parseFloat(debt.total_with_interest)
  if (!total) return 0
  return Math.min(Math.round((paid / total) * 100), 100)
}

// ── Formateo ────────────────────────────────────────────────────
const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('es-ES', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

// ── Modal ───────────────────────────────────────────────────────
const openModal = () => {
  isEditMode.value = false
  editingId.value = null
  form.value = {
    name: '',
    creditor_name: '',
    amount: '',
    interest_rate: 0,
    months: 0,
    due_date: '',
    category_id: '',
    description: '',
    status: 'pending',
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const openMenu = (id) => {
  activeMenu.value = activeMenu.value === id ? null : id
}

// ── CRUD ────────────────────────────────────────────────────────
const addDebt = async () => {
  try {
    const token = getToken()
    const payload = {
      ...form.value,
      category_id: form.value.category_id || null,
      // Enviamos el total calculado para que el backend lo guarde
      total_with_interest: calculatedTotal.value,
    }
    await axios.post('http://localhost:8000/api/debts/create/', payload, {
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    })
    await loadDebts()
    closeModal()
    showNotification('Deuda creada exitosamente')
  } catch (error) {
    console.error('Error:', error)
    alert(error.response?.data?.message || 'Error al crear deuda')
  }
}

const editDebt = (id) => {
  const debt = debts.value.find((d) => d.id === id)
  if (!debt) return
  isEditMode.value = true
  editingId.value = id
  form.value = {
    name: debt.name,
    creditor_name: debt.creditor_name || '',
    amount: debt.amount,
    interest_rate: debt.interest_rate || 0,
    months: debt.months || 0,
    due_date: debt.due_date,
    category_id: debt.category_id || '',
    description: debt.description || '',
    status: debt.status,
  }
  activeMenu.value = null
  showModal.value = true
}

const updateDebt = async () => {
  try {
    const token = getToken()
    const payload = {
      ...form.value,
      category_id: form.value.category_id || null,
      total_with_interest: calculatedTotal.value,
    }
    await axios.put(`http://localhost:8000/api/debts/${editingId.value}/`, payload, {
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    })
    await loadDebts()
    closeModal()
    showNotification('Deuda actualizada exitosamente')
  } catch (error) {
    console.error('Error:', error)
    alert(error.response?.data?.message || 'Error al actualizar deuda')
  }
}

const deleteDebt = async (id) => {
  if (!confirm('¿Estás seguro de eliminar esta deuda?')) return
  try {
    const token = getToken()
    await axios.delete(`http://localhost:8000/api/debts/${id}/delete/`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    await loadDebts()
    showNotification('Deuda eliminada exitosamente')
  } catch (error) {
    console.error('Error:', error)
    alert(error.response?.data?.message || 'Error al eliminar deuda')
  }
}

onMounted(() => {
  loadCategories()
  loadDebts()
  loadTransactions()

  const intervalId = setInterval(() => {
    loadTransactions()
  }, 10000)

  const handleVisibilityChange = () => {
    if (!document.hidden) {
      loadTransactions()
      loadDebts()
    }
  }
  document.addEventListener('visibilitychange', handleVisibilityChange)

  return () => {
    clearInterval(intervalId)
    document.removeEventListener('visibilitychange', handleVisibilityChange)
  }
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.debts-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
}

.debts-header {
  display: flex;
  align-items: center;
  background-color: #f8fdf8;
  color: #1a7f3a;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  padding: 20px 30px;
  border-bottom: 1px solid #e0e8e0;
  width: 100%;
}

.debts-header h1 {
  font-size: 28px;
  font-weight: 600;
}

.debts-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: #fafafa;
}

.button-group {
  margin-bottom: 24px;
}

.btn-create {
  background-color: #1a7f3a;
  color: #ffffff;
  border: none;
  padding: 12px 24px;
  font-size: 15px;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(26, 127, 58, 0.2);
}

.btn-create:hover {
  background-color: #166f33;
  box-shadow: 0 4px 12px rgba(26, 127, 58, 0.3);
  transform: translateY(-2px);
}

.empty-state {
  text-align: center;
  color: #888;
  font-size: 18px;
  margin-top: 50px;
}

/* ── Grid de cards (igual que budgets) ── */
.debts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.debt-card {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #f0f0f0;
  transition: all 0.2s ease;
  position: relative;
}

.debt-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

/* ── Card header ── */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 14px;
  position: relative;
}

.card-title-section {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.card-header h3 {
  font-size: 16px;
  font-weight: 700;
  color: #222;
  margin: 0;
}

.creditor-badge {
  background: #e3f2fd;
  color: #1565c0;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.menu-btn {
  background: none;
  border: none;
  font-size: 20px;
  color: #999;
  cursor: pointer;
  padding: 4px 8px;
  transition: all 0.2s ease;
}

.menu-btn:hover { color: #333; }

.dropdown-menu {
  position: absolute;
  top: 30px;
  right: 0;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 120px;
  z-index: 10;
}

.menu-item {
  display: block;
  width: 100%;
  border: none;
  padding: 10px 16px;
  text-align: left;
  background: none;
  cursor: pointer;
  font-size: 14px;
  color: #333;
  transition: all 0.2s ease;
}

.menu-item:first-child { border-bottom: 1px solid #f0f0f0; }
.menu-item:hover { background-color: #f5f5f5; }
.menu-item.delete:hover { background-color: #ffe8e8; color: #e74c3c; }

/* ── Montos ── */
.card-amounts {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.amount-row {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.label {
  font-size: 11px;
  color: #999;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.paid-amount {
  font-size: 14px;
  font-weight: 700;
  color: #1a7f3a;
}

.total-amount {
  font-size: 14px;
  font-weight: 700;
  color: #333;
}

/* ── Progreso ── */
.card-progress {
  margin: 10px 0 14px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #e8e8e8;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 4px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #1a7f3a 0%, #16a34a 100%);
  transition: width 0.5s ease;
  border-radius: 4px;
}

.progress-fill.progress-complete {
  background: linear-gradient(90deg, #16a34a 0%, #4caf50 100%);
}

.progress-percentage {
  text-align: right;
  font-size: 13px;
  font-weight: 700;
  color: #1a7f3a;
}

/* ── Detalles ── */
.card-details {
  border-top: 1px solid #f0f0f0;
  padding-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}

.detail-label {
  color: #888;
  font-weight: 500;
}

.detail-value {
  color: #333;
  font-weight: 600;
}

.status-badge {
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.status-pending     { background: #fff8e1; color: #f9a825; }
.status-in_progress { background: #e3f2fd; color: #1565c0; }
.status-paid        { background: #e8f5e9; color: #2e7d32; }

.category-tag {
  background: #e8f5e9;
  color: #1a7f3a;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
}

.card-description {
  font-size: 12px;
  color: #888;
  margin-top: 10px;
  font-style: italic;
}

/* ── Notificación ── */
.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  background: #e8f5e9;
  color: #1a7f3a;
  border: 1px solid #a5d6a7;
  border-radius: 10px;
  padding: 14px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 4px 16px rgba(26, 127, 58, 0.15);
  z-index: 2000;
}

.notif-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #1a7f3a;
  line-height: 1;
}

.notif-fade-enter-active,
.notif-fade-leave-active { transition: all 0.3s ease; }
.notif-fade-enter-from,
.notif-fade-leave-to { opacity: 0; transform: translateY(-10px); }

/* ── Modal ── */
.modal-fade-enter-active,
.modal-fade-leave-active { transition: opacity 0.3s ease; }
.modal-fade-enter-from,
.modal-fade-leave-to { opacity: 0; }

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.55);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}

.modal-content {
  background-color: #ffffff;
  border-radius: 12px;
  width: 90%;
  max-width: 560px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  animation: slideUp 0.3s ease;
  max-height: 90vh;
  overflow-y: auto;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 24px 24px 12px;
  border-bottom: 1px solid #f0f0f0;
  position: sticky;
  top: 0;
  background: #fff;
  z-index: 1;
}

.modal-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: #1a7f3a;
  margin: 0 0 4px;
}

.modal-subtitle {
  font-size: 13px;
  color: #888;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 28px;
  color: #999;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.modal-close:hover { background-color: #f5f5f5; color: #333; }

.debt-form {
  padding: 24px;
}

/* ── Preview de interés compuesto ── */
.interest-preview {
  background: linear-gradient(135deg, #f0faf4 0%, #e8f5e9 100%);
  border: 1px solid #c8e6c9;
  border-radius: 10px;
  padding: 14px 16px;
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.preview-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #555;
}

.interest-value {
  color: #e67e22;
  font-weight: 600;
}

.preview-total {
  border-top: 1px solid #c8e6c9;
  padding-top: 8px;
  margin-top: 4px;
  font-weight: 700;
  color: #1a7f3a;
  font-size: 14px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}

.form-group {
  margin-bottom: 16px;
}

.form-row .form-group { margin-bottom: 0; }

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  color: #333;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  transition: all 0.2s ease;
  background-color: #fafafa;
}

.form-input:focus {
  outline: none;
  border-color: #1a7f3a;
  background-color: #ffffff;
  box-shadow: 0 0 0 3px rgba(26, 127, 58, 0.1);
}

.form-input:hover { border-color: #d0d0d0; }

textarea.form-input {
  resize: vertical;
  min-height: 80px;
}

.amount-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.currency {
  position: absolute;
  left: 12px;
  color: #999;
  font-weight: 500;
  font-size: 14px;
  pointer-events: none;
}

.amount-input-wrapper .form-input {
  padding-left: 24px;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.btn-cancel,
.btn-submit {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel { background-color: #f5f5f5; color: #333; }
.btn-cancel:hover { background-color: #e8e8e8; }

.btn-submit { background-color: #1a7f3a; color: #ffffff; }
.btn-submit:hover {
  background-color: #166f33;
  box-shadow: 0 4px 12px rgba(26, 127, 58, 0.25);
}
.btn-submit:active { transform: scale(0.98); }
</style>