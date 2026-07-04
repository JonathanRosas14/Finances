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
        <!--Summary-->
        <router-link to="/dashboard" class="nav-link" :class="{ active: activeRoutePath === '/dashboard' }">Summary</router-link>
        <!--Budgets-->
        <router-link to="/budgets" class="nav-link" :class="{ active: activeRoutePath === '/budgets' }">Budgets</router-link>
        <!--Goals-->
        <router-link to="/goals" class="nav-link" :class="{ active: activeRoutePath === '/goals' }">Goals</router-link>
        <!--Transactions-->
        <router-link to="/transactions" class="nav-link" :class="{ active: activeRoutePath === '/transactions' }">Transactions</router-link>
        <!--Debts-->
        <router-link to="/debts" class="nav-link" :class="{ active: activeRoutePath === '/debts' }">Debts</router-link>
        <!--Categories-->
        <router-link to="/categories" class="nav-link" :class="{ active: activeRoutePath === '/categories' }">Categories</router-link>
        <!--Reports-->
        <router-link to="/reports" class="nav-link" :class="{ active: activeRoutePath === '/reports' }">Reports</router-link>
        <!--Settings-->
        <router-link to="/settings" class="nav-link" :class="{ active: activeRoutePath === '/settings' }">Settings</router-link>
      </div>

      <div class="log-out">
        <button @click="showLogoutModal = true" class="logout-btn">Log Out</button>
      </div>
    </nav>

    <section class="main-content">
      <router-view />
    </section>

    <transition name="modal-fade">
      <div v-if="showLogoutModal" class="modal" @click="showLogoutModal = false">
        <div class="modal-content confirm-modal" @click.stop>
          <div class="modal-header">
            <h2>Confirm Log Out</h2>
            <button type="button" class="modal-close" @click="showLogoutModal = false">×</button>
          </div>
          <p class="modal-subtitle">Are you sure you want to log out?</p>
          <div class="form-actions">
            <button type="button" @click="handleLogout" class="btn-logout-confirm">Yes, Log Out</button>
            <button type="button" @click="showLogoutModal = false" class="btn-cancel">Cancel</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";

const showLogoutModal = ref(false);
const user = ref({});
const loading = ref(true);
const router = useRouter();
const route = useRoute();

const activeRoutePath = computed(() => route.path)

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

.nav-link.active {
  background: #e8f5e9;
  color: #1a7f3a;
  font-weight: 600;
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
  background-color: #ffebee !important;
  color: #c62828 !important;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #fafbfa;
}

.modal-fade-enter-active,
.modal-fade-leave-active { transition: opacity 0.3s ease; }
.modal-fade-enter-from,
.modal-fade-leave-to { opacity: 0; }

.modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  border-radius: 16px;
  padding: 32px;
  width: 90%;
  max-width: 420px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}

.confirm-modal .modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.confirm-modal .modal-header h2 {
  font-size: 20px;
  color: #1a1a2e;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  color: #999;
  cursor: pointer;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: 0.2s;
}

.modal-close:hover {
  background: #f5f5f5;
  color: #333;
}

.confirm-modal .modal-subtitle {
  font-size: 15px;
  color: #666;
  margin-bottom: 24px;
  line-height: 1.5;
}

.confirm-modal .form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.confirm-modal .btn-logout-confirm {
  padding: 10px 20px;
  background: #c62828;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.confirm-modal .btn-logout-confirm:hover {
  background: #b71c1c;
}

.confirm-modal .btn-cancel {
  padding: 10px 20px;
  background: #f5f5f5;
  color: #333;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.confirm-modal .btn-cancel:hover {
  background: #e0e0e0;
}
</style>