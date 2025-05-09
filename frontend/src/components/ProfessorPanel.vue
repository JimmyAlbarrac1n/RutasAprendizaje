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
          <form class="material-form" @submit.prevent>
            <div class="form-row">
              <div class="form-group">
                <label>Título</label>
                <input v-model="materialForm.title" type="text" required />
              </div>
              <div class="form-group">
                <label>Descripción</label>
                <input v-model="materialForm.description" type="text" required />
              </div>
            </div>
            <div class="form-group">
              <label>Seleccione las etiquetas que describen el material</label>
              <multiselect
                v-model="materialForm.tags"
                :options="etiquetas"
                :multiple="true"
                :close-on-select="false"
                :clear-on-select="false"
                :preserve-search="true"
                placeholder="Buscar y seleccionar etiquetas"
                label="name"
                track-by="_id"
              />
            </div>
            <div class="form-group">
              <label>Seleccione el número de dificultad (1 la más baja)</label>
              <div class="difficulty-row">
                <label v-for="n in 5" :key="n">
                  <input type="radio" v-model="materialForm.difficulty" :value="n" required /> {{ n }}
                </label>
              </div>
            </div>
            <div class="form-group">
              <label>Seleccione etiquetas de conocimientos previos necesarios</label>
              <multiselect
                v-model="materialForm.prerequisites"
                :options="etiquetas"
                :multiple="true"
                :close-on-select="false"
                :clear-on-select="false"
                :preserve-search="true"
                placeholder="Buscar y seleccionar etiquetas"
                label="name"
                track-by="_id"
              />
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Link del recurso</label>
                <input v-model="materialForm.link" type="url" placeholder="https://..." />
              </div>
              <div class="form-group">
                <label>Subir archivo</label>
                <input type="file" @change="onFileChange" />
              </div>
            </div>
            <div class="form-group">
              <label>Seleccione la ruta a la que pertenecerá</label>
              <multiselect
                v-model="materialForm.route"
                :options="rutas"
                :multiple="false"
                placeholder="Buscar o crear ruta"
                label="name"
                track-by="_id"
                :allow-empty="false"
                :taggable="true"
                @tag="addNewRoute"
              />
            </div>
            <div class="form-actions">
              <button class="btn-neon" type="submit">Crear material</button>
            </div>
          </form>
        </template>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Multiselect from 'vue-multiselect';
import axios from 'axios';
import 'vue-multiselect/dist/vue-multiselect.min.css';

const activeTab = ref('rutas');
const selectedRoute = ref(null);

const etiquetas = ref([]);
const rutas = ref([]);
const loadingTags = ref(false);
const loadingRutas = ref(false);
const creatingRoute = ref(false);
const routeError = ref('');

const materialForm = ref({
  title: '',
  description: '',
  tags: [],
  difficulty: '',
  prerequisites: [],
  link: '',
  file: null,
  route: null
});

async function fetchEtiquetas() {
  loadingTags.value = true;
  try {
    const res = await axios.get('http://localhost:5000/tags/', { withCredentials: true });
    etiquetas.value = res.data.data || [];
  } catch (e) {
    etiquetas.value = [];
  }
  loadingTags.value = false;
}

async function fetchRutas() {
  loadingRutas.value = true;
  try {
    const res = await axios.get('http://localhost:5000/routes/', { withCredentials: true });
    rutas.value = res.data.data || [];
  } catch (e) {
    rutas.value = [];
  }
  loadingRutas.value = false;
}

onMounted(() => {
  fetchEtiquetas();
  fetchRutas();
});

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
function onFileChange(e) {
  materialForm.value.file = e.target.files[0];
}

async function addNewRoute(newRouteName) {
  routeError.value = '';
  if (!newRouteName) return;
  creatingRoute.value = true;
  try {
    const res = await axios.post('http://localhost:5000/routes/', {
      name: newRouteName,
      description: 'Nueva ruta creada desde el formulario.'
    }, { withCredentials: true });
    if (res.data && res.data.data && res.data.data.id) {
      await fetchRutas();
      // Seleccionar la nueva ruta automáticamente
      const nueva = rutas.value.find(r => r._id === res.data.data.id);
      if (nueva) materialForm.value.route = nueva;
    }
  } catch (e) {
    routeError.value = e.response?.data?.message || 'Error al crear ruta';
  }
  creatingRoute.value = false;
}

// ...mockRoutes para la vista de rutas/materiales...
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
</script>

<style scoped>
@import 'vue-multiselect/dist/vue-multiselect.min.css';
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
.material-form {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 0 12px #39ff1433;
  padding: 2rem 1.5rem;
  max-width: 600px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}
.form-row {
  display: flex;
  gap: 1.2rem;
}
.form-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
}
.form-group label {
  color: #ff9100;
  font-weight: bold;
  margin-bottom: 0.3rem;
}
.material-form input[type="text"],
.material-form input[type="url"],
.material-form select {
  width: 100%;
  padding: 0.6rem;
  border: 1.5px solid #39ff14;
  border-radius: 6px;
  background: #f7f7f7;
  color: #181818;
  font-size: 1rem;
  outline: none;
  margin-top: 0.2rem;
}
.material-form input[type="file"] {
  margin-top: 0.5rem;
}
.difficulty-row {
  display: flex;
  gap: 1.2rem;
  margin-top: 0.5rem;
}
.difficulty-row label {
  color: #39ff14;
  font-weight: normal;
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 1.2rem;
}
.btn-neon {
  background: linear-gradient(90deg, #39ff14 60%, #ff9100 100%);
  color: #181818;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  padding: 0.8rem 1.5rem;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-neon:hover {
  background: linear-gradient(90deg, #ff9100 60%, #39ff14 100%);
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
@media (max-width: 700px) {
  .material-form {
    padding: 1rem 0.5rem;
    max-width: 99vw;
  }
  .form-row {
    flex-direction: column;
    gap: 0;
  }
}
</style> 