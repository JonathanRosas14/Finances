<template>
  <div class="goals-container">
    <header class="goals-header">
      <h1>Goals</h1>
    </header>
    <div class="goals-content">
      <div class="button-group">
        <button @click="openModal()" class="btn-primary">
          + create goal
        </button>
      </div>
      <div v-if="goals.length === 0" class="empty-state">
        <p>No goals yet. Start by creating your first goal!</p>
      </div>
      <div v-else class="goals-section">
        <div v-for="goal in goals" :key="goal.id" class="goal-card">
          <div class="goal-header">
            <div class="goal-title">
              <h3>{{ goal.name }}</h3>
              <span :class="['priority-badge', goal.priority]">{{ goal.priority }}</span>
              <span :class="['status-badge', goal.status]">{{ goal.status }}</span>
            </div>
            <button @click="openMenu(goal.id)" class="menu-btn">⋮</button>
            <div v-if="activeMenu === goal.id" class="dropdown-menu" @click.stop>
              <button @click="editGoal(goal)" class="menu-item">Edit</button>
              <button @click="deleteGoal(goal.id)" class="menu-item delete">Delete</button>
            </div>
          </div>

          <p v-if="goal.description" class="goal-description">
            {{ goal.description }}
          </p>

          <div class="goal-progress">
            <div class="progress-info">
              <span class="progress-label">Progress</span>
              <span class="progress-percent"
                >{{ getProgressPercent(goal) }}%</span
              >
            </div>
            <div class="progress-bar">
              <div
                class="progress-fill"
                :style="{ width: getProgressPercent(goal) + '%' }"
              ></div>
            </div>
            <div class="progress-details">
              <span
                >${{ parseFloat(goal.current_amount || 0).toFixed(2) }}</span
              >
              <span class="separator">/</span>
              <span>${{ parseFloat(goal.target_amount || 0).toFixed(2) }}</span>
            </div>
          </div>

          <div class="goal-footer">
            <div class="goal-info">
              <span v-if="goal.category_name" class="category-tag">{{
                goal.category_name
              }}</span>
              <span class="target-date"
                >📅 {{ formatDate(goal.target_date) }}</span
              >
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal for creating/editing goals -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ editingGoal ? "Edit Goal" : "Create New Goal" }}</h2>
          <button @click="closeModal" class="close-btn">&times;</button>
        </div>

        <form @submit.prevent="saveGoal" class="goal-form">
          <div class="form-group">
            <label for="name">Goal Name *</label>
            <input
              id="name"
              v-model="formData.name"
              type="text"
              placeholder="e.g., Save for vacation"
              required
            />
          </div>

          <div class="form-group">
            <label for="description">Description</label>
            <textarea
              id="description"
              v-model="formData.description"
              placeholder="Add details about your goal..."
              rows="3"
            ></textarea>
          </div>

          <div class="form-group">
            <label for="target-amount">Target Amount *</label>
            <input
              id="target-amount"
              v-model.number="formData.target_amount"
              type="number"
              placeholder="0.00"
              step="0.01"
              min="0"
              required
            />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="target-date">Target Date *</label>
              <input
                id="target-date"
                v-model="formData.target_date"
                type="date"
                required
              />
            </div>

            <div class="form-group">
              <label for="category">Category (for tracking income)</label>
              <select
                id="category"
                v-model="formData.category"
                class="form-input"
              >
                <option :value="null">No category</option>
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
              <select
                id="priority"
                v-model="formData.priority"
                class="form-input"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>

            <div class="form-group">
              <label for="status">Status</label>
              <select id="status" v-model="formData.status" class="form-input">
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
                <option value="on_hold">On Hold</option>
              </select>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" @click="closeModal" class="cancel-btn">
              Cancel
            </button>
            <button type="submit" class="save-btn">
              {{ editingGoal ? "Update" : "Create" }} Goal
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>

// pendiente arreglar bug no crea las goals
import { ref, onMounted } from "vue";
import axios from "axios";

