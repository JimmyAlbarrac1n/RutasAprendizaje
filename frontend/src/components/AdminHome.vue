<template>
  <div class="admin-home">
    <h1>Bienvenido, Administrador</h1>
    <div class="admin-menu">
      <button @click="goTo('usuarios')">CRUD de Usuarios</button>
      <button @click="goTo('etiquetas')">CRUD de Etiquetas</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();

function goTo(option) {
  if (option === 'usuarios') {
    router.push('/admin/usuarios');
  } else if (option === 'etiquetas') {
    router.push('/admin/etiquetas');
  }
}
</script>

<style scoped>
.admin-home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}
.admin-home h1 {
  color: #39ff14;
  margin-bottom: 2rem;
}
.admin-menu {
  display: flex;
  gap: 2rem;
}
button {
  background: linear-gradient(90deg, #39ff14 60%, #ff9100 100%);
  color: #181818;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background 0.2s;
}
button:hover {
  background: linear-gradient(90deg, #ff9100 60%, #39ff14 100%);
}
</style> 