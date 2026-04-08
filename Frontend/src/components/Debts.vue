<template>
  <div class="debts-container">
    <header class="debts-header">
      <h1>Debts Management</h1>
    </header>
    <div class="debts-content">
      <div class="button-group">
        <button @click="openModal()" class="btn-primary">+ create debt</button>
      </div>

      <div v-if="debts.length === 0" class="empty-state">
        <p>No debts found. Start by creating a new debt.</p>
      </div>

      <div v-else class="debts-grid">
        <div
          v-for="debt in filteredDebts"
          :key="debt.id"
          class="debt-card"
        >
          <div class="card-header">
            <div class="card-title-section">
              <h3>{{ debt.name }}</h3>
              <span class="creditor-badge">{{ debt.creditor || "General" }}</span>
            </div>
            <button @click="openMenu(debt.id)" class="menu-btn">⋮</button>
            <div
              v-if="activeMenu === debt.id"
              class="dropdown-menu"
              @click.stop
            >
              <button @click="editDebt(debt.id)" class="menu-item">
                Edit
              </button>
              <button @click="deleteDebt(debt.id)" class="menu-item delete">
                Delete
              </button>
            </div>
          </div>

          <div class="card-progress">
            <div class="progress-info">
              <span class="paid">Paid: ${{ parseFloat(debt.paid_amount_calculated).toFixed(2) }}</span>
              <span class="total">Total: ${{ parseFloat(debt.total_with_interest).toFixed(2) }}</span>
            </div>
            <div class="progress-bar">
              <div
                class="progress-fill"
                :style="{ width: getProgressPercent(debt) + '%' }"
              ></div>
            </div>
            <div class="progress-percentage">
              {{ getProgressPercent(debt) }}%
            </div>
          </div>

          <div class="card-details">
            <div class="detail-item">
              <span class="label">Status:</span>
              <span :class="['status-badge', debt.status]">{{ debt.status }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Due Date:</span>
              <span>{{ formatDate(debt.due_date) }}</span>
            </div>
            <div v-if="debt.interest_rate" class="detail-item">
              <span class="label">Interest:</span>
              <span>{{ debt.interest_rate }}%</span>
            </div>
          </div>

          <div v-if="debt.description" class="card-description">
            {{ debt.description }}
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para crear/editar deuda -->
    <transition name="modal-fade">
      <div v-if="showModal" class="modal" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>{{ isEditMode ? "Edit Debt" : "Create Debt" }}</h2>
            <button type="button" class="modal-close" @click="closeModal">
              ×
            </button>
          </div>
          <p class="modal-subtitle">Manage your debts and track payments</p>

          <form
            @submit.prevent="isEditMode ? updateDebt() : addDebt()"
            class="debt-form"
          >
            <div class="form-group">
              <label for="name">Debt Name *</label>
              <input
                type="text"
                id="name"
                v-model="form.name"
                required
                placeholder="e.g., Car Loan, Credit Card"
                class="form-input"
              />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="creditor">Creditor Name</label>
                <input
                  type="text"
                  id="creditor"
                  v-model="form.creditor"
                  placeholder="e.g., Bank ABC, Company XYZ"
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label for="interest-rate">Interest Rate (%)</label>
                <input
                  type="number"
                  id="interest-rate"
                  v-model="form.interest_rate"
                  step="0.01"
                  placeholder="0.00"
                  class="form-input"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="total-amount">Total Amount *</label>
                <div class="amount-input-wrapper">
                  <span class="currency">$</span>
                  <input
                    type="number"
                    id="total-amount"
                    v-model="form.total_amount"
                    step="0.01"
                    required
                    placeholder="0.00"
                    class="form-input"
                  />
                </div>
              </div>
              <div class="form-group">
                <label for="due-date">Due Date *</label>
                <input
                  type="date"
                  id="due-date"
                  v-model="form.due_date"
                  required
                  class="form-input"
                />
              </div>
            </div>

            <div class="form-group">
              <label for="category">Category</label>
              <select
                id="category"
                v-model="form.category"
                class="form-input"
              >
                <option :value="null">General Debt</option>
                <option
                  v-for="category in categories"
                  :key="category.id"
                  :value="category.id"
                >
                  {{ category.name }}
                </option>
              </select>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="months">Months *</label>
                <input
                  type="number"
                  id="months"
                  v-model="form.months"
                  min="1"
                  required
                  placeholder="Number of months"
                  class="form-input"
                />
              </div>
              <div class="form-group" v-if="form.total_amount && form.interest_rate && form.months">
                <label>Total with Interest</label>
                <div class="amount-display">
                  ${{ calculateTotalWithInterest() }}
                </div>
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
import { ref, computed, onMounted, onUnmounted } from "vue";
import axios from "axios";

// Estado
const debts = ref([]);
const categories = ref([]);
const showModal = ref(false);
const loading = ref(false);
const isEditMode = ref(false);
const editingId = ref(null);
const activeMenu = ref(null);

// Filtros
const search = ref("");
const filterStatus = ref("");

// Formulario
const form = ref({
  name: "",
  creditor: "",
  total_amount: "",
  paid_amount: 0,
  due_date: "",
  interest_rate: 0,
  months: 1,
  category: null,
  description: "",
  status: "pending",
});

// Obtener token
const getToken = () => {
  return localStorage.getItem("token");
};

// Obtener headers
const getHeaders = () => {
  return {
    Authorization: `Bearer ${getToken()}`,
  };
};

// Cargar categorías
const loadCategories = async () => {
  try {
    const response = await axios.get("http://localhost:8000/api/categories", {
      headers: getHeaders(),
    });
    categories.value = response.data;
  } catch (error) {
    console.error("Error loading categories:", error);
  }
};

// Cargar deudas
const loadDebts = async () => {
  try {
    const response = await axios.get("http://localhost:8000/api/debts", {
      headers: getHeaders(),
    });
    debts.value = response.data;
  } catch (error) {
    console.error("Error loading debts:", error);
  }
};

// Deudas filtradas
const filteredDebts = computed(() => {
  return debts.value.filter((debt) => {
    const matchesSearch =
      debt.name.toLowerCase().includes(search.value.toLowerCase()) ||
      (debt.creditor &&
        debt.creditor.toLowerCase().includes(search.value.toLowerCase()));

    const matchesStatus =
      !filterStatus.value || debt.status === filterStatus.value;

    return matchesSearch && matchesStatus;
  });
});

// Abrir/cerrar menú
const openMenu = (debtId) => {
  activeMenu.value = activeMenu.value === debtId ? null : debtId;
};

// Abrir modal
const openModal = () => {
  isEditMode.value = false;
  editingId.value = null;
  form.value = {
    name: "",
    creditor: "",
    total_amount: "",
    paid_amount: 0,
    due_date: "",
    interest_rate: 0,
    months: 1,
    category: null,
    description: "",
    status: "pending",
  };
  showModal.value = true;
};

// Cerrar modal
const closeModal = () => {
  showModal.value = false;
  isEditMode.value = false;
  editingId.value = null;
};

// Editar deuda
const editDebt = async (debtId) => {
  try {
    const debtToEdit = debts.value.find((d) => d.id === debtId);
    if (debtToEdit) {
      editingId.value = debtId;
      form.value = { ...debtToEdit };
      isEditMode.value = true;
      showModal.value = true;
    }
  } catch (error) {
    console.error("Error editing debt:", error);
  }
};

// Agregar deuda
const addDebt = async () => {
  try {
    if (!form.value.name || !form.value.total_amount || !form.value.due_date) {
      alert("Por favor completa los campos requeridos");
      return;
    }

    const token = getToken();
    await axios.post("http://localhost:8000/api/debts/create/", form.value, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    
    await loadDebts();
    closeModal();
    alert("✅ Deuda creada exitosamente");
  } catch (error) {
    console.error("Error:", error);
    alert(error.response?.data?.message || "Error al crear deuda");
  }
};

// Actualizar deuda
const updateDebt = async () => {
  try {
    const token = getToken();
    await axios.put(
      `http://localhost:8000/api/debts/${editingId.value}/`,
      form.value,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );
    
    await loadDebts();
    closeModal();
    alert("✅ Deuda actualizada exitosamente");
  } catch (error) {
    console.error("Error:", error);
    alert(error.response?.data?.message || "Error al actualizar deuda");
  }
};

// Eliminar deuda
const deleteDebt = async (debtId) => {
  if (!confirm("¿Estás seguro de eliminar esta deuda?")) return;

  try {
    const token = getToken();
    await axios.delete(`http://localhost:8000/api/debts/${debtId}/delete/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    
    await loadDebts();
    alert("✅ Deuda eliminada exitosamente");
  } catch (error) {
    console.error("Error:", error);
    alert(error.response?.data?.message || "Error al eliminar deuda");
  }
};

// Calcular porcentaje de progreso
const getProgressPercent = (debt) => {
  if (!debt.total_with_interest) return 0;
  return Math.min(
    Math.round((debt.paid_amount_calculated / debt.total_with_interest) * 100),
    100,
  );
};

// Calcular el total con intereses
const calculateTotalWithInterest = () => {
  const total = parseFloat(form.value.total_amount) || 0;
  const rate = parseFloat(form.value.interest_rate) || 0;
  const months = parseInt(form.value.months) || 1;
  
  const interest = total * (rate / 100) * months;
  return (total + interest).toFixed(2);
};

// Formatear fecha
const formatDate = (dateString) => {
  const options = { year: "numeric", month: "short", day: "numeric" };
  return new Date(dateString).toLocaleDateString("es-ES", options);
};

// Ciclo de vida
onMounted(() => {
  loadCategories();
  loadDebts();

  // Recargar deudas cada 3 segundos para actualizar progreso automáticamente
  const intervalId = setInterval(() => {
    loadDebts();
  }, 3000);

  // Recargar cuando el usuario vuelve a esta pestaña
  const handleFocus = () => {
    console.log("👀 Debts: enfoco la ventana");
    loadDebts();
  };
  window.addEventListener("focus", handleFocus);

  // Escuchar eventos de actualización de transacciones desde otros componentes
  const handleTransactionUpdated = async () => {
    console.log("🔥 Debts: Se recibió evento transactionUpdated");
    await loadDebts();
    console.log("🗘 Debts: Datos recargados");
  };
  window.addEventListener("transactionUpdated", handleTransactionUpdated);

  // Escuchar eventos propios de deudas
  const handleDebtUpdated = async () => {
    console.log("🔥 Debts: Se recibió evento debtUpdated");
    await loadDebts();
  };
  window.addEventListener("debtUpdated", handleDebtUpdated);

  return () => {
    clearInterval(intervalId);
    window.removeEventListener("focus", handleFocus);
    window.removeEventListener("transactionUpdated", handleTransactionUpdated);
    window.removeEventListener("debtUpdated", handleDebtUpdated);
  };
});
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
}

.button-group {
  display: flex;
  margin-bottom: 20px;
  gap: 10px;
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

.btn-primary {
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

.btn-primary:hover {
  background-color: #166f33;
  box-shadow: 0 4px 12px rgba(26, 127, 58, 0.3);
  transform: translateY(-2px);
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.empty-state p {
  font-size: 16px;
}

.debts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.debt-card {
  background: white;
  border: 1px solid #e0e8e0;
  border-radius: 8px;
  padding: 20px;
  transition: box-shadow 0.3s ease;
}

.debt-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
  position: relative;
}

.card-title-section {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.card-title-section h3 {
  font-size: 18px;
  color: #1a1a1a;
  margin: 0;
}

.creditor-badge {
  background-color: #e8f5e9;
  color: #1a7f3a;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.menu-btn {
  background: none;
  border: none;
  font-size: 20px;
  color: #999;
  cursor: pointer;
  padding: 0;
  transition: color 0.3s ease;
}

.menu-btn:hover {
  color: #1a7f3a;
}

.dropdown-menu {
  position: absolute;
  top: 30px;
  right: 0;
  background: white;
  border: 1px solid #e0e8e0;
  border-radius: 6px;
  padding: 8px 0;
  min-width: 150px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.menu-item {
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  padding: 10px 16px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.menu-item:hover {
  background-color: #f5f5f5;
}

.menu-item.delete {
  color: #d32f2f;
}

.card-progress {
  margin-bottom: 15px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  margin-bottom: 8px;
}

.progress-info .paid {
  color: #1a7f3a;
  font-weight: 600;
}

.progress-info .total {
  color: #666;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #e8f5e9;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #1a7f3a, #2db856);
  border-radius: 10px;
  transition: width 0.3s ease;
}

.progress-percentage {
  text-align: right;
  font-size: 13px;
  font-weight: 600;
  color: #1a7f3a;
}

.card-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 10px;
  padding: 10px 0;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}

.detail-item .label {
  color: #666;
  font-weight: 600;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.pending {
  background-color: #fff3cd;
  color: #856404;
}

.status-badge.in_progress {
  background-color: #cfe2ff;
  color: #084298;
}

.status-badge.paid {
  background-color: #d1e7dd;
  color: #0f5132;
}

.card-description {
  font-size: 13px;
  color: #666;
  margin-top: 10px;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 4px;
  border-left: 3px solid #1a7f3a;
}

.debts-table thead {
  background-color: #f0f8f0;
  border-bottom: 2px solid #d0e0d0;
}

.debts-table th {
  padding: 15px;
  text-align: left;
  font-weight: 600;
  color: #1a7f3a;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.debts-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 14px;
  color: #333;
}

.debts-table tbody tr:hover {
  background-color: #f9fff9;
}

.progress-bar {
  width: 100px;
  height: 6px;
  background-color: #e0e0e0;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 5px;
}

.progress-fill {
  height: 100%;
  background-color: #1a7f3a;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 12px;
  color: #666;
  font-weight: 500;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.pending {
  background-color: #fff3cd;
  color: #856404;
}

.status-badge.in_progress {
  background-color: #cfe2ff;
  color: #084298;
}

.status-badge.paid {
  background-color: #d1e7dd;
  color: #0f5132;
}

.edit-btn,
.delete-btn {
  padding: 6px 10px;
  margin: 0 2px;
  font-size: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: white;
}

.edit-btn {
  color: #0066cc;
  border-color: #0066cc;
}

.edit-btn:hover {
  background-color: #0066cc;
  color: white;
}

.delete-btn {
  color: #ffffff;
  background-color: #dc3545;
  border-color: #dc3545;
  border: none;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(220, 53, 69, 0.2);
}

.delete-btn:hover {
  background-color: #c82333;
  border-color: #c82333;
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
  transform: translateY(-1px);
}

/* Modal Styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  padding: 30px;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.modal-header h2 {
  color: #1a7f3a;
  font-size: 22px;
}

.modal-close {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: #666;
  transition: color 0.3s ease;
}

.modal-close:hover {
  color: #000;
}

.modal-subtitle {
  color: #666;
  font-size: 14px;
  margin-bottom: 20px;
}

.debt-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-group label {
  color: #333;
  font-weight: 600;
  font-size: 14px;
}

.form-input,
input[type="text"],
input[type="number"],
input[type="date"],
select,
textarea {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
  transition: all 0.3s ease;
}

.form-input:focus,
input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: #1a7f3a;
  box-shadow: 0 0 0 3px rgba(26, 127, 58, 0.1);
}

.amount-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.currency {
  position: absolute;
  left: 12px;
  color: #666;
  font-weight: 600;
}

.amount-input-wrapper input {
  padding-left: 25px;
  width: 100%;
}

.amount-display {
  padding: 10px 12px;
  background-color: #f0f8f0;
  border: 1px solid #1a7f3a;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  color: #1a7f3a;
  display: flex;
  align-items: center;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

.btn-cancel,
.btn-submit {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
}

.btn-cancel {
  background-color: #f0f0f0;
  color: #333;
}

.btn-cancel:hover {
  background-color: #e0e0e0;
}

.btn-submit {
  background-color: #1a7f3a;
  color: white;
}

.btn-submit:hover {
  background-color: #165f30;
}

/* Animation */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .debts-grid {
    grid-template-columns: 1fr;
  }

  .modal-content {
    width: 95%;
    padding: 20px;
  }
}
</style>
