import './assets/main.css'
import { createRouter, createWebHistory } from 'vue-router'
import Login from './components/Login.vue'
import AdminPanel from './components/AdminPanel.vue'
import ProfessorPanel from './components/ProfessorPanel.vue'

const routes = [
  { path: '/login', component: Login },
  { path: '/admin', component: AdminPanel },
  { path: '/profesor', component: ProfessorPanel },
  // Aquí luego agregaremos las rutas protegidas para admin y profesor
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)
app.use(router)
app.mount('#app')
