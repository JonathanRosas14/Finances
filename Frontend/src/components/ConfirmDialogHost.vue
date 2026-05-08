<script setup>
import { onMounted, onUnmounted, watch } from 'vue';
import { confirmDialogState, completeConfirm } from '@/lib/confirmDialog';

function onBackdrop() {
  completeConfirm(false);
}

function onConfirm() {
  completeConfirm(true);
}

function onCancel() {
  completeConfirm(false);
}

/** @param {KeyboardEvent} e */
function onKeydown(e) {
  if (!confirmDialogState.visible) return;
  if (e.key === 'Escape') {
    e.preventDefault();
    completeConfirm(false);
  }
}

watch(
  () => confirmDialogState.visible,
  (open) => {
    document.body.style.overflow = open ? 'hidden' : '';
  },
);

onMounted(() => {
  window.addEventListener('keydown', onKeydown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown);
  document.body.style.overflow = '';
});
</script>

<template>
  <Teleport to="body">
    <Transition name="fp-confirm">
      <div
        v-if="confirmDialogState.visible"
        class="fp-confirm-backdrop"
        role="presentation"
        @click.self="onBackdrop"
      >
        <div
          class="fp-confirm-dialog"
          role="alertdialog"
          aria-modal="true"
          :aria-labelledby="'fp-confirm-title'"
          @click.stop
        >
          <h2 id="fp-confirm-title" class="fp-confirm-title">
            {{ confirmDialogState.title }}
          </h2>
          <p v-if="confirmDialogState.message" class="fp-confirm-msg">
            {{ confirmDialogState.message }}
          </p>
          <p class="fp-confirm-hint">You can cancel with Escape or by clicking outside the dialog.</p>
          <div class="fp-confirm-actions">
            <button type="button" class="fp-confirm-btn fp-confirm-cancel" @click="onCancel">
              {{ confirmDialogState.cancelText }}
            </button>
            <button
              type="button"
              class="fp-confirm-btn fp-confirm-ok"
              :class="'fp-confirm-' + confirmDialogState.variant"
              @click="onConfirm"
            >
              {{ confirmDialogState.confirmText }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.fp-confirm-backdrop {
  position: fixed;
  inset: 0;
  z-index: 100000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: rgba(15, 22, 18, 0.55);
  backdrop-filter: blur(3px);
}

.fp-confirm-dialog {
  width: 100%;
  max-width: 432px;
  background: #fff;
  border-radius: 14px;
  box-shadow:
    0 24px 48px rgba(0, 0, 0, 0.14),
    0 4px 12px rgba(26, 127, 58, 0.08);
  border: 1px solid #e0e8e0;
  padding: 26px 28px 24px;
  font-family:
    manrope,
    system-ui,
    sans-serif;
}

.fp-confirm-title {
  margin: 0 0 12px;
  font-size: 1.35rem;
  font-weight: 700;
  color: #143d24;
  line-height: 1.25;
}

.fp-confirm-msg {
  margin: 0 0 10px;
  font-size: 15px;
  line-height: 1.5;
  color: #374151;
  white-space: pre-wrap;
}

.fp-confirm-hint {
  margin: 0 0 22px;
  font-size: 12px;
  color: #6b7280;
  line-height: 1.4;
}

.fp-confirm-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: flex-end;
}

.fp-confirm-btn {
  cursor: pointer;
  font-family: inherit;
  font-weight: 600;
  font-size: 14px;
  padding: 11px 20px;
  border-radius: 9px;
  border: none;
  min-width: 112px;
  transition:
    transform 0.15s ease,
    box-shadow 0.15s ease,
    background 0.15s ease;
}

.fp-confirm-btn:active:not(:disabled) {
  transform: scale(0.98);
}

.fp-confirm-cancel {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #e5e7eb;
}

.fp-confirm-cancel:hover {
  background: #e8f5e9;
  border-color: #c8dcd0;
  color: #156830;
}

.fp-confirm-ok.fp-confirm-primary {
  background: #1a7f3a;
  color: #fff;
  box-shadow: 0 4px 12px rgba(26, 127, 58, 0.28);
}

.fp-confirm-ok.fp-confirm-primary:hover {
  background: #156830;
}

.fp-confirm-ok.fp-confirm-danger {
  background: #c62828;
  color: #fff;
  box-shadow: 0 4px 12px rgba(198, 40, 40, 0.25);
}

.fp-confirm-ok.fp-confirm-danger:hover {
  background: #b71c1c;
}

.fp-confirm-ok.fp-confirm-neutral {
  background: #37474f;
  color: #fff;
  box-shadow: 0 4px 12px rgba(55, 71, 79, 0.2);
}

.fp-confirm-ok.fp-confirm-neutral:hover {
  background: #263238;
}

.fp-confirm-enter-active,
.fp-confirm-leave-active {
  transition: opacity 0.22s ease;
}

.fp-confirm-enter-active .fp-confirm-dialog,
.fp-confirm-leave-active .fp-confirm-dialog {
  transition:
    transform 0.22s ease,
    opacity 0.22s ease;
}

.fp-confirm-enter-from,
.fp-confirm-leave-to {
  opacity: 0;
}

.fp-confirm-enter-from .fp-confirm-dialog,
.fp-confirm-leave-to .fp-confirm-dialog {
  transform: scale(0.94) translateY(8px);
  opacity: 0;
}
</style>
