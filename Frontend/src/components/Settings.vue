<template>
  <div class="settings-container">
    <header class="settings-header">
      <div>
        <p class="eyebrow">Preferences</p>
        <h1>Settings</h1>
        <p class="settings-subtitle">
          Control how Finances Pro looks, formats money and opens your dashboard.
        </p>
      </div>

      <div class="header-actions">
        <span v-if="saveMessage" class="save-toast">{{ saveMessage }}</span>
        <button type="button" class="ghost-btn" :disabled="!hasChanges" @click="discardChanges">
          Discard
        </button>
        <button type="button" class="primary-btn" :disabled="saving || !hasChanges" @click="save">
          {{ saving ? 'Saving...' : 'Save changes' }}
        </button>
      </div>
    </header>

    <main class="settings-content">
      <section class="settings-panel account-panel">
        <div class="panel-heading">
          <div>
            <h2>Account</h2>
            <p>Current session information stored in this browser.</p>
          </div>
          <span class="status-pill">{{ userProfile ? 'Signed in' : 'No session' }}</span>
        </div>

        <div v-if="userProfile" class="profile-card">
          <div class="avatar">{{ userInitials }}</div>
          <div class="profile-main">
            <strong>{{ userProfile.username || userProfile.email || 'User' }}</strong>
            <span>{{ userProfile.email || 'No email available' }}</span>
          </div>
        </div>

        <div class="kv-grid">
          <div class="kv-item">
            <span>Username</span>
            <strong>{{ userProfile?.username || '-' }}</strong>
          </div>
          <div class="kv-item">
            <span>Provider</span>
            <strong>{{ userProfile?.provider || 'local' }}</strong>
          </div>
          <div class="kv-item">
            <span>Session</span>
            <strong>{{ hasToken ? 'Active' : 'Missing token' }}</strong>
          </div>
        </div>
      </section>

      <section class="settings-panel">
        <div class="panel-heading">
          <div>
            <h2>Appearance</h2>
            <p>Choose the app theme used by the main workspace.</p>
          </div>
        </div>

        <div class="theme-grid">
          <label
            v-for="option in themeOptions"
            :key="option.value"
            class="theme-option"
            :class="{ selected: form.theme === option.value }"
          >
            <input v-model="form.theme" type="radio" name="theme" :value="option.value" />
            <span class="theme-preview" :class="option.value">
              <i></i>
              <i></i>
              <i></i>
            </span>
            <strong>{{ option.label }}</strong>
            <small>{{ option.description }}</small>
          </label>
        </div>
      </section>

      <section class="settings-panel">
        <div class="panel-heading">
          <div>
            <h2>Region & currency</h2>
            <p>Used for dashboard amounts and date previews.</p>
          </div>
        </div>

        <div class="form-grid">
          <label class="field-group" for="locale">
            <span>Locale</span>
            <select id="locale" v-model="form.locale" class="form-input">
              <option value="en-US">English (United States)</option>
              <option value="es-ES">Spanish (Spain)</option>
              <option value="es-MX">Spanish (Mexico)</option>
            </select>
          </label>

          <label class="field-group" for="currency">
            <span>Currency</span>
            <select id="currency" v-model="form.currencyCode" class="form-input">
              <option value="USD">USD ($)</option>
              <option value="EUR">EUR (€)</option>
              <option value="MXN">MXN ($)</option>
              <option value="COP">COP ($)</option>
            </select>
          </label>
        </div>

        <div class="preview-strip">
          <div>
            <span>Money preview</span>
            <strong>{{ currencyPreview }}</strong>
          </div>
          <div>
            <span>Date preview</span>
            <strong>{{ datePreview }}</strong>
          </div>
        </div>
      </section>

      <section class="settings-panel">
        <div class="panel-heading">
          <div>
            <h2>Dashboard</h2>
            <p>Default period for the Summary page.</p>
          </div>
        </div>

        <div class="period-grid">
          <label
            v-for="option in periodOptions"
            :key="option.value"
            class="period-option"
            :class="{ selected: form.dashboardDefaultPeriod === option.value }"
          >
            <input
              v-model="form.dashboardDefaultPeriod"
              type="radio"
              name="dashboard-period"
              :value="option.value"
            />
            <strong>{{ option.label }}</strong>
            <small>{{ option.description }}</small>
          </label>
        </div>
      </section>

      <section class="settings-panel danger-zone">
        <div class="panel-heading">
          <div>
            <h2>Maintenance</h2>
            <p>Local actions only. Server transactions are not deleted.</p>
          </div>
        </div>

        <div class="maintenance-grid">
          <div class="maintenance-card">
            <strong>Reset preferences</strong>
            <span>Restore theme, currency and dashboard period to defaults.</span>
            <button type="button" class="outline-danger-btn" @click="resetPrefs">
              Reset preferences
            </button>
          </div>

          <div class="maintenance-card critical">
            <strong>Clear session</strong>
            <span>Remove this browser token and return to the landing page.</span>
            <button type="button" class="danger-btn" @click="confirmSignOut">
              Clear session & sign out
            </button>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, reactive, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import {
  applySettingsToDocument,
  defaultSettings,
  readAppSettings,
  resetAppSettingsToDefaults,
  writeAppSettings,
} from '../lib/appSettings';
import { showConfirm } from '../lib/confirmDialog';

