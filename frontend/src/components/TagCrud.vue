<template>
  <div class="tag-crud">
    <div class="header-row">
      <h2>Etiquetas</h2>
      <button class="btn-neon" @click="openCreateModal">+ Crear etiqueta</button>
    </div>
    <table class="tag-table">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="tag in tags" :key="tag._id">
          <td>{{ tag.name }}</td>
          <td>
            <button class="btn-edit" @click="openEditModal(tag)">Editar</button>
            <button class="btn-delete" @click="openDeleteModal(tag)">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>
    <!-- Modal de creación -->
    <div v-if="showCreateModal" class="modal-bg">
      <div class="modal-box">
        <h3 style="color:#39ff14;">Crear Etiqueta</h3>
        <form @submit.prevent="handleCreate">
          <div class="form-group">
            <label>Nombre</label>
            <input v-model="form.name" type="text" required />
          </div>
          <div v-if="error" class="form-error">{{ error }}</div>
          <div class="form-actions">
            <button class="btn-neon" type="submit">Crear</button>
            <button class="btn-cancel" type="button" @click="closeCreateModal">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
    <!-- Modal de edición -->
    <div v-if="showEditModal" class="modal-bg">
      <div class="modal-box">
        <h3 style="color:#39ff14;">Editar Etiqueta</h3>
        <form @submit.prevent="handleEdit">
          <div class="form-group">
            <label>Nombre</label>
            <input v-model="editForm.name" type="text" required />
          </div>
          <div v-if="editError" class="form-error">{{ editError }}</div>
          <div class="form-actions">
            <button class="btn-neon" type="submit">Guardar</button>
            <button class="btn-cancel" type="button" @click="closeEditModal">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
    <!-- Modal de eliminación -->
    <div v-if="showDeleteModal" class="modal-bg">
      <div class="modal-box">
        <h3 style="color:#ff9100;">¿Eliminar etiqueta?</h3>
        <p style="color:#181818;">¿Estás seguro de que deseas eliminar <b>{{ deleteTagData.name }}</b>?</p>
        <div v-if="deleteError" class="form-error">{{ deleteError }}</div>
        <div class="form-actions">
          <button class="btn-delete" @click="handleDelete">Eliminar</button>
          <button class="btn-cancel" @click="closeDeleteModal">Cancelar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const tags = ref([]);
const showCreateModal = ref(false);
const showEditModal = ref(false);
const showDeleteModal = ref(false);
const form = ref({ name: '' });
const editForm = ref({ _id: '', name: '' });
const deleteTagData = ref({});
const error = ref('');
const editError = ref('');
const deleteError = ref('');

async function fetchTags() {
  try {
    const res = await axios.get('http://localhost:5000/tags/');
    tags.value = res.data.data || [];
  } catch (e) {
    tags.value = [];
  }
}

function openCreateModal() {
  form.value = { name: '' };
  error.value = '';
  showCreateModal.value = true;
}
function closeCreateModal() {
  showCreateModal.value = false;
}

async function handleCreate() {
  error.value = '';
  if (!form.value.name) {
    error.value = 'Completa el nombre';
    return;
  }
  try {
    await axios.post('http://localhost:5000/tags/', form.value, { withCredentials: true });
    showCreateModal.value = false;
    await fetchTags();
  } catch (e) {
    error.value = e.response?.data?.message || 'Error al crear etiqueta';
  }
}

function openEditModal(tag) {
  editForm.value = { _id: tag._id, name: tag.name };
  editError.value = '';
  showEditModal.value = true;
}
function closeEditModal() {
  showEditModal.value = false;
}

async function handleEdit() {
  editError.value = '';
  if (!editForm.value.name) {
    editError.value = 'Completa el nombre';
    return;
  }
  try {
    await axios.put(`http://localhost:5000/tags/${editForm.value._id}`, editForm.value, { withCredentials: true });
    showEditModal.value = false;
    await fetchTags();
  } catch (e) {
    editError.value = e.response?.data?.message || 'Error al editar etiqueta';
  }
}

function openDeleteModal(tag) {
  deleteTagData.value = tag;
  deleteError.value = '';
  showDeleteModal.value = true;
}
function closeDeleteModal() {
  showDeleteModal.value = false;
}

async function handleDelete() {
  try {
    await axios.delete(`http://localhost:5000/tags/${deleteTagData.value._id}`, { withCredentials: true });
    showDeleteModal.value = false;
    await fetchTags();
  } catch (e) {
    deleteError.value = e.response?.data?.message || 'Error al eliminar etiqueta';
  }
}

onMounted(fetchTags);
</script>

<style scoped>
.tag-crud {
  width: 100%;
  background: #fff;
  border-radius: 12px;
  padding: 2rem 1rem;
  box-shadow: 0 0 12px #39ff1433;
}
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.tag-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
}
.tag-table th {
  color: #39ff14;
  font-size: 1.1rem;
  padding: 0.7rem;
  border-bottom: 2px solid #39ff14;
  text-align: left;
}
.tag-table td {
  color: #181818;
  padding: 0.7rem;
  border-bottom: 1px solid #eee;
}
.btn-neon {
  background: linear-gradient(90deg, #39ff14 60%, #ff9100 100%);
  color: #181818;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-neon:hover {
  background: linear-gradient(90deg, #ff9100 60%, #39ff14 100%);
}
.btn-cancel {
  background: none;
  color: #ff9100;
  border: 1.5px solid #ff9100;
  border-radius: 6px;
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
  cursor: pointer;
  margin-left: 1rem;
  font-weight: bold;
  transition: background 0.2s, color 0.2s;
}
.btn-cancel:hover {
  background: #ff9100;
  color: #fff;
}
.btn-edit {
  background: none;
  color: #39ff14;
  border: 1.5px solid #39ff14;
  border-radius: 5px;
  padding: 0.3rem 0.8rem;
  margin-right: 0.5rem;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.2s, color 0.2s;
}
.btn-edit:hover {
  background: #39ff14;
  color: #181818;
}
.btn-delete {
  background: none;
  color: #ff9100;
  border: 1.5px solid #ff9100;
  border-radius: 5px;
  padding: 0.3rem 0.8rem;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.2s, color 0.2s;
}
.btn-delete:hover {
  background: #ff9100;
  color: #181818;
}
.modal-bg {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-box {
  background: #fff;
  border-radius: 12px;
  padding: 2rem 2.5rem;
  box-shadow: 0 0 24px #39ff14, 0 0 8px #ff9100;
  min-width: 320px;
  max-width: 95vw;
  text-align: center;
}
.form-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 1rem;
  width: 100%;
}
.form-group label {
  color: #ff9100;
  font-weight: bold;
  margin-bottom: 0.3rem;
}
.form-group input {
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
.form-error {
  color: #ff9100;
  margin-bottom: 1rem;
  text-align: left;
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 1.2rem;
}
@media (max-width: 700px) {
  .tag-crud {
    padding: 1rem 0.2rem;
  }
  .modal-box {
    padding: 1rem 0.5rem;
    min-width: 90vw;
  }
}
</style> 