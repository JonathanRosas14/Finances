<template>
  <div class="categories-container">
    <header class="categories-header">
      <h1>Categories Management</h1>
    </header>

    <div class="categories-content">
      <div class="botom-agree">
        <button @click="openModal()">+ create category</button>
      </div>

      <!-- Categories list would be rendered here -->
      <div v-if="categories.length === 0" class="empty-state">
        <p>No categories available. Please create a new category.</p>
      </div>

      <div v-else class="categories-section">
        <!-- Render categories here -->
        <div class="categories-grid">
          <div
            v-for="category in categories"
            :key="category.id"
            class="category-card"
          >
            <div
              class="category-icon-circle"
              :style="{ backgroundColor: category.color }"
            >
              {{ category.icon }}
            </div>
            <div class="category-info">
              <h3>{{ category.name }}</h3>
              <p class="category-type">{{ category.type }}</p>
            </div>
            <button
              @click="deleteCategory(category.id)"
              class="delete-btn"
              title="Delete"
            >
              ✕
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal component would go here -->
    <transition name="modal">
      <!-- Modal content placeholder -->
      <div v-if="showModal" class="modal" @click="closeModal">
        <!-- Modal content would be implemented here -->
        <div class="modal-content" @click.stop>
          <h2>Create New Category</h2>
          <p>Customize the style of your new category</p>
          <!-- Form fields for creating a new category would go here -->
          <div class="form-group">
            <label for="category-name">Category Name:</label>
            <input
              type="text"
              id="category-name"
              name="category-name"
              v-model="categoryForm.name"
              required
            />
          </div>

          <div class="icon-forms">
            <div class="text-icon">
              <h2>Icon</h2>
            </div>
            <!-- Icon selection implementation would go here -->
            <div class="icon-picker-grid">
              <div
                v-for="icon in availableIcons"
                :key="icon"
                class="icon-option"
                @click="categoryForm.icon = icon"
                :class="{ selected: categoryForm.icon === icon }"
              >
                {{ icon }}
              </div>
            </div>
          </div>

          <div class="colors-forms">
            <div class="text-color">
              <h2>Color</h2>
              <div class="color-picker">
                <div
                  v-for="color in availableColors"
                  :key="color"
                  class="color-circle"
                  :style="{ backgroundColor: color }"
                  @click="categoryForm.color = color"
                  :class="{ selected: categoryForm.color === color }"
                ></div>
              </div>
            </div>
          </div>

          <div class="type-forms">
            <div class="text-type">
              <label for="type">Type</label>
              <select id="type" name="type" v-model="categoryForm.type">
                <option value="expense">Expense</option>
                <option value="income">Income</option>
              </select>
            </div>
          </div>

          <div class="modal-buttons">
            <button @click="closeModal" class="close">Close</button>
            <button @click="createCategory" class="submit">Create</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const categories = ref([]);
const showModal = ref(false);
const loading = ref(false);
const availableColors = ref([
  "#00ACEE", // Azul
  "#FF8C42", // Naranja
  "#FF1493", // Rosa
  "#9B59B6", // Púrpura
  "#4169E1", // Azul Marino
  "#20B2AA", // Verde Azulado
  "#FFB347", // Naranja claro
]);

const availableIcons = ref([
  "🏪", // Supermercado
  "🍽️", // Restaurante
  "🎬", // Cine
  "🏥", // Salud
  "🚗", // Transporte
  "🏠", // Casa
  "👕", // Ropa
  "📚", // Educación
  "✈️", // Viajes
  "🎮", // Entretenimiento
  "💼", // Trabajo
  "🎁", // Regalos
]);

const categoryForm = ref({
  name: "",
  color: "#00ACEE",
  type: "expense",
  icon: "🏪",
});

const openModal = () => {
  categoryForm.value = {
    name: "",
    color: "#00ACEE",
    type: "expense",
    icon: "🏪",
  };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const createCategory = async () => {
  try {
    if (!categoryForm.value.name.trim()) {
      alert("Please enter the category name");
      return;
    }

    loading.value = true;
    const token = localStorage.getItem("token");

    const response = await fetch("http://localhost:8000/api/categories/create/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(categoryForm.value),
    });

    if (!response.ok) {
      const error = await response.json();
      alert(error.message || "Error creating category");
      return;
    }

    const data = await response.json();
    categories.value.push(data.category);
    closeModal();
    categoryForm.value.name = "";
  } catch (error) {
    console.error("Error creating category:", error);
    alert("Error creating category");
  } finally {
    loading.value = false;
  }
};

const fetchCategories = async () => {
  try {
    loading.value = true;
    const token = localStorage.getItem("token");

    const response = await fetch("http://localhost:8000/api/categories/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Error getting categories");
    }

    const data = await response.json();
    categories.value = data;
  } catch (error) {
    console.error("Error getting categories:", error);
  } finally {
    loading.value = false;
  }
};

