<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="sidebar-title">Panel Admin</div>
      <nav>
        <ul>
          <li :class="{active: activeTab === 'usuarios'}" @click="activeTab = 'usuarios'">
            <span>👤</span> Usuarios
          </li>
          <li :class="{active: activeTab === 'etiquetas'}" @click="activeTab = 'etiquetas'">
            <span>🏷️</span> Etiquetas
          </li>
        </ul>
      </nav>
      <button class="btn-logout" @click="logout">Cerrar sesión</button>
    </aside>
    <main class="main-panel">
      <div class="panel-content">
        <UserCrud v-if="activeTab === 'usuarios'" />
        <TagCrud v-else />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import UserCrud from './UserCrud.vue';
import TagCrud from './TagCrud.vue';

const activeTab = ref('usuarios');
const router = useRouter();

async function logout() {
  try {
    await axios.post('http://localhost:5000/auth/logout', {}, { withCredentials: true });
  } catch (e) {}
  router.push('/login');
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  width: 100vw;
  margin: 0;
  background: #fff;
}
.sidebar {
  width: 220px;
  background: #181818;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 2rem 1rem 1rem 1rem;
  color: #39ff14;
  min-height: 100vh;
  border-radius: 0;
  box-shadow: none;
}
.sidebar-title {
  font-size: 1.3rem;
  font-weight: bold;
  color: #ff9100;
  margin-bottom: 2.5rem;
  letter-spacing: 1px;
}
.sidebar nav ul {
  list-style: none;
  padding: 0;
  width: 100%;
}
.sidebar nav li {
  padding: 0.8rem 1rem;
  margin-bottom: 1rem;
  border-radius: 8px;
  cursor: pointer;
  color: #39ff14;
  font-weight: bold;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 0.7rem;
  transition: background 0.2s, color 0.2s;
}
.sidebar nav li.active, .sidebar nav li:hover {
  background: linear-gradient(90deg, #39ff14 60%, #ff9100 100%);
  color: #181818;
}
.main-panel {
  flex: 1;
  background: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 2.5rem 2rem 2rem 2rem;
  min-height: 100vh;
  border-radius: 0;
  box-shadow: none;
}
.panel-content {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
}
.btn-logout {
  margin-top: 2rem;
  width: 100%;
  background: linear-gradient(90deg, #39ff14 60%, #ff9100 100%);
  color: #181818;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  padding: 0.8rem 0;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-logout:hover {
  background: linear-gradient(90deg, #ff9100 60%, #39ff14 100%);
}
@media (max-width: 900px) {
  .admin-layout {
    flex-direction: column;
    max-width: 100vw;
  }
  .sidebar {
    width: 100%;
    min-height: auto;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    padding: 1rem 0.5rem;
    border-radius: 0;
  }
  .sidebar nav ul {
    display: flex;
    flex-direction: row;
    gap: 1rem;
    width: auto;
  }
  .sidebar nav li {
    margin-bottom: 0;
  }
  .main-panel {
    border-radius: 0;
    padding: 1.5rem 0.5rem;
    min-height: 60vh;
  }
}
</style> 