<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const routes = ref([])
const loading = ref(true)
const error = ref(null)

// Obtener rutas de aprendizaje
const fetchRoutes = async () => {
  try {
    loading.value = true
    const response = await axios.get('http://localhost:5000/routes/')
    routes.value = response.data
  } catch (err) {
    error.value = 'Error al cargar las rutas de aprendizaje'
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}

// Cargar rutas al montar el componente
onMounted(() => {
  fetchRoutes()
})

// Función para formatear la fecha
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Función para navegar a la vista detallada de una ruta
const viewRoute = (routeId: number) => {
  router.push(`/professor/routes/${routeId}`)
}
</script>

<template>
  <div class="learning-routes">
    <h1>Rutas de Aprendizaje</h1>
    
    <!-- Loading state -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Cargando rutas...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>

    <!-- Empty state -->
    <div v-else-if="routes.length === 0" class="empty-state">
      <p>No hay rutas de aprendizaje disponibles.</p>
      <p>¡Crea tu primera ruta de aprendizaje!</p>
    </div>

    <!-- Routes grid -->
    <div v-else class="routes-grid">
      <div v-for="route in routes" 
           :key="route.id" 
           class="route-card"
           @click="viewRoute(route.id)">
        <h3>{{ route.title }}</h3>
        <p class="description">{{ route.description }}</p>
        <div class="route-info">
          <span class="materials">
            <i class="fas fa-book"></i>
            {{ route.materials_count || 0 }} materiales
          </span>
          <span class="date">
            <i class="fas fa-calendar"></i>
            {{ formatDate(route.created_at) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.learning-routes {
  padding: 2rem;
}

h1 {
  color: #333;
  margin-bottom: 2rem;
}

.loading, .error, .empty-state {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #00ff00;
  border-radius: 50%;
  margin: 0 auto 1rem;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  color: #ff0000;
}

.empty-state {
  color: #666;
}

.empty-state p:first-child {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.empty-state p:last-child {
  color: #00ff00;
  font-weight: 500;
}

.routes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.route-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.route-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.route-card h3 {
  color: #333;
  margin-bottom: 0.5rem;
}

.description {
  color: #666;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.route-info {
  display: flex;
  justify-content: space-between;
  color: #888;
  font-size: 0.9rem;
}

.route-info span {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.route-info i {
  color: #00ff00;
}
</style> 