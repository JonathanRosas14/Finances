/** App-wide preferences persisted in localStorage (no backend yet). */

export const STORAGE_KEY = 'fp_settings';

export const defaultSettings = {
  theme: 'light',
  /** BCP 47 tag; used for date/number previews and html lang hint */
  locale: 'en-US',
  /** Display-only label for money formatting across the UI */
  currencyCode: 'USD',
  dashboardDefaultPeriod: '30',
};

/**
 * @returns {typeof defaultSettings & Record<string, unknown>}
 */
export function readAppSettings() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { ...defaultSettings };
    const parsed = JSON.parse(raw);
    return { ...defaultSettings, ...parsed };
  } catch {
    return { ...defaultSettings };
  }
}

/**
 * @param {Partial<typeof defaultSettings>} patch
 */
export function writeAppSettings(patch) {
  const next = { ...readAppSettings(), ...patch };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
  applySettingsToDocument(next);
  window.dispatchEvent(new CustomEvent('fp-settings-changed', { detail: next }));
}

export function resetAppSettingsToDefaults() {
  localStorage.removeItem(STORAGE_KEY);
  applySettingsToDocument({ ...defaultSettings });
  window.dispatchEvent(
    new CustomEvent('fp-settings-changed', { detail: { ...defaultSettings } }),
  );
}

/**
 * @param {typeof defaultSettings} s
 */
export function applySettingsToDocument(s) {
  const root = document.documentElement;
  root.dataset.theme = s.theme === 'dark' ? 'dark' : 'light';
  const lang = String(s.locale || 'en-US').split('-')[0] || 'en';
  root.lang = lang;
}

export function applyStoredSettingsOnBoot() {
  applySettingsToDocument(readAppSettings());
}
