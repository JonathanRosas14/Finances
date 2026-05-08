<template>
  <div id="app">
    <router-view />
    <ConfirmDialogHost />
  </div>
</template>
<script setup>
import ConfirmDialogHost from './components/ConfirmDialogHost.vue'
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  width: 100%;
  min-height: 100vh;
  background-color: #0c140f;
  font-family: manrope, sans-serif;
}
</style>
