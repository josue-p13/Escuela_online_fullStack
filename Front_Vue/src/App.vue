<script setup>
  import { ref } from 'vue';
  import Login from './components/Login.vue';
  import Register from './components/Register.vue';
  import Dashboard from './components/Dashboard.vue'; // Importar Dashboard

  // Estado para controlar qué componente mostrar (Login/Register o Dashboard)
  const isAuthenticated = ref(false);
  // Cambiado para almacenar el objeto de usuario completo
  const loggedInUser = ref(null); // Inicialmente null

  // Estado para alternar entre Login y Register (solo si no está autenticado)
  const showLoginView = ref(true);

  // Función para cambiar entre Login y Register
  function toggleAuthView() {
    showLoginView.value = !showLoginView.value;
  }

  // Función para manejar el éxito del login
  function handleLoginSuccess(userData) {
    console.log('Login success event received in App.vue:', userData);
    loggedInUser.value = userData; // Guardar el objeto de usuario completo
    isAuthenticated.value = true; // Marcar como autenticado
  }
</script>

<template>
  <!-- Si el usuario está autenticado, muestra el Dashboard -->
  <!-- Pasar el objeto loggedInUser completo como prop 'user' -->
  <Dashboard v-if="isAuthenticated" :user="loggedInUser" />

  <!-- Si no está autenticado, muestra Login o Register -->
  <template v-else>
    <Login v-if="showLoginView" @showRegister="toggleAuthView" @loginSuccess="handleLoginSuccess" />
    <Register v-else @showLogin="toggleAuthView" />
  </template>
</template>

<style lang="scss">
@use './assets/colors.scss' as colors;

body {
  background-color: colors.$color-bg;
  margin: 0;
  font-family: sans-serif;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
