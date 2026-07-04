<template>
  <div class="settings-container">
    <header class="settings-header">
      <div class="settings-header-text">
        <h1>Settings</h1>
        <p class="settings-subtitle">
          Preferences are stored on this device. Sign in again after clearing
          session data.
        </p>
      </div>
      <div class="header-actions">
        <span v-if="saveMessage" class="save-toast">{{ saveMessage }}</span>
        <button type="button" class="primary-btn" :disabled="saving" @click="save">
          {{ saving ? 'Saving…' : 'Save changes' }}
        </button>
      </div>
    </header>

    <div class="settings-layout">
      <section class="settings-panel">
        <h2 class="panel-title">Account</h2>
        <p class="field-hint">Read-only from your current session.</p>
        <div v-if="userProfile" class="settings-card-highlight">
          <div class="kv-row">
            <span class="kv-label">Username</span>
            <span class="kv-value">{{ userProfile.username || '—' }}</span>
          </div>
          <div class="kv-row">
            <span class="kv-label">Email</span>
            <span class="kv-value">{{ userProfile.email || '—' }}</span>
          </div>
          <div class="kv-row">
            <span class="kv-label">Provider</span>
            <span class="kv-value">{{ userProfile.provider || 'local' }}</span>
          </div>
        </div>
        <p v-else class="empty-profile">No user in local storage. Log in again.</p>
      </section>

      <section class="settings-panel">
        <h2 class="panel-title">Appearance</h2>
        <label class="field-label" for="theme">Theme</label>
        <select id="theme" v-model="form.theme" class="form-input">
          <option value="light">Light</option>
          <option value="dark">Dark</option>
        </select>
        <p class="field-hint">Affects the main app shell and workspace panels.</p>
      </section>

      <section class="settings-panel">
        <h2 class="panel-title">Region & currency</h2>
        <label class="field-label" for="locale">Locale</label>
        <select id="locale" v-model="form.locale" class="form-input">
          <option value="en-US">English (United States)</option>
          <option value="es-ES">Spanish (Spain)</option>
          <option value="es-MX">Spanish (Mexico)</option>
        </select>

        <label class="field-label" for="currency">Currency (display)</label>
        <select id="currency" v-model="form.currencyCode" class="form-input">
          <option value="USD">USD ($)</option>
          <option value="EUR">EUR (€)</option>
          <option value="MXN">MXN ($)</option>
        </select>
        <p class="field-hint">
          Stored for upcoming unified formatting.
          Preview:
          {{ currencyPreview }}
        </p>
      </section>

      <section class="settings-panel">
        <h2 class="panel-title">Dashboard</h2>
        <label class="field-label" for="period">Default summary period</label>
        <select id="period" v-model="form.dashboardDefaultPeriod" class="form-input">
          <option value="7">Last 7 days</option>
          <option value="30">Last 30 days</option>
          <option value="qtd">Quarter to date</option>
        </select>
        <p class="field-hint">Used when opening Summary (reload or revisit).</p>
      </section>

      <section class="settings-panel danger-zone">
        <h2 class="panel-title danger-title">Maintenance</h2>
        <p class="field-hint">
          Reset preferences to defaults (does not delete transactions on the server).
        </p>
        <button type="button" class="ghost-btn" @click="resetPrefs">
          Reset preferences
        </button>
        <p class="field-hint pushed">
          End this session locally. Your account on the server is unchanged.
        </p>
        <button type="button" class="danger-btn" @click="confirmSignOut">
          Clear session & sign out
        </button>
      </section>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import {
  readAppSettings,
  writeAppSettings,
  resetAppSettingsToDefaults,
  defaultSettings,
} from '../lib/appSettings';
import { showConfirm } from '@/lib/confirmDialog';

const router = useRouter();

const form = reactive({ ...readAppSettings() });
const saving = ref(false);
const saveMessage = ref('');

const userProfile = ref(null);

const currencyPreview = computed(() => {
  try {
    return new Intl.NumberFormat(form.locale, {
      style: 'currency',
      currency: form.currencyCode || 'USD',
      maximumFractionDigits: 2,
    }).format(1234.56);
  } catch {
    return '$1,234.56';
  }
});

function loadUser() {
  try {
    const raw = localStorage.getItem('user');
    userProfile.value = raw ? JSON.parse(raw) : null;
  } catch {
    userProfile.value = null;
  }
}

let saveToastTimer;
function flash(msg) {
  saveMessage.value = msg;
  clearTimeout(saveToastTimer);
  saveToastTimer = setTimeout(() => {
    saveMessage.value = '';
  }, 2200);
}

function save() {
  saving.value = true;
  try {
    writeAppSettings({ ...form });
    flash('Saved');
  } finally {
    saving.value = false;
  }
}

