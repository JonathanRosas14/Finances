<template>
  <div class="main-page">
    <nav class="sidebar">
      <div class="logo">
        <div class="logo-icon">
          <img src="../assets/Logo.png" alt="Logo" />
        </div>
        <span>Finances Pro</span>
      </div>
      <div class="nav-links">
        <!--Resumen-->
        <router-link to="/dashboard" class="nav-link">Summary</router-link>
        <!--Presupuestos-->
        <router-link to="/budgets" class="nav-link">Budgets</router-link>
        <!--Metas-->
        <router-link to="/goals" class="nav-link">Goals</router-link>
        <!--Transacciones-->
        <router-link to="/transactions" class="nav-link"
          >Transactions</router-link
        >
        <!--Deudas-->
        <router-link to="/debts" class="nav-link">Debts</router-link>
        <!--Categorías-->
        <router-link to="/categories" class="nav-link">Categories</router-link>
        <!--Reportes-->
        <router-link to="/reports" class="nav-link">Reports</router-link>
        <!--Configuraciones-->
        <router-link to="/settings" class="nav-link">Settings</router-link>
      </div>

      <div class="log-out">
        <button @click="handleLogout" class="logout-btn">Log Out</button>
      </div>
    </nav>

    <section class="main-content">
      <router-view />
    </section>
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const user = ref({});
const loading = ref(true);
const router = useRouter();

onMounted(() => {
  const savedUser = localStorage.getItem("user");

  if (!savedUser) {
    router.push("/");
    return;
  }

  user.value = JSON.parse(savedUser);
  loading.value = false;
});

const handleLogout = () => {
  localStorage.clear();
  router.push("/");
};
</script>
<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.main-page {
  display: flex;
  height: 100vh;
  background-color: #ffffff;
  font-family: manrope, sans-serif;
}

.logo {
  display: flex;
  align-items: center;
  font-size: 22px;
  font-weight: bold;
  color: #1a7f3a;
}

.logo span {
  margin-left: 10px;
}
.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-icon img {
  width: 50px;
  height: 50px;
}

.sidebar {
  width: 250px;
  background-color: #f8fdf8;
  color: #ffffff;
  display: flex;
  flex-direction: column;
  padding: 20px;
  border-right: 1px solid #e0e8e0;
  gap: 30px;
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.nav-link {
  text-decoration: none;
  color: #4a5568;
  font-size: 18px;
  padding: 10px;
  border-radius: 5px;
  transition:
    background-color 0.3s,
    color 0.3s;
}

.nav-link:hover {
  background-color: #e8f5e9;
  color: #1a7f3a;
}

.log-out {
  margin-top: auto;
}
.logout-btn {
  width: 100%;
  padding: 10px;
  color: #4a5568;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background-color: #ef5350;
  color: #ffffff;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #fafbfa;
}
</style>