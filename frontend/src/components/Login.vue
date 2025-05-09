<template>
  <div class="login-bg">
    <form class="login-form" @submit.prevent="handleLogin">
      <h2>Iniciar Sesión</h2>
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div class="form-group">
        <label for="password">Contraseña</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Entrar</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const error = ref('');
const router = useRouter();

async function handleLogin() {
  error.value = '';
  if (!email.value || !password.value) {
    error.value = 'Completa todos los campos';
    return;
  }
  try {
    const response = await axios.post('http://localhost:5000/auth/login', {
      email: email.value,
      password: password.value
    }, {
      withCredentials: true // Para que se guarde la cookie de sesión
    });
    const data = response.data;
    if (data.status === 'success') {
      // Redirigir según el rol
      if (data.data.role === 'admin') {
        router.push('/admin');
      } else if (data.data.role === 'professor') {
        router.push('/profesor');
      } else {
        error.value = 'Rol no reconocido';
      }
    } else {
      error.value = data.message || 'Error desconocido';
    }
  } catch (err) {
    if (err.response && err.response.data && err.response.data.message) {
      error.value = err.response.data.message;
    } else {
      error.value = 'Error de conexión con el servidor';
    }
  }
}
</script>

<style scoped>
.login-bg {
  min-height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #181818;
}
.login-form {
  background: #222;
  padding: 2.5rem 2.5rem;
  border-radius: 18px;
  box-shadow: 0 0 32px #39ff14, 0 0 12px #ff9100;
  display: flex;
  flex-direction: column;
  max-width: 380px;
  width: 100%;
}
.login-form h2 {
  color: #39ff14;
  margin-bottom: 1.5rem;
  text-align: center;
}
.form-group {
  margin-bottom: 1.2rem;
}
label {
  color: #ff9100;
  font-weight: bold;
  margin-bottom: 0.3rem;
  display: block;
}
input {
  width: 100%;
  padding: 0.6rem;
  border: 1.5px solid #39ff14;
  border-radius: 6px;
  background: #181818;
  color: #fff;
  font-size: 1rem;
  outline: none;
  margin-top: 0.2rem;
}
button {
  background: linear-gradient(90deg, #39ff14 60%, #ff9100 100%);
  color: #181818;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  padding: 0.8rem;
  font-size: 1.1rem;
  cursor: pointer;
  margin-top: 0.8rem;
  transition: background 0.2s;
}
button:hover {
  background: linear-gradient(90deg, #ff9100 60%, #39ff14 100%);
}
.error {
  color: #ff9100;
  margin-top: 1rem;
  text-align: center;
}
</style> 