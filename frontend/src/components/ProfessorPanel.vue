<template>
  <div class="professor-layout">
    <aside class="sidebar">
      <div class="sidebar-title">Panel Profesor</div>
      <nav>
        <ul>
          <li :class="{active: activeTab === 'rutas'}" @click="goToRutas">
            <span>🗂️</span> Rutas de aprendizaje
          </li>
          <li :class="{active: activeTab === 'material'}" @click="activeTab = 'material'">
            <span>➕</span> Añadir material
          </li>
        </ul>
      </nav>
      <button class="btn-logout" @click="logout">Cerrar sesión</button>
    </aside>
    <main class="main-panel">
      <div class="panel-content">
        <template v-if="activeTab === 'rutas' && !selectedRoute">
          <h2 class="main-title">Mis rutas de aprendizaje</h2>
          <div class="routes-list-compact">
            <div class="route-card-compact" v-for="route in mockRoutes" :key="route._id" @click="selectRoute(route)">
              <div class="route-title">{{ route.name }}</div>
              <div class="route-desc">{{ route.description }}</div>
              <div class="route-info">
                <span>{{ route.materials.length }} materiales</span>
                <span>•</span>
                <span>{{ route.updatedAt }}</span>
              </div>
            </div>
          </div>
        </template>
        <template v-else-if="activeTab === 'rutas' && selectedRoute">
          <button class="btn-back" @click="selectedRoute = null">← Volver a rutas</button>
          <h2 class="main-title">{{ selectedRoute.name }}</h2>
          <div class="route-desc">{{ selectedRoute.description }}</div>
          <div class="materials-grid">
            <div class="material-card" v-for="mat in selectedRoute.materials" :key="mat._id">
              <div class="material-title">{{ mat.title }}</div>
              <div class="material-tags">
                <span v-for="tag in mat.tags.slice(0,5)" :key="tag" class="tag">{{ tag }}</span>
              </div>
              <div class="material-info">
                <span>Dificultad: {{ mat.difficulty }}</span>
                <span>•</span>
                <span>{{ mat.date }}</span>
              </div>
            </div>
          </div>
        </template>
        <template v-else>
          <h2 class="main-title">Añadir material</h2>
          <div class="add-material-placeholder">
            <p>Aquí irá el formulario para añadir material y se mostrarán las etiquetas creadas por el administrador.</p>
          </div>
        </template>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
const activeTab = ref('rutas');
const selectedRoute = ref(null);

// Mock de rutas y materiales para estructura visual
const mockRoutes = [
  {
    _id: '1',
    name: 'Desarrollo Web con Flask y Vue',
    description: 'Ruta para aprender a crear apps web modernas.',
    updatedAt: '2024-06-10',
    materials: [
      { _id: 'm1', title: 'Introducción a Flask', tags: ['Flask'], difficulty: 1, date: '2024-06-10' },
      { _id: 'm2', title: 'Frontend con Vue', tags: ['Vue'], difficulty: 2, date: '2024-06-11' }
    ]
  },
  {
    _id: '2',
    name: 'Machine Learning Básico',
    description: 'Conceptos y ejemplos de ML en Python.',
    updatedAt: '2024-06-09',
    materials: [
      { _id: 'm3', title: 'Conceptos de ML', tags: ['ML'], difficulty: 1, date: '2024-06-09' }
    ]
  }
];

function logout() {
  window.location.href = '/login';
}
function selectRoute(route) {
  selectedRoute.value = route;
}
function goToRutas() {
  activeTab.value = 'rutas';
  selectedRoute.value = null;
}
</script>

<style scoped>
.professor-layout {
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
}
.sidebar-title {
  font-size: 1.3rem;
  font-weight: bold;
  color: #39ff14;
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
.main-panel {
  flex: 1;
  background: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 2.5rem 2rem 2rem 2rem;
  min-height: 100vh;
}
.panel-content {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
}
.main-title {
  color: #181818;
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
}
.routes-list-compact {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: flex-start;
}
.route-card-compact {
  background: #fff;
  border: 2px solid #39ff14;
  border-radius: 10px;
  box-shadow: 0 0 8px #39ff1433;
  padding: 1rem 1.2rem;
  min-width: 220px;
  max-width: 260px;
  flex: 1 1 220px;
  margin-bottom: 1rem;
  cursor: pointer;
  transition: box-shadow 0.2s, border 0.2s;
}
.route-card-compact:hover {
  box-shadow: 0 0 16px #ff9100aa;
  border: 2px solid #ff9100;
}
.route-title {
  color: #39ff14;
  font-weight: bold;
  font-size: 1.1rem;
  margin-bottom: 0.3rem;
}
.route-desc {
  color: #181818;
  font-size: 0.98rem;
  margin-bottom: 0.7rem;
}
.route-info {
  color: #ff9100;
  font-size: 0.95rem;
  display: flex;
  gap: 0.5rem;
  align-items: center;
}
.btn-back {
  background: none;
  color: #ff9100;
  border: 1.5px solid #ff9100;
  border-radius: 6px;
  padding: 0.5rem 1.2rem;
  font-size: 1rem;
  cursor: pointer;
  margin-bottom: 1.5rem;
  font-weight: bold;
  transition: background 0.2s, color 0.2s;
}
.btn-back:hover {
  background: #ff9100;
  color: #fff;
}
.materials-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: flex-start;
}
.material-card {
  background: #f7f7f7;
  border: 1.5px solid #ff9100;
  border-radius: 8px;
  padding: 1rem 1.2rem;
  min-width: 220px;
  max-width: 260px;
  flex: 1 1 220px;
  margin-bottom: 1rem;
}
.material-title {
  color: #ff9100;
  font-weight: bold;
  font-size: 1.08rem;
  margin-bottom: 0.3rem;
}
.material-tags {
  margin: 0.3rem 0 0.5rem 0;
}
.material-tags .tag {
  background: #fff;
  color: #ff9100;
  border: 1px solid #ff9100;
}
.material-info {
  font-size: 0.95rem;
  color: #181818;
  display: flex;
  gap: 0.5rem;
  align-items: center;
}
.add-material-placeholder {
  background: #f7f7f7;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  color: #181818;
  font-size: 1.1rem;
}
@media (max-width: 900px) {
  .professor-layout {
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
    padding: 1.5rem 0.5rem;
    min-height: 60vh;
  }
  .routes-list-compact, .materials-grid {
    flex-direction: column;
    gap: 1rem;
  }
}
</style> 