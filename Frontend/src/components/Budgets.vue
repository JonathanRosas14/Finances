<template>
  <div class="budgets-container">
    <header class="budgets-header">
      <h1>Budgets</h1>
    </header>
    <div class="budgets-content">
      <div class="button-group">
        <button @click="openModal()" class="btn-create">+ Create Budget</button>
      </div>

      <div v-if="budgets.length === 0" class="empty-state">
        <p>No budgets available. Please create a new budget.</p>
      </div>

      <div v-else class="budgets-grid">
        <div
          v-for="budget in budgets"
          :key="budget.id"
          class="budget-card"
          :class="{ 'budget-alert': isAlertActive(budget) }"
        >
          <div class="card-header">
            <div class="card-title-section">
              <h3>{{ budget.name }}</h3>
              <span class="period-badge">{{ budget.period }}</span>
            </div>
            <button @click="openMenu(budget.id)" class="menu-btn">⋮</button>
            <div
              v-if="activeMenu === budget.id"
              class="dropdown-menu"
              @click.stop
            >
              <button @click="editBudget(budget.id)" class="menu-item">
                Edit
              </button>
              <button @click="deleteBudget(budget.id)" class="menu-item delete">
                Delete
              </button>
            </div>
          </div>

          <div v-if="budget.category_name" class="card-category">
            {{ budget.category_name }}
          </div>

          <div class="card-progress">
            <div class="progress-info">
              <span class="spent">Spent: ${{ getBudgetSpent(budget.id) }}</span>
              <span class="limit">Limit: ${{ budget.amount }}</span>
            </div>
            <div class="progress-bar">
              <div
                class="progress-fill"
                :style="{ width: getProgressPercentage(budget.id) + '%' }"
                :class="{ 'progress-warning': isAlertActive(budget) }"
              ></div>
            </div>
            <div class="progress-percentage">
              {{ getProgressPercentage(budget.id) }}%
            </div>
          </div>

          <div v-if="budget.description" class="card-description">
            {{ budget.description }}
          </div>

          <div class="card-footer">
            <span class="date-range">{{
              formatDateRange(budget.start_date, budget.end_date)
            }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para crear/editar presupuesto -->
    <transition name="modal-fade">
      <div v-if="showModal" class="modal" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>{{ isEditMode ? "Edit Budget" : "Create Budget" }}</h2>
            <button type="button" class="modal-close" @click="closeModal">
              ×
            </button>
          </div>
          <p class="modal-subtitle">Manage your spending limits</p>

          <form
            @submit.prevent="isEditMode ? updateBudget() : addBudget()"
            class="budget-form"
          >
            <div class="form-group">
              <label for="name">Budget Name *</label>
              <input
                type="text"
                id="name"
                v-model="form.name"
                required
                placeholder="e.g., Food, Entertainment"
                class="form-input"
              />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="category">Category</label>
                <select
                  id="category"
                  v-model="form.category_id"
                  class="form-input"
                >
                  <option value="">General Budget</option>
                  <option
                    v-for="category in categories"
                    :key="category.id"
                    :value="category.id"
                  >
                    {{ category.name }}
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label for="period">Period *</label>
                <select
                  id="period"
                  v-model="form.period"
                  required
                  class="form-input"
                >
                  <option value="monthly">Monthly</option>
                  <option value="quarterly">Quarterly</option>
                  <option value="yearly">Yearly</option>
                </select>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="amount">Budget Amount *</label>
                <div class="amount-input-wrapper">
                  <span class="currency">$</span>
                  <input
                    type="number"
                    id="amount"
                    v-model="form.amount"
                    step="0.01"
                    required
                    placeholder="0.00"
                    class="form-input"
                  />
                </div>
              </div>
              <div class="form-group">
                <label for="alert">Alert at %</label>
                <input
                  type="number"
                  id="alert"
                  v-model="form.alert_percentage"
                  min="1"
                  max="100"
                  placeholder="80"
                  class="form-input"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="start-date">Start Date *</label>
                <input
                  type="date"
                  id="start-date"
                  v-model="form.start_date"
                  required
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label for="end-date">End Date</label>
                <input
                  type="date"
                  id="end-date"
                  v-model="form.end_date"
                  class="form-input"
                />
              </div>
            </div>

            <div class="form-group">
              <label for="description">Description</label>
              <textarea
                id="description"
                v-model="form.description"
                placeholder="Add notes about this budget..."
                rows="3"
                class="form-input"
              ></textarea>
            </div>

            <div class="form-group">
              <label class="checkbox-label">
                <input
                  type="checkbox"
                  v-model="form.is_active"
                  class="form-checkbox"
                />
                Active Budget
              </label>
            </div>

            <div class="form-actions">
              <button type="button" @click="closeModal" class="btn-cancel">
                Cancel
              </button>
              <button type="submit" class="btn-submit">
                {{ isEditMode ? "Update" : "Create" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";

// Estados
const budgets = ref([]);
const categories = ref([]);
const transactions = ref([]);
const showModal = ref(false);
const isEditMode = ref(false);
const editingId = ref(null);
const activeMenu = ref(null);

// Formulario
const form = ref({
  name: "",
  category_id: "",
  amount: "",
  period: "monthly",
  start_date: new Date().toISOString().split("T")[0],
  end_date: "",
  alert_percentage: 80,
  is_active: true,
  description: "",
});

const getToken = () => localStorage.getItem("token");

// Cargar categorías
const loadCategories = async () => {
  try {
    const token = getToken();
    if (!token) return;

    const response = await axios.get("http://localhost:8000/api/categories", {
      headers: { Authorization: `Bearer ${token}` },
    });
    categories.value = response.data;
  } catch (error) {
    console.error("Error al cargar categorías:", error);
  }
};

// Cargar presupuestos
const loadBudgets = async () => {
  try {
    const token = getToken();
    if (!token) return;

    const response = await axios.get("http://localhost:8000/api/budgets", {
      headers: { Authorization: `Bearer ${token}` },
    });
    budgets.value = response.data;
  } catch (error) {
    console.error("Error al cargar presupuestos:", error);
  }
};

// Cargar transacciones para calcular gasto
const loadTransactions = async () => {
  try {
    const token = getToken();
    if (!token) return;

    const response = await axios.get("http://localhost:8000/api/transactions", {
      headers: { Authorization: `Bearer ${token}` },
    });
    transactions.value = response.data;
  } catch (error) {
    console.error("Error al cargar transacciones:", error);
  }
};

// Calcular gasto en un presupuesto
const getBudgetSpent = (budgetId) => {
  const budget = budgets.value.find((b) => b.id === budgetId);
  if (!budget || !transactions.value) return "0.00";

  const spent = transactions.value
    .filter((t) => {
      if (budget.category_id && t.category_id !== budget.category_id)
        return false;
      if (t.type !== "expense") return false;

      const txDate = new Date(t.transaction_date);
      const startDate = new Date(budget.start_date);
      const endDate = budget.end_date ? new Date(budget.end_date) : new Date();

      return txDate >= startDate && txDate <= endDate;
    })
    .reduce((sum, t) => sum + parseFloat(t.amount), 0);

  return spent.toFixed(2);
};

// Calcular porcentaje de progreso
const getProgressPercentage = (budgetId) => {
  const budget = budgets.value.find((b) => b.id === budgetId);
  if (!budget) return 0;

  const spent = parseFloat(getBudgetSpent(budgetId));
  const percentage = (spent / budget.amount) * 100;

  return Math.min(Math.round(percentage), 100);
};

// Verificar si alerta está activa
const isAlertActive = (budget) => {
  return getProgressPercentage(budget.id) >= budget.alert_percentage;
};

// Formatear rango de fechas
const formatDateRange = (startDate, endDate) => {
  const start = new Date(startDate).toLocaleDateString("es-ES", {
    month: "short",
    day: "numeric",
  });
  const end = endDate
    ? new Date(endDate).toLocaleDateString("es-ES", {
        month: "short",
        day: "numeric",
        year: "numeric",
      })
    : "Open";

  return `${start} - ${end}`;
};

// Abrir modal
const openModal = () => {
  isEditMode.value = false;
  editingId.value = null;
  form.value = {
    name: "",
    category_id: "",
    amount: "",
    period: "monthly",
    start_date: new Date().toISOString().split("T")[0],
    end_date: "",
    alert_percentage: 80,
    is_active: true,
    description: "",
  };
  showModal.value = true;
};

// Cerrar modal
const closeModal = () => {
  showModal.value = false;
};

// Abrir menú dropdown
const openMenu = (budgetId) => {
  activeMenu.value = activeMenu.value === budgetId ? null : budgetId;
};

// Crear presupuesto
const addBudget = async () => {
  try {
    if (!form.value.name || !form.value.amount || !form.value.start_date) {
      alert("Por favor completa los campos requeridos");
      return;
    }

    const token = getToken();
    const response = await axios.post(
      "http://localhost:8000/api/budgets/create/",
      form.value,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      },
    );

    await loadBudgets();
    closeModal();
    alert("✅ Presupuesto creado exitosamente");
  } catch (error) {
    console.error("Error:", error);
    alert(error.response?.data?.message || "Error al crear presupuesto");
  }
};

// Editar presupuesto
const editBudget = (id) => {
  const budget = budgets.value.find((b) => b.id === id);
  if (!budget) return;

  isEditMode.value = true;
  editingId.value = id;
  form.value = { ...budget };
  activeMenu.value = null;
  showModal.value = true;
};

// Actualizar presupuesto
const updateBudget = async () => {
  try {
    const token = getToken();
    await axios.put(
      `http://localhost:8000/api/budgets/${editingId.value}`,
      form.value,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      },
    );

    await loadBudgets();
    closeModal();
    alert("✅ Presupuesto actualizado exitosamente");
  } catch (error) {
    console.error("Error:", error);
    alert(error.response?.data?.message || "Error al actualizar presupuesto");
  }
};

// Eliminar presupuesto
const deleteBudget = async (id) => {
  if (!confirm("¿Estás seguro de eliminar este presupuesto?")) return;

  try {
    const token = getToken();
    await axios.delete(`http://localhost:8000/api/budgets/${id}/delete/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    await loadBudgets();
    alert("✅ Presupuesto eliminado exitosamente");
  } catch (error) {
    console.error("Error:", error);
    alert(error.response?.data?.message || "Error al eliminar presupuesto");
  }
};

onMounted(() => {
  loadCategories();
  loadBudgets();
  loadTransactions();

  // Recargar transacciones cada 10 segundos para actualizar presupuestos
  const intervalId = setInterval(() => {
    loadTransactions();
  }, 10000);

  // Recargar cuando el usuario vuelve a esta pestaña
  const handleVisibilityChange = () => {
    if (!document.hidden) {
      loadTransactions();
      loadBudgets();
    }
  };
  document.addEventListener("visibilitychange", handleVisibilityChange);

  // Limpiar al desmontar el componente
  return () => {
    clearInterval(intervalId);
    document.removeEventListener("visibilitychange", handleVisibilityChange);
  };
});
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.budgets-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
}

.budgets-header {
  display: flex;
  align-items: center;
  background-color: #f8fdf8;
  color: #1a7f3a;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  padding: 20px 30px;
  border-bottom: 1px solid #e0e8e0;
  width: 100%;
}

.budgets-header h1 {
  font-size: 28px;
  font-weight: 600;
}

.budgets-content {
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
  color: #888888;
  font-size: 18px;
  margin-top: 50px;
}

.budgets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.budget-card {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #f0f0f0;
  transition: all 0.2s ease;
}

.budget-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.budget-card.budget-alert {
  border-left: 4px solid #e74c3c;
  background: linear-gradient(135deg, #fff5f5 0%, #ffffff 100%);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  position: relative;
}

.card-title-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.card-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.period-badge {
  background-color: #e8f5e9;
  color: #1a7f3a;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
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

.menu-btn:hover {
  color: #333;
}

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

.menu-item:first-child {
  border-bottom: 1px solid #f0f0f0;
}

.menu-item:hover {
  background-color: #f5f5f5;
}

.menu-item.delete:hover {
  background-color: #ffe8e8;
  color: #e74c3c;
}

.card-category {
  font-size: 12px;
  color: #666;
  margin-bottom: 12px;
  text-transform: capitalize;
  font-weight: 500;
}

.card-progress {
  margin: 16px 0;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 13px;
}

.spent {
  color: #e74c3c;
  font-weight: 600;
}

.limit {
  color: #999;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #e8e8e8;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #1a7f3a 0%, #16a34a 100%);
  transition: width 0.3s ease;
}

.progress-fill.progress-warning {
  background: linear-gradient(90deg, #f39c12 0%, #e74c3c 100%);
}

.progress-percentage {
  text-align: right;
  font-size: 13px;
  font-weight: 600;
  color: #333;
}

.card-description {
  font-size: 13px;
  color: #666;
  margin: 12px 0;
  font-style: italic;
}

.card-footer {
  border-top: 1px solid #f0f0f0;
  padding-top: 12px;
}

.date-range {
  font-size: 12px;
  color: #999;
}

/* Modal Styles */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

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
  max-width: 550px;
  box-shadow:
    0 10px 40px rgba(0, 0, 0, 0.15),
    0 0 0 1px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 16px;
  border-bottom: 1px solid #f0f0f0;
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
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.modal-close:hover {
  background-color: #f5f5f5;
  color: #333;
}

.modal-subtitle {
  padding: 0 24px 12px;
  color: #666;
  font-size: 13px;
  margin: 0;
}

.budget-form {
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

.form-row .form-group {
  margin-bottom: 0;
}

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

.form-input:hover {
  border-color: #d0d0d0;
}

.form-input textarea {
  resize: vertical;
  min-height: 70px;
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
  padding-left: 28px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  margin-bottom: 0;
  font-size: 14px;
  font-weight: 400;
  text-transform: none;
  letter-spacing: normal;
  color: #333;
  cursor: pointer;
}

.form-checkbox {
  width: 18px;
  height: 18px;
  margin-right: 8px;
  cursor: pointer;
  accent-color: #1a7f3a;
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

.btn-cancel {
  background-color: #f5f5f5;
  color: #333;
}

.btn-cancel:hover {
  background-color: #e8e8e8;
}

.btn-submit {
  background-color: #1a7f3a;
  color: #ffffff;
}

.btn-submit:hover {
  background-color: #166f33;
  box-shadow: 0 4px 12px rgba(26, 127, 58, 0.25);
}

.btn-submit:active {
  transform: scale(0.98);
}
</style>