const goals = ref([]);
const categories = ref([]);
const showModal = ref(false);
const editingGoal = ref(null);
const activeMenu = ref(null);

const formData = ref({
  name: "",
  description: "",
  target_amount: null,
  target_date: "",
  category: "",
  priority: "medium",
  status: "in_progress",
});

const apiUrl = "http://localhost:8000/api/goals";

const getToken = () => {
  return localStorage.getItem("token");
};

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
    console.error("Error fetching categories:", error);
  }
};

const fetchGoals = async () => {
  try {
    const response = await axios.get(apiUrl, { headers: getHeaders() });
    goals.value = response.data;
  } catch (error) {
    console.error("Error fetching goals:", error);
  }
};

const openModal = () => {
  editingGoal.value = null;
  formData.value = {
    name: "",
    description: "",
    target_amount: null,
    target_date: "",
    category: null,
    priority: "medium",
    status: "in_progress",
  };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  editingGoal.value = null;
};

const openMenu = (goalId) => {
  activeMenu.value = activeMenu.value === goalId ? null : goalId;
};

const editGoal = (goal) => {
  editingGoal.value = goal;
  formData.value = {
    name: goal.name,
    description: goal.description,
    target_amount: goal.target_amount,
    target_date: goal.target_date,
    category: goal.category || null,
    priority: goal.priority,
    status: goal.status,
  };
  activeMenu.value = true;  
  showModal.value = true;
};

const saveGoal = async () => {
  try {
    if (!formData.value.name || !formData.value.target_amount || !formData.value.target_date) {
      alert("Por favor completa los campos requeridos");
      return;
    }

    const token = getToken();
    
    if (editingGoal.value) {
      // Update existing goal
      await axios.put(
        `http://localhost:8000/api/goals/${editingGoal.value.id}/`, 
        formData.value,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );
    } else {
      // Create new goal
      await axios.post(
        "http://localhost:8000/api/goals/create/", 
        formData.value,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );
    }
    
    await fetchGoals();
    closeModal();
    alert('✅ Goal saved successfully');
  } catch (error) {
    console.error("Error:", error);
    alert(error.response?.data?.message || 'Error saving goal');
  }
};

const deleteGoal = async (goalId) => {
  if (!confirm('Are you sure you want to delete this goal?')) {
    return;
  }
  
  try {
    await axios.delete(`http://localhost:8000/api/goals/${goalId}/delete/`, { 
      headers: getHeaders() 
    });
    fetchGoals();
    alert('✅ Goal deleted successfully');
  } catch (error) {
    console.error("Error deleting goal:", error);
    alert(error.response?.data?.message || 'Error deleting goal');
  }
};

const getGoalSpent = (goalId) => {
  const goal = goals.value.find((b) => b.id === goalId);
  return goal ? goal.current_amount || 0 : 0;
};

  
const getProgressPercent = (goal) => {
  if (!goal || !goal.target_amount) return 0;

  const spent = parseFloat(goal.current_amount || 0);
  const percentage = (spent / goal.target_amount) * 100;

  return Math.min(Math.round(percentage), 100);
};

const formatDate = (dateString) => {
  const options = { year: "numeric", month: "short", day: "numeric" };
  return new Date(dateString).toLocaleDateString("es-ES", options);
};

const getCategoryName = (categoryId) => {
  const category = categories.value.find((c) => c.id === categoryId);
  return category ? category.name : "General";
};

onMounted(() => {
  loadCategories();
  fetchGoals();

  // Recargar goals cada 3 segundos para actualizar progreso automáticamente
  const intervalId = setInterval(() => {
    fetchGoals();
  }, 3000);

  // Recargar cuando el usuario vuelve a esta pestaña
  const handleFocus = () => {
    fetchGoals();
  };
  window.addEventListener("focus", handleFocus);

  // Escuchar eventos de actualización de transacciones desde otros componentes
  const handleTransactionUpdated = () => {
    fetchGoals();
  };
  window.addEventListener("transactionUpdated", handleTransactionUpdated);

  return () => {
    clearInterval(intervalId);
    window.removeEventListener("focus", handleFocus);
    window.removeEventListener("transactionUpdated", handleTransactionUpdated);
  };
});
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
}

