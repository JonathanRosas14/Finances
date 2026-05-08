<template>
  <div class="auth-success-container">
    <div class="loading">
      <p>Authenticating...</p>
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
    // Get the token from the URL
    const token = route.query.token;

    if (token) {
      // Save the token in localStorage
      localStorage.setItem("token", token);

      // Decode the token to get user information
      const parts = token.split(".");
      if (parts.length === 3) {
        const decoded = JSON.parse(atob(parts[1]));
        // Save user information
        localStorage.setItem("user", JSON.stringify(decoded));
      }

      // Redirect to MainPage/Dashboard after 500ms
      setTimeout(() => {
        router.push("/Dashboard");
      }, 500);
    } else {
      // If no token, redirect to login
      router.push("/login");
    }
  } catch (error) {
    console.error("Error in authentication:", error);
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