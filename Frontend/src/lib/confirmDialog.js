import { reactive } from 'vue';

/** @typedef {'danger' | 'primary' | 'neutral'} ConfirmVariant */

export const confirmDialogState = reactive({
  visible: false,
  title: '',
  message: '',
  confirmText: 'Confirm',
  cancelText: 'Cancel',
  /** danger = destructive (red), primary = create/save (green), neutral = secondary action */
  variant: /** @type {ConfirmVariant} */ ('danger'),
});

/** @type {((value: boolean) => void) | null} */
let pendingResolve = null;

/**
 * @param {object} [options]
 * @param {string} [options.title]
 * @param {string} [options.message]
 * @param {string} [options.confirmText]
 * @param {string} [options.cancelText]
 * @param {ConfirmVariant} [options.variant]
 * @returns {Promise<boolean>}
 */
export function showConfirm(options = {}) {
  return new Promise((resolve) => {
    if (pendingResolve) {
      pendingResolve(false);
      pendingResolve = null;
    }
    confirmDialogState.title = options.title ?? 'Confirm';
    confirmDialogState.message = options.message ?? '';
    confirmDialogState.confirmText = options.confirmText ?? 'Confirm';
    confirmDialogState.cancelText = options.cancelText ?? 'Cancel';
    confirmDialogState.variant = options.variant ?? 'danger';
    confirmDialogState.visible = true;
    pendingResolve = resolve;
  });
}

/**
 * @param {boolean} confirmed
 */
export function completeConfirm(confirmed) {
  confirmDialogState.visible = false;
  if (pendingResolve) {
    pendingResolve(confirmed);
    pendingResolve = null;
  }
}