const router = useRouter();

const themeOptions = [
  { value: 'light', label: 'Light', description: 'Clean white workspace' },
  { value: 'dark', label: 'Dark', description: 'Reduced brightness mode' },
];

const periodOptions = [
  { value: '7', label: '7 days', description: 'Short weekly overview' },
  { value: '30', label: '30 days', description: 'Recommended monthly view' },
  { value: '90', label: '90 days', description: 'Quarterly movement' },
  { value: 'qtd', label: 'Quarter', description: 'Quarter to date' },
  { value: 'all', label: 'All time', description: 'Full account history' },
];

const form = reactive({ ...readAppSettings() });
const savedSettings = ref({ ...readAppSettings() });
const userProfile = ref(null);
const hasToken = ref(false);
const saving = ref(false);
const saveMessage = ref('');

const hasChanges = computed(() => {
  return JSON.stringify(form) !== JSON.stringify(savedSettings.value);
});

const userInitials = computed(() => {
  const source = userProfile.value?.username || userProfile.value?.email || 'FP';
  return source
    .split(/[\s@._-]+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join('') || 'FP';
});

const currencyPreview = computed(() => {
  try {
    return new Intl.NumberFormat(form.locale, {
      style: 'currency',
      currency: form.currencyCode || defaultSettings.currencyCode,
      maximumFractionDigits: 2,
    }).format(2450.75);
  } catch {
    return '$2,450.75';
  }
});

const datePreview = computed(() => {
  try {
    return new Intl.DateTimeFormat(form.locale, {
      weekday: 'short',
      month: 'short',
      day: '2-digit',
      year: 'numeric',
    }).format(new Date());
  } catch {
    return new Date().toLocaleDateString('en-US');
  }
});

watch(
  () => ({ theme: form.theme, locale: form.locale }),
  () => {
    applySettingsToDocument({ ...savedSettings.value, ...form });
  },
  { deep: true },
);

function loadUser() {
  try {
    const raw = localStorage.getItem('user');
    userProfile.value = raw ? JSON.parse(raw) : null;
  } catch {
    userProfile.value = null;
  }

  hasToken.value = Boolean(localStorage.getItem('token'));
}

let saveToastTimer;
function flash(message) {
  saveMessage.value = message;
  clearTimeout(saveToastTimer);
  saveToastTimer = setTimeout(() => {
    saveMessage.value = '';
  }, 2200);
}

function save() {
  saving.value = true;
  try {
    writeAppSettings({ ...form });
    savedSettings.value = { ...form };
    flash('Settings saved');
  } finally {
    saving.value = false;
  }
}

function discardChanges() {
  Object.assign(form, savedSettings.value);
  applySettingsToDocument(savedSettings.value);
  flash('Changes discarded');
}

async function resetPrefs() {
  const ok = await showConfirm({
    title: 'Reset preferences',
    message: 'Restore the default theme, currency, locale and dashboard period?',
    confirmText: 'Reset',
    cancelText: 'Cancel',
    variant: 'danger',
  });
  if (!ok) return;

  resetAppSettingsToDefaults();
  savedSettings.value = { ...defaultSettings };
  Object.assign(form, defaultSettings);
  flash('Preferences reset');
}

async function confirmSignOut() {
  const ok = await showConfirm({
    title: 'Clear session',
    message: 'Your token and local user data will be removed from this browser.',
    confirmText: 'Sign out',
    cancelText: 'Cancel',
    variant: 'danger',
  });
  if (!ok) return;

  localStorage.removeItem('token');
  localStorage.removeItem('user');
  router.push('/');
}

function onSettingsChanged(event) {
  if (!event?.detail || typeof event.detail !== 'object') return;
  savedSettings.value = { ...defaultSettings, ...event.detail };
  Object.assign(form, savedSettings.value);
}

onMounted(() => {
  loadUser();
  savedSettings.value = { ...readAppSettings() };
  Object.assign(form, savedSettings.value);
  window.addEventListener('fp-settings-changed', onSettingsChanged);
});

onUnmounted(() => {
  if (hasChanges.value) applySettingsToDocument(savedSettings.value);
  window.removeEventListener('fp-settings-changed', onSettingsChanged);
  clearTimeout(saveToastTimer);
});
</script>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.settings-container {
  color: #1f2933;
  display: flex;
  flex-direction: column;
  font-family: manrope, sans-serif;
  height: 100%;
  width: 100%;
}

.settings-header {
  align-items: center;
  background: linear-gradient(135deg, #f8fdf8 0%, #eef9ef 100%);
  border: 1px solid #e0e8e0;
  border-radius: 18px;
  box-shadow: 0 10px 30px rgba(26, 127, 58, 0.08);
  display: flex;
  gap: 20px;
  justify-content: space-between;
  padding: 24px 28px;
  width: 100%;
}

.eyebrow {
  color: #1a7f3a;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.12em;
  margin-bottom: 6px;
  text-transform: uppercase;
}

.settings-header h1 {
  color: #14532d;
  font-size: 30px;
  font-weight: 800;
}

.settings-subtitle {
  color: #667085;
  font-size: 14px;
  margin-top: 6px;
}

.header-actions {
  align-items: center;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: flex-end;
}

.save-toast {
  color: #1a7f3a;
  font-size: 13px;
  font-weight: 800;
}

.settings-content {
  display: grid;
  flex: 1;
  gap: 18px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  overflow-y: auto;
  padding: 24px 0 0;
}

.settings-panel {
  background: #ffffff;
  border: 1px solid #e6efe7;
  border-radius: 18px;
  box-shadow: 0 12px 28px rgba(15, 23, 42, 0.06);
  padding: 22px;
}

.account-panel,
.danger-zone {
  grid-column: span 2;
}

.panel-heading {
  align-items: flex-start;
  display: flex;
  gap: 14px;
  justify-content: space-between;
  margin-bottom: 18px;
}

.panel-heading h2 {
  color: #14532d;
  font-size: 20px;
  margin-bottom: 4px;
}

.panel-heading p,
.theme-option small,
.period-option small,
.maintenance-card span,
.profile-main span {
  color: #667085;
  font-size: 13px;
  line-height: 1.45;
}

.status-pill {
  background: #e8f5e9;
  border-radius: 999px;
  color: #1a7f3a;
  font-size: 12px;
  font-weight: 800;
  padding: 7px 12px;
  white-space: nowrap;
}

.profile-card {
  align-items: center;
  background: #f8fdf8;
  border: 1px solid #d8ebd8;
  border-radius: 16px;
  display: flex;
  gap: 14px;
  margin-bottom: 16px;
  padding: 16px;
}

.avatar {
  align-items: center;
  background: linear-gradient(135deg, #1a7f3a, #2ca84f);
  border-radius: 16px;
  color: #ffffff;
  display: flex;
  font-weight: 900;
  height: 52px;
  justify-content: center;
  letter-spacing: 0.04em;
  width: 52px;
}

.profile-main {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.profile-main strong,
.kv-item strong,
.theme-option strong,
.period-option strong,
.maintenance-card strong,
.preview-strip strong {
  color: #1f2933;
}

.kv-grid,
.form-grid,
.preview-strip,
.maintenance-grid {
  display: grid;
  gap: 14px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.kv-item,
.preview-strip div {
  background: #fbfefb;
  border: 1px solid #e6efe7;
  border-radius: 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 14px;
}

.kv-item span,
.preview-strip span,
.field-group > span {
  color: #667085;
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.theme-grid,
.period-grid {
  display: grid;
  gap: 14px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.period-grid {
  grid-template-columns: repeat(5, minmax(0, 1fr));
}

.theme-option,
.period-option {
  border: 1px solid #e0e8e0;
  border-radius: 16px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px;
  transition:
    border-color 0.18s ease,
    box-shadow 0.18s ease,
    transform 0.18s ease;
}

.theme-option input,
.period-option input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.theme-option.selected,
.period-option.selected {
  border-color: #1a7f3a;
  box-shadow: 0 10px 24px rgba(26, 127, 58, 0.12);
  transform: translateY(-1px);
}

.theme-preview {
  border-radius: 14px;
  display: grid;
  gap: 8px;
  grid-template-columns: 0.8fr 1fr;
  height: 86px;
  padding: 12px;
}

.theme-preview.light {
  background: #f8fdf8;
  border: 1px solid #d8ebd8;
}

.theme-preview.dark {
  background: #0f1a13;
  border: 1px solid #243529;
}

.theme-preview i {
  border-radius: 8px;
  display: block;
}

.theme-preview.light i {
  background: #ffffff;
}

.theme-preview.light i:first-child {
  background: #1a7f3a;
  grid-row: span 2;
}

.theme-preview.dark i {
  background: #1d2c22;
}

.theme-preview.dark i:first-child {
  background: #7fd49a;
  grid-row: span 2;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.form-input {
  background: #ffffff;
  border: 1px solid #c8d9c9;
  border-radius: 12px;
  color: #1f2937;
  font: inherit;
  min-height: 44px;
  padding: 0 12px;
  width: 100%;
}

.preview-strip {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  margin-top: 16px;
}

.maintenance-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.maintenance-card {
  background: #fffafa;
  border: 1px solid #f0c2c2;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 18px;
}

.maintenance-card.critical {
  background: #fff5f5;
}

.primary-btn,
.ghost-btn,
.danger-btn,
.outline-danger-btn {
  border-radius: 12px;
  cursor: pointer;
  font: inherit;
  font-weight: 800;
  min-height: 42px;
  padding: 0 16px;
  transition:
    opacity 0.16s ease,
    transform 0.16s ease,
    background 0.16s ease;
}

.primary-btn {
  background: #1a7f3a;
  border: 1px solid #1a7f3a;
  color: #ffffff;
}

.ghost-btn {
  background: #ffffff;
  border: 1px solid #c8d9c9;
  color: #1a7f3a;
}

.danger-btn,
.outline-danger-btn {
  margin-top: auto;
}

.danger-btn {
  background: #c62828;
  border: 1px solid #c62828;
  color: #ffffff;
}

.outline-danger-btn {
  background: #ffffff;
  border: 1px solid #c62828;
  color: #c62828;
}

.primary-btn:hover:not(:disabled),
.ghost-btn:hover:not(:disabled),
.danger-btn:hover:not(:disabled),
.outline-danger-btn:hover:not(:disabled) {
  transform: translateY(-1px);
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

@media (max-width: 1100px) {
  .settings-content,
  .account-panel,
  .danger-zone {
    grid-template-columns: 1fr;
  }

  .account-panel,
  .danger-zone {
    grid-column: span 1;
  }

  .period-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .settings-header,
  .header-actions {
    align-items: stretch;
    flex-direction: column;
  }

  .header-actions {
    width: 100%;
  }

  .header-actions button {
    width: 100%;
  }

  .kv-grid,
  .theme-grid,
  .form-grid,
  .preview-strip,
  .maintenance-grid,
  .period-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 520px) {
  .settings-header,
  .settings-panel {
    border-radius: 14px;
    padding: 18px;
  }

  .settings-header h1 {
    font-size: 24px;
  }

  .panel-heading {
    flex-direction: column;
  }
}
</style>
