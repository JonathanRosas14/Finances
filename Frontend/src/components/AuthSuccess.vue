<template>
  <div class="auth-success-container">
    <div class="loading">
      <p>Autenticando...</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();

onMounted(async () => {
  try {
    // Obtener el token de la URL
    const token = route.query.token;

    if (token) {
      // Guardar el token en localStorage
      localStorage.setItem("token", token);

      // Decodificar el token para obtener la información del usuario
      const parts = token.split(".");
      if (parts.length === 3) {
        const decoded = JSON.parse(atob(parts[1]));
        // Guardar información del usuario
        localStorage.setItem("user", JSON.stringify(decoded));
      }

      // Redireccionar a MainPage/Dashboard después de 500ms
      setTimeout(() => {
        router.push("/Dashboard");
      }, 500);
    } else {
      // Si no hay token, redirigir a login
      router.push("/login");
    }
  } catch (error) {
    console.error("Error en autenticación:", error);
    router.push("/login");
  }
});
</script>

<style scoped>
.auth-success-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0a1a0f 0%, #112218 100%);
}

.loading {
  text-align: center;
  color: #ffffff;
  font-size: 18px;
}
</style>