const deleteCategory = async (categoryId) => {
  if (!confirm("Are you sure you want to delete this category?")) {
    return;
  }

  try {
    const token = localStorage.getItem("token");

    const response = await fetch(
      `http://localhost:8000/api/categories/${categoryId}/delete/`,
      {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );

    if (!response.ok) {
      throw new Error("Error deleting category");
    }

    categories.value = categories.value.filter((c) => c.id !== categoryId);
  } catch (error) {
    console.error("Error deleting category:", error);
    alert("Error deleting category");
  }
};

onMounted(() => {
  fetchCategories();
});
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.categories-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
}

.categories-header {
  display: flex;
  align-items: center;
  background-color: #f8fdf8;
  color: #1a7f3a;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  padding: 20px 30px;
  border-bottom: 1px solid #e0e8e0;
  width: 100%;
}

.categories-header h1 {
  font-size: 28px;
  font-weight: 600;
}

.categories-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.botom-agree {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 30px;
}

.botom-agree button {
  background-color: #1a7f3a;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  font-size: 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.botom-agree button:hover {
  background-color: #166f33;
}

.empty-state {
  text-align: center;
  color: #888;
  font-size: 18px;
  margin-top: 50px;
}

.categories-section {
  width: 100%;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
  width: 100%;
}

.category-card {
  background-color: white;
  border: 1.5px solid #e0e8e0;
  border-radius: 10px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.category-card:hover {
  border-color: #1a7f3a;
  box-shadow: 0 8px 16px rgba(26, 127, 58, 0.12);
  transform: translateY(-2px);
}

.category-icon-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  margin-bottom: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.category-info {
  text-align: center;
  flex: 1;
  width: 100%;
}

.category-info h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 4px;
  word-break: break-word;
}

.category-type {
  font-size: 12px;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0;
}

.delete-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: none;
  background-color: rgba(255, 0, 0, 0.1);
  color: #e74c3c;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  opacity: 0;
}

.category-card:hover .delete-btn {
  opacity: 1;
}

.delete-btn:hover {
  background-color: #e74c3c;
  color: white;
  transform: scale(1.1);
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 12px;
  padding: 40px;
  max-width: 650px;
  width: 90%;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  max-height: 90vh;
  overflow-y: auto;
}

.modal-content h2 {
  font-size: 26px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #1a1a1a;
}

.modal-content > p {
  color: #888;
  margin-bottom: 30px;
  font-size: 14px;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 10px;
  font-weight: 600;
  color: #1a1a1a;
  font-size: 15px;
}

.form-group input,
.type-forms select {
  width: 100%;
  padding: 12px 14px;
  border: 1.5px solid #e0e8e0;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
  background-color: #fafbfa;
  transition: all 0.3s ease;
  color: #333;
}

.form-group input:focus,
.type-forms select:focus {
  outline: none;
  border-color: #1a7f3a;
  background-color: white;
  box-shadow: 0 0 0 3px rgba(26, 127, 58, 0.1);
}

.icon-forms,
.colors-forms,
.type-forms {
  margin-bottom: 28px;
}

.text-icon,
.text-color,
.text-type {
  margin-bottom: 16px;
}

.text-color h2,
.text-icon h2,
.text-type label {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #1a1a1a;
}

.color-picker {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  align-items: center;
  background-color: #fafbfa;
  padding: 16px;
  border-radius: 8px;
}

.color-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  cursor: pointer;
  border: 3px solid transparent;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
  flex-shrink: 0;
}

.color-circle:hover {
  transform: scale(1.12);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.color-circle.selected {
  border-color: #1a7f3a;
  box-shadow:
    0 0 0 2px white,
    0 0 0 5px #1a7f3a,
    0 4px 12px rgba(26, 127, 58, 0.2);
}

.modal-buttons {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 40px;
  padding-top: 24px;
  border-top: 1px solid #e0e8e0;
}

.close,
.submit {
  padding: 12px 28px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.close {
  background-color: #e8ebe8;
  color: #333;
}

.close:hover {
  background-color: #dce0dc;
  transform: translateY(-1px);
}

.submit {
  background-color: #1a7f3a;
  color: white;
  box-shadow: 0 2px 8px rgba(26, 127, 58, 0.2);
}

.submit:hover {
  background-color: #166f33;
  box-shadow: 0 4px 12px rgba(26, 127, 58, 0.3);
  transform: translateY(-1px);
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.icon-picker {
  border: 2px dashed #e0e8e0;
  padding: 32px;
  text-align: center;
  color: #999;
  font-size: 14px;
  border-radius: 8px;
  background-color: #fafbfa;
}

.icon-picker-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 10px;
  background-color: #fafbfa;
  padding: 16px;
  border-radius: 8px;
}

.icon-option {
  width: 100%;
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  cursor: pointer;
  border: 2px solid transparent;
  border-radius: 8px;
  transition: all 0.3s ease;
  background-color: white;
}

.icon-option:hover {
  border-color: #1a7f3a;
  background-color: #f0f5f0;
  transform: scale(1.05);
}

.icon-option.selected {
  border-color: #1a7f3a;
  background-color: #e8f4ec;
  box-shadow: 0 0 0 2px rgba(26, 127, 58, 0.1);
}
</style>