.bottom-agree {
  display: flex;
  margin-bottom: 20px;
}

.create-goal-btn {
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

.create-goal-btn:hover {
  background-color: #166f33;
  box-shadow: 0 4px 12px rgba(26, 127, 58, 0.3);
  transform: translateY(-2px);
}

.button-group .btn-primary {
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

.button-group .btn-primary:hover {
  background-color: #166f33;
  box-shadow: 0 4px 12px rgba(26, 127, 58, 0.3);
  transform: translateY(-2px);
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #888;
  font-size: 18px;
}

.goals-section {
  display: grid;
  gap: 15px;
}

.goal-card {
  background: white;
  border: 1px solid #e0e8e0;
  border-radius: 8px;
  padding: 20px;
  transition: box-shadow 0.3s ease;
}

.goal-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.goal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
  position: relative;
}

.goal-title {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.goal-title h3 {
  font-size: 18px;
  color: #1a1a1a;
}

.priority-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.priority-badge.high {
  background-color: #ffebee;
  color: #c62828;
}

.priority-badge.medium {
  background-color: #fff3e0;
  color: #e65100;
}

.priority-badge.low {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.in_progress {
  background-color: #e3f2fd;
  color: #1565c0;
}

.status-badge.completed {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.status-badge.on_hold {
  background-color: #f3e5f5;
  color: #6a1b9a;
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
  color: #dc3545;
  font-weight: 500;
}

.goal-description {
  color: #666;
  font-size: 14px;
  margin-bottom: 15px;
  line-height: 1.5;
}

.goal-progress {
  margin-bottom: 15px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 13px;
}

.progress-label {
  color: #666;
  font-weight: 500;
}

.progress-percent {
  color: #1a7f3a;
  font-weight: 600;
}

.progress-bar {
  height: 8px;
  background-color: #e0e8e0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background-color: #1a7f3a;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-details {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #888;
}

.separator {
  margin: 0 4px;
}

.goal-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.goal-info {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 13px;
}

.category-tag {
  background-color: #e8f5e9;
  color: #1a7f3a;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: 500;
}

.target-date {
  color: #666;
}

.add-progress-btn {
  background-color: #e8f5e9;
  color: #1a7f3a;
  border: 1px solid #1a7f3a;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.add-progress-btn:hover {
  background-color: #1a7f3a;
  color: white;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e0e8e0;
}

.modal-header h2 {
  font-size: 20px;
  color: #1a1a1a;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #1a1a1a;
}

.goal-form {
  padding: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #1a1a1a;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d0d7d0;
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
  transition: border-color 0.2s ease;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #1a7f3a;
  box-shadow: 0 0 0 3px rgba(26, 127, 58, 0.1);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.form-row .form-group {
  margin-bottom: 0;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e0e8e0;
}

.cancel-btn,
.save-btn {
  flex: 1;
  padding: 10px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.3s ease;
}

.cancel-btn {
  background-color: #f0f0f0;
  color: #1a1a1a;
}

.cancel-btn:hover {
  background-color: #e0e0e0;
}

.save-btn {
  background-color: #1a7f3a;
  color: white;
}

.save-btn:hover {
  background-color: #145c2b;
}

/* Scrollbar styles */
.goals-content::-webkit-scrollbar {
  width: 8px;
}

.goals-content::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.goals-content::-webkit-scrollbar-thumb {
  background: #bbb;
  border-radius: 4px;
}

.goals-content::-webkit-scrollbar-thumb:hover {
  background: #888;
}

.modal-content::-webkit-scrollbar {
  width: 8px;
}

.modal-content::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.modal-content::-webkit-scrollbar-thumb {
  background: #bbb;
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background: #888;
}
</style>
