<template>
  <div class="centered-content">
    <router-view />
  </div>
</template>

<script setup>
// No se necesita lógica aquí por ahora
</script>

<style scoped>
body {
  background: #181818;
}
.centered-content {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
