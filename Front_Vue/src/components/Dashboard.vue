<script setup>
// Definir las props que el componente espera recibir
defineProps({
  user: { // Recibe el objeto user completo
    type: Object,
    required: true
  }
})
</script>

<template>
  <div>
    <!-- Mostrar nombres y apellidos del objeto user -->
    <h1>Bienvenido, {{ user.nombres }} {{ user.apellidos }}!</h1>
    <p>Este es tu panel de control. Tu correo es: {{ user.email }}</p>
  </div>
</template>

<style scoped>
/* Añade estilos si es necesario */
h1 {
  color: #333;
}
</style>
