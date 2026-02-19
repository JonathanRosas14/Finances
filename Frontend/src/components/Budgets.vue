<template>
  <div class="budgets-container">
    <header class="budgets-header">
      <h1>Budgets</h1>
    </header>
    <div class="budgets-content">
      <!-- Content goes here -->
    </div>
  </div>
</template>

<script setup></script>

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
}
</style>