async function resetPrefs() {
  const ok = await showConfirm({
    title: 'Reset preferences',
    message: 'Are you sure you want to restore all default values on this device?',
    confirmText: 'Yes, reset',
    cancelText: 'Cancel',
    variant: 'danger',
  });
  if (!ok) return;
  resetAppSettingsToDefaults();
  Object.assign(form, { ...defaultSettings });
  flash('Preferences reset');
}

async function confirmSignOut() {
  const ok = await showConfirm({
    title: 'Log out here',
    message:
      'The token in this browser will be removed. Your local preferences are kept unless you reset them.',
    confirmText: 'Yes, log out',
    cancelText: 'Cancel',
    variant: 'danger',
  });
  if (!ok) return;
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  router.push('/');
}

function onSettingsChanged(ev) {
  if (ev?.detail && typeof ev.detail === 'object') Object.assign(form, ev.detail);
}

onMounted(() => {
  loadUser();
  Object.assign(form, readAppSettings());
  window.addEventListener('fp-settings-changed', onSettingsChanged);
});

onUnmounted(() => {
  window.removeEventListener('fp-settings-changed', onSettingsChanged);
  clearTimeout(saveToastTimer);
});
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.settings-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  font-family: manrope, sans-serif;
}

.settings-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  background-color: #f8fdf8;
  color: #1a7f3a;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  padding: 20px 30px;
  border-bottom: 1px solid #e0e8e0;
  width: 100%;
}

.settings-header-text {
  flex: 1;
  min-width: 0;
}

.settings-header h1 {
  font-size: 28px;
  font-weight: 600;
}

.settings-subtitle {
  font-size: 14px;
  color: #4a5568;
  font-weight: 400;
  line-height: 1.45;
  margin-top: 8px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
}

.save-toast {
  font-size: 14px;
  font-weight: 600;
  color: #1a7f3a;
}

.primary-btn {
  padding: 10px 22px;
  border: none;
  border-radius: 8px;
  background: #1a7f3a;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  transition:
    background 0.2s ease,
    transform 0.15s ease;
}

.primary-btn:hover:not(:disabled) {
  background: #156830;
  transform: translateY(-1px);
}

.primary-btn:disabled {
  opacity: 0.65;
  cursor: wait;
}

.settings-layout {
  flex: 1;
  width: 100%;
  min-width: 0;
  overflow-y: auto;
  padding: 24px 30px;
  background: #fafbfa;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.settings-panel {
  padding: 22px;
  border-radius: 12px;
  border: 1px solid #e0e8e0;
  background: #fff;
}

.panel-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a7f3a;
  margin-bottom: 14px;
}

.field-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
  margin-top: 14px;
}

.field-label:first-of-type {
  margin-top: 0;
}

.form-input {
  width: 100%;
  max-width: none;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #c8d9c9;
  font-size: 14px;
  font-family: inherit;
  background: #fff;
  color: #1f2937;
}

.field-hint {
  font-size: 12px;
  color: #6b7280;
  margin-top: 10px;
  line-height: 1.45;
}

.field-hint.pushed {
  margin-top: 18px;
}

.settings-card-highlight {
  margin-top: 8px;
  padding: 16px;
  border-radius: 10px;
  background: #f8fdf8;
  border: 1px solid #d8ebd8;
}

.kv-row {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  padding: 8px 0;
  border-bottom: 1px solid #e0e8e0;
  font-size: 14px;
}

.kv-row:last-child {
  border-bottom: none;
}

.kv-label {
  color: #6b7280;
  font-weight: 500;
}

.kv-value {
  color: #1f2937;
  font-weight: 600;
  text-align: right;
  word-break: break-all;
}

.empty-profile {
  font-size: 14px;
  color: #6b7280;
  margin-top: 8px;
}

.ghost-btn {
  margin-top: 12px;
  padding: 10px 18px;
  border-radius: 8px;
  border: 1px solid #1a7f3a;
  background: #fff;
  color: #1a7f3a;
  font-weight: 600;
  cursor: pointer;
  transition:
    background 0.2s ease,
    color 0.2s ease;
}

.ghost-btn:hover {
  background: #e8f5e9;
}

.danger-zone {
  border-color: #f0c2c2;
  background: #fffafa;
}

.danger-title {
  color: #c62828;
}

.danger-btn {
  margin-top: 10px;
  padding: 10px 18px;
  border-radius: 8px;
  border: 1px solid #c62828;
  background: #c62828;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  transition:
    background 0.2s ease,
    border-color 0.2s ease;
}

.danger-btn:hover {
  background: #b71c1c;
  border-color: #b71c1c;
}
</style>
