<template>
  <div class="goals-container">
    <header class="goals-header">
      <h1>Goals</h1>
    </header>
    <div class="goals-content">
      <div class="button-group">
        <button @click="openModal()" class="btn-create">+ create goal</button>
      </div>

      <div v-if="goals.length === 0" class="empty-state">
        <p>No goals yet. Create your first goal!</p>
      </div>

      <div v-else class="goals-list">
        <div
          v-for="goal in goals"
          :key="goal.id"
          class="goal-card"
        >
          <div class="card-header">
            <div class="card-title-section">
              <h3>{{ goal.name }}</h3>
              <span class="priority-badge" :class="'priority-' + goal.priority.toLowerCase()">
                {{ goal.priority.toUpperCase() }}
              </span>
              <span class="status-badge" :class="'status-' + goal.status.toLowerCase()">
                {{ goal.status.toUpperCase() }}
              </span>
            </div>
            <button @click="openMenu(goal.id)" class="menu-btn">⋮</button>
            <div
              v-if="activeMenu === goal.id"
              class="dropdown-menu"
              @click.stop
            >
              <button @click="editGoal(goal.id)" class="menu-item">Edit</button>
              <button @click="deleteGoal(goal.id)" class="menu-item delete">Delete</button>
            </div>
          </div>

          <div v-if="goal.description" class="card-description">
            {{ goal.description }}
          </div>

          <div class="card-progress">
            <div class="progress-label">Progress</div>
            <div class="progress-bar">
              <div
                class="progress-fill"
                :style="{ width: getGoalProgress(goal) + '%' }"
                :class="{ 'progress-complete': getGoalProgress(goal) >= 100 }"
              ></div>
            </div>
            <div class="progress-percentage">{{ getGoalProgress(goal) }}%</div>
          </div>

          <div class="card-amounts">
            <span class="amount-current">${{ getGoalSaved(goal).toFixed(2) }}</span>
            <span class="amount-separator">/</span>
            <span class="amount-target">${{ parseFloat(goal.target_amount).toFixed(2) }}</span>
          </div>

          <div class="card-footer">
            <span v-if="goal.category_name" class="category-tag">{{ goal.category_name }}</span>
            <span v-if="goal.target_date" class="date-tag">
              📅 {{ formatDate(goal.target_date) }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Notification -->
    <transition name="notif-fade">
      <div v-if="notification.show" class="notification" :class="notification.type">
        <span>✓ {{ notification.message }}</span>
        <button @click="notification.show = false" class="notif-close">×</button>
      </div>
    </transition>

    <!-- Modal crear/editar goal -->
    <transition name="modal-fade">
      <div v-if="showModal" class="modal" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>{{ isEditMode ? 'Edit Goal' : 'Create New Goal' }}</h2>
            <button type="button" class="modal-close" @click="closeModal">×</button>
          </div>

          <form @submit.prevent="isEditMode ? updateGoal() : addGoal()" class="goal-form">
            <div class="form-group">
              <label for="name">Goal Name *</label>
              <input
                type="text"
                id="name"
                v-model="form.name"
                required
                placeholder="e.g., House, Vacation"
                class="form-input"
              />
            </div>

            <div class="form-group">
              <label for="description">Description</label>
              <textarea
                id="description"
                v-model="form.description"
                placeholder="Add details about your goal..."
                rows="3"
                class="form-input"
              ></textarea>
            </div>

            <div class="form-group">
              <label for="target_amount">Target Amount *</label>
              <input
                type="number"
                id="target_amount"
                v-model="form.target_amount"
                step="0.01"
                min="0.01"
                required
                placeholder="0.00"
                class="form-input"
              />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="target_date">Target Date *</label>
                <input
                  type="date"
                  id="target_date"
                  v-model="form.target_date"
                  required
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label for="category">Category (for tracking income)</label>
                <select id="category" v-model="form.category_id" class="form-input">
                  <option value="">No category</option>
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

            <div class="form-row">
              <div class="form-group">
                <label for="priority">Priority</label>
                <select id="priority" v-model="form.priority" class="form-input">
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
              <div class="form-group">
                <label for="status">Status</label>
                <select id="status" v-model="form.status" class="form-input">
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                  <option value="paused">Paused</option>
                </select>
              </div>
            </div>

            <div class="form-actions">
              <button type="button" @click="closeModal" class="btn-cancel">Cancel</button>
              <button type="submit" class="btn-submit">
                {{ isEditMode ? 'Update Goal' : 'Create Goal' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- Delete confirmation modal -->
    <transition name="modal-fade">
      <div v-if="showDeleteConfirmModal" class="modal" @click="cancelDelete">
        <div class="modal-content delete-modal" @click.stop>
          <div class="modal-header">
            <h2>Delete Goal</h2>
            <button type="button" class="modal-close" @click="cancelDelete">
              ×
            </button>
          </div>
          <p class="modal-subtitle">
            Are you sure you want to delete this goal?
          </p>
          <p style="text-align: center; color: #666; font-size: 14px; margin: 0;">
            This action cannot be undone.
          </p>
          <div class="form-actions">
            <button type="button" @click="cancelDelete" class="btn-cancel">
              Cancel
            </button>
            <button type="button" @click="confirmDelete" class="btn-delete">
              Delete
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Create confirmation modal -->
    <transition name="modal-fade">
      <div v-if="showCreateConfirmModal" class="modal" @click="cancelCreateGoal">
        <div class="modal-content confirm-modal" @click.stop>
          <div class="modal-header">
            <h2>Create Goal</h2>
            <button type="button" class="modal-close" @click="cancelCreateGoal">
              ×
            </button>
          </div>
          <p class="modal-subtitle">
            Are you sure you want to create this goal?
          </p>
          <div class="form-actions">
            <button type="button" @click="cancelCreateGoal" class="btn-cancel">
              Cancel
            </button>
            <button type="button" @click="confirmCreateGoal" class="btn-delete">
              Create
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../lib/api'

const goals = ref([])
const categories = ref([])
const transactions = ref([])
const showModal = ref(false)
const isEditMode = ref(false)
const editingId = ref(null)
const activeMenu = ref(null)

const notification = ref({ show: false, message: '', type: 'success' })
const showDeleteConfirmModal = ref(false)
const showCreateConfirmModal = ref(false)
const goalToDelete = ref(null)

const form = ref({
  name: '',
  description: '',
  target_amount: '',
  target_date: '',
  category_id: '',
  priority: 'medium',
  status: 'in_progress',
})

const getToken = () => localStorage.getItem('token')

const showNotification = (message, type = 'success') => {
  notification.value = { show: true, message, type }
  setTimeout(() => { notification.value.show = false }, 3500)
}

// ── Data loading ──────────────────────────────────────────────
const loadCategories = async () => {
  try {
    const token = getToken()
    if (!token) return
    const response = await api.get('/api/categories/', {
      headers: { Authorization: `Bearer ${token}` },
    })
    categories.value = response.data
  } catch (error) {
    console.error('Error loading categories:', error)
  }
}

const loadGoals = async () => {
  try {
    const token = getToken()
    if (!token) return
    const response = await api.get('/api/goals/', {
      headers: { Authorization: `Bearer ${token}` },
    })
    goals.value = response.data
  } catch (error) {
    console.error('Error loading goals:', error)
  }
}

const loadTransactions = async () => {
  try {
    const token = getToken()
    if (!token) return
    const response = await api.get('/api/transactions/', {
      headers: { Authorization: `Bearer ${token}` },
    })
    transactions.value = response.data
  } catch (error) {
    console.error('Error loading transactions:', error)
  }
}

// ── Progress logic ──────────────────────────────────────────
// Sum all income transactions whose category
// matches the goal's associated category.
const getGoalSaved = (goal) => {
  if (!goal.category_id) return 0
  return transactions.value
    .filter(
      (t) =>
        t.category_id === goal.category_id &&
        t.type === 'income'
    )
    .reduce((sum, t) => sum + parseFloat(t.amount), 0)
}

const getGoalProgress = (goal) => {
  const saved = getGoalSaved(goal)
  const target = parseFloat(goal.target_amount)
  if (!target) return 0
  return Math.min(Math.round((saved / target) * 100), 100)
}

// ── Formatting ────────────────────────────────────────────────────
const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString('en-US', {
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
    description: '',
    target_amount: '',
    target_date: '',
    category_id: '',
    priority: 'medium',
    status: 'in_progress',
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
const addGoal = () => {
  showCreateConfirmModal.value = true
}

const confirmCreateGoal = async () => {
  try {
    const token = getToken()
    await api.post(
      '/api/goals/create/',
      {
        ...form.value,
        category_id: form.value.category_id || null,
      },
      { headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` } }
    )
    await loadGoals()
    closeModal()
    showCreateConfirmModal.value = false
    showNotification('Goal saved successfully')
  } catch (error) {
    console.error('Error:', error)
    showCreateConfirmModal.value = false
    showNotification(error.response?.data?.message || 'Error creating goal', 'error')
  }
}

const cancelCreateGoal = () => {
  showCreateConfirmModal.value = false
}

const editGoal = (id) => {
  const goal = goals.value.find((g) => g.id === id)
  if (!goal) return
  isEditMode.value = true
  editingId.value = id
  form.value = {
    name: goal.name,
    description: goal.description || '',
    target_amount: goal.target_amount,
    target_date: goal.target_date,
    category_id: goal.category_id || '',
    priority: goal.priority,
    status: goal.status,
  }
  activeMenu.value = null
  showModal.value = true
}

const updateGoal = async () => {
  try {
    const token = getToken()
    await api.put(
      `/api/goals/${editingId.value}/`,
      {
        ...form.value,
        category_id: form.value.category_id || null,
      },
      { headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` } }
    )
    await loadGoals()
    closeModal()
    showNotification('Goal updated successfully')
  } catch (error) {
    console.error('Error:', error)
    showNotification(error.response?.data?.message || 'Error updating goal', 'error')
  }
}

const deleteGoal = (id) => {
  goalToDelete.value = id
  showDeleteConfirmModal.value = true
}

const confirmDelete = async () => {
  try {
    const token = getToken()
    await api.delete(`/api/goals/${goalToDelete.value}/delete/`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    await loadGoals()
    showDeleteConfirmModal.value = false
    goalToDelete.value = null
    showNotification('Goal deleted successfully')
  } catch (error) {
    console.error('Error:', error)
    showDeleteConfirmModal.value = false
    showNotification(error.response?.data?.message || 'Error deleting goal', 'error')
  }
}

const cancelDelete = () => {
  showDeleteConfirmModal.value = false
  goalToDelete.value = null
}

onMounted(() => {
  loadCategories()
  loadGoals()
  loadTransactions()

  const intervalId = setInterval(() => {
    loadTransactions()
  }, 10000)

  const handleVisibilityChange = () => {
    if (!document.hidden) {
      loadTransactions()
      loadGoals()
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

.goals-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
}

.goals-header {
  display: flex;
  align-items: center;
  background-color: #f8fdf8;
  color: #1a7f3a;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  padding: 20px 30px;
  border-bottom: 1px solid #e0e8e0;
  width: 100%;
}

.goals-header h1 {
  font-size: 28px;
  font-weight: 600;
}

.goals-content {
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

/* ── Goals list (wide single column as in the design) ── */
.goals-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.goal-card {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 20px 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #f0f0f0;
  transition: all 0.2s ease;
  position: relative;
}

.goal-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

/* ── Card header ── */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
  position: relative;
}

.card-title-section {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.card-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: #222;
  margin: 0;
}

/* Priority badges */
.priority-badge {
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.priority-low    { background: #e8f5e9; color: #2e7d32; }
.priority-medium { background: #fff8e1; color: #f9a825; }
.priority-high   { background: #fdecea; color: #c62828; }

/* Status badges */
.status-badge {
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.status-in_progress { background: #e3f2fd; color: #1565c0; }
.status-completed   { background: #e8f5e9; color: #2e7d32; }
.status-paused      { background: #f5f5f5; color: #757575; }

/* Dropdown menu */
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

/* ── Description ── */
.card-description {
  font-size: 13px;
  color: #666;
  margin-bottom: 14px;
  font-style: italic;
}

/* ── Progreso ── */
.card-progress {
  margin: 14px 0 8px;
}

.progress-label {
  font-size: 12px;
  font-weight: 600;
  color: #555;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
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

/* ── Amounts ── */
.card-amounts {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 10px 0;
  font-size: 14px;
}

.amount-current {
  font-weight: 700;
  color: #1a7f3a;
}

.amount-separator {
  color: #bbb;
}

.amount-target {
  color: #999;
  font-weight: 500;
}

/* ── Footer ── */
.card-footer {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
  flex-wrap: wrap;
}

.category-tag {
  background: #e8f5e9;
  color: #1a7f3a;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.date-tag {
  font-size: 12px;
  color: #888;
}

/* ── Notification ── */
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

.notification.error {
  background: #ffebee;
  color: #c62828;
  border: 1px solid #ef9a9a;
  box-shadow: 0 4px 16px rgba(198, 40, 40, 0.15);
}

/* Delete modal */
.delete-modal {
  max-width: 520px;
  padding: 0;
}

.delete-modal .modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 16px;
  border-bottom: 1px solid #f0f0f0;
  position: sticky;
  top: 0;
  background: #fff;
  z-index: 1;
}

.delete-modal .modal-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: #e74c3c;
  margin: 0;
}

.delete-modal .modal-subtitle {
  text-align: center;
  padding: 16px 24px 8px;
  font-size: 16px;
  color: #333;
}

.delete-modal .form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 16px;
  padding: 16px 24px 24px;
  border-top: 1px solid #f0f0f0;
}

/* Confirm modal */
.confirm-modal {
  max-width: 520px;
  padding: 0;
}

.confirm-modal .modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 16px;
  border-bottom: 1px solid #f0f0f0;
  position: sticky;
  top: 0;
  background: #fff;
  z-index: 1;
}

.confirm-modal .modal-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: #1a7f3a;
  margin: 0;
}

.confirm-modal .modal-subtitle {
  text-align: center;
  padding: 16px 24px 8px;
  font-size: 16px;
  color: #333;
}

.confirm-modal .form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 16px;
  padding: 16px 24px 24px;
  border-top: 1px solid #f0f0f0;
}

.confirm-modal .btn-delete {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #1a7f3a;
  color: #ffffff;
}

.confirm-modal .btn-delete:hover {
  background-color: #166f33;
  box-shadow: 0 4px 12px rgba(26, 127, 58, 0.25);
}

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
  max-width: 520px;
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
  align-items: center;
  padding: 24px 24px 16px;
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
}

.modal-close:hover { background-color: #f5f5f5; color: #333; }

.goal-form {
  padding: 24px;
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

.btn-delete {
  background-color: #e74c3c;
  color: #ffffff;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-delete:hover {
  background-color: #c0392b;
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.25);
}

.btn-delete:active { transform: scale(0.98); }

.modal-subtitle {
  text-align: center;
  padding: 0 24px;
  margin-top: 16px;
  font-size: 16px;
  color: #333;
}
</style>