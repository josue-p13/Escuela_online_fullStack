<script >
import { ref } from 'vue'; // Importar ref

export default {
    name : 'Login',
    emits: ['showRegister', 'loginSuccess'], // Añadir 'loginSuccess' a los emits
    setup(props, { emit }) {
        const email = ref('');
        const password = ref('');
        const errorMessage = ref('');

        const handleLogin = async () => {
            errorMessage.value = ''; // Limpiar errores previos

            if (!email.value || !password.value) {
                errorMessage.value = 'Por favor, ingresa correo y contraseña.';
                return;
            }

            try {
                const response = await fetch('http://localhost:8000/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email.value,
                        password: password.value,
                    }),
                });

                if (!response.ok) {
                    // Intenta obtener el detalle del error de la respuesta JSON
                    const errorData = await response.json().catch(() => ({})); // Intenta parsear JSON, si falla, objeto vacío
                    throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`);
                }

                const data = await response.json();

                // Login exitoso
                console.log('Login exitoso:', data);
                // Emitir el objeto 'user' completo recibido del backend
                emit('loginSuccess', data.user);

            } catch (error) {
                // Asegurarse de que error.message sea una cadena
                if (error instanceof Error) {
                    errorMessage.value = error.message;
                } else {
                    errorMessage.value = 'Ocurrió un error inesperado al iniciar sesión.';
                }
                console.error('Error en el login:', error);
            }
        };

        return {
            email,
            password,
            errorMessage,
            handleLogin,
        };
    }
}
</script>

<template>
<div>
    <h1>Login</h1>
    <!-- Mostrar mensaje de error -->
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <form @submit.prevent="handleLogin"> <!-- Usar handleLogin -->
    <input type="text" placeholder="Ingresa tu correo" v-model="email" required>
    <input type="password" placeholder="Contraseña" v-model="password" required>
    <button type="submit">Iniciar Sesión</button>
    </form>
    <!-- Enlace para ir al registro -->
    <p class="toggle-link">
    ¿Aun no tienes cuenta? <a href="#" @click.prevent="$emit('showRegister')">da click aqui para crearla</a>
    </p>
</div>
</template>

<style lang="scss" scoped>
@use '../assets/colors.scss' as colors;

div {
    max-width: 400px;
    padding: 30px;
    border: 1px solid colors.$color-accent2;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: colors.$color-bg;
    text-align: center;
    box-sizing: border-box;
}

h1 {
    color: colors.$color-primary;
    margin-bottom: 25px;
    font-weight: 500;
}

/* Añadir estilos para mensajes de error */
.error-message {
    color: colors.$color-error; /* Asegúrate de tener esta variable en colors.scss */
    background-color: rgba(255, 0, 0, 0.1);
    border: 1px solid colors.$color-error;
    padding: 10px;
    border-radius: 4px;
    margin-bottom: 15px;
    text-align: left;
}

form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

input[type="text"],
input[type="password"] {
    padding: 12px 15px;
    border: 1px solid colors.$color-accent1;
    border-radius: 4px;
    font-size: 1rem;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    box-sizing: border-box;
    background-color: #fff;
    color: colors.$color-primary;
    &::placeholder {
    color: colors.$color-accent2;
    opacity: 0.7;
    }
    &:focus {
    outline: none;
    border-color: colors.$color-primary;
    box-shadow: 0 0 0 3px rgba(72, 166, 167, 0.25);
    }
}

button {
    padding: 12px 20px;
    background-color: colors.$color-primary;
    color: colors.$color-bg;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s ease;
    &:hover {
    background-color: colors.$color-accent2;
    }
}

// Estilos para el enlace de cambio de vista
.toggle-link {
  margin-top: 25px; // Espacio sobre el enlace
  font-size: 0.9rem;
  color: colors.$color-primary; // Color del texto normal

  a {
    color: colors.$color-accent2; // Color del enlace
    text-decoration: underline;
    cursor: pointer;
    background: none; // Sin fondo
    border: none; // Sin borde
    padding: 0; // Sin padding extra

    &:hover, &:active, &:focus {
      color: colors.$color-accent2; // Mantiene el color al interactuar
      text-decoration: underline; // Mantiene el subrayado
    }
  }
}


/* Media Query para pantallas más pequeñas (ej. móviles) */
@media (max-width: 480px) {
    div {
        max-width: 95%;
        margin: 20px auto;
        padding: 20px;
    }

    h1 {
        font-size: 1.5rem;
        margin-bottom: 20px;
    }

    input[type="text"],
    input[type="password"],
    button {
        font-size: 0.95rem;
        padding: 10px 12px;
    }

    form {
        gap: 15px;
    }
    .toggle-link {
        font-size: 0.85rem; // Un poco más pequeño en móvil
    }
}
</style>
