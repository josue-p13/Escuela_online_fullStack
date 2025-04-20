<script>
import { ref } from 'vue';

export default {
    name: 'Register',
    emits: ['showLogin'],
    setup(props, { emit }) { 
        const nombres = ref('');
        const apellidos = ref('');
        const email = ref('');
        const telefono = ref('');
        const password = ref('');
        const confirmPassword = ref('');
        const errorMessage = ref('');
        const successMessage = ref(''); 

        // Método para manejar el envío del formulario
        const handleSubmit = async () => {
            errorMessage.value = ''; 
            successMessage.value = ''; 

            if (password.value !== confirmPassword.value) {
                errorMessage.value = 'Las contraseñas no coinciden.';
                return;
            }
            if (!nombres.value || !apellidos.value || !email.value || !password.value) {
                errorMessage.value = 'Por favor, completa todos los campos obligatorios.';
                return;
            }
            const formData = new FormData();
            formData.append('nombres', nombres.value);
            formData.append('apellidos', apellidos.value);
            formData.append('email', email.value);
            if (telefono.value) { // Solo añadir si tiene valor
                formData.append('telefono', telefono.value);
            }
            formData.append('password', password.value);
            formData.append('confirm_password', confirmPassword.value);

            try {
                const response = await fetch('http://localhost:8000/auth/register', {
                    method: 'POST',
                    body: formData,
                });

                const data = await response.json(); 
                if (!response.ok) {
                    throw new Error(data.detail || `Error ${response.status}`);
                }
                // Éxito
                successMessage.value = data.message || '¡Registro exitoso!';
                // Limpiar formulario 
                nombres.value = '';
                apellidos.value = '';
                email.value = '';
                telefono.value = '';
                password.value = '';
                confirmPassword.value = '';
            } catch (error) {
                errorMessage.value = error.message || 'Ocurrió un error al registrar. Inténtalo de nuevo.';
                console.error('Error en el registro:', error);
            }
        };

        return { 
            nombres,
            apellidos,
            email,
            telefono,
            password,
            confirmPassword,
            errorMessage,
            successMessage,
            handleSubmit,
        };
    }
}
</script>

<template>
    <div>
        <h1>Registro</h1>
        <!-- Mostrar mensajes de error o éxito -->
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success-message">{{ successMessage }}</p>

        <form @submit.prevent="handleSubmit"> <!-- Usar el método handleSubmit -->
        <!-- Usar v-model para enlazar inputs con las variables reactivas -->
        <input type="text" placeholder="Nombres" v-model="nombres" required>
        <input type="text" placeholder="Apellidos" v-model="apellidos" required>
        <input type="email" placeholder="Correo electrónico" v-model="email" required>
        <input type="tel" placeholder="Número de teléfono (Opcional)" v-model="telefono">
        <input type="password" placeholder="Contraseña" v-model="password" required>
        <input type="password" placeholder="Confirmar Contraseña" v-model="confirmPassword" required>
        <button type="submit">Registrarse</button>
        </form>
        <p class="toggle-link">
        ¿Ya tienes cuenta? <a href="#" @click.prevent="$emit('showLogin')">Inicia sesión aquí</a>
        </p>
    </div>
</template>

<style lang="scss" scoped>
@use '../assets/colors.scss' as colors;

/* Añadir estilos para mensajes de error y éxito */
.error-message {
    color: colors.$color-error; /* Asegúrate de tener esta variable en colors.scss */
    background-color: rgba(255, 0, 0, 0.1);
    border: 1px solid colors.$color-error;
    padding: 10px;
    border-radius: 4px;
    margin-bottom: 15px;
    text-align: left;
}

.success-message {
    color: colors.$color-success; /* Asegúrate de tener esta variable en colors.scss */
    background-color: rgba(0, 128, 0, 0.1);
    border: 1px solid colors.$color-success;
    padding: 10px;
    border-radius: 4px;
    margin-bottom: 15px;
    text-align: left;
}

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

form {
    display: flex;
    flex-direction: column;
    gap: 15px; // Un poco menos de espacio para más campos
}

input[type="text"],
input[type="email"],
input[type="tel"],
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
    margin-top: 10px; // Espacio extra antes del botón
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

.toggle-link {
margin-top: 25px;
font-size: 0.9rem;
color: colors.$color-primary;

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

/* Media Query */
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
    input[type="email"],
    input[type="tel"],
    input[type="password"],
    button {
        font-size: 0.95rem;
        padding: 10px 12px;
    }

    form {
        gap: 12px;
    }
    .toggle-link {
        font-size: 0.85rem;
    }
}
</style>