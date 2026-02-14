<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <h1>Dashboard Principal</h1>
    </header>
    <div class="dashboard-content">
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

.dashboard-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
}

.dashboard-header {
  display: flex;
  align-items: center;
  background-color: #f8fdf8;
  color: #1a7f3a;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  padding: 20px 30px;
  border-bottom: 1px solid #e0e8e0;
  width: 100%;
}

.dashboard-header h1 {
  font-size: 28px;
  font-weight: 600;
}

.dashboard-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}
</style>