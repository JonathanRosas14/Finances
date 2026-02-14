<template>
  <div class="register-container">
    <header>
      <div class="logo">
        <div class="logo-icon">
          <img src="../assets/Logo.png" alt="Logo" />
        </div>
        <span>Finances Pro</span>
      </div>
      <div class="header-botoms">
        <router-link to="/login" class="btn-login">Login</router-link>
      </div>
    </header>

    <div class="content-wrapper">
      <div class="left-side">
        <img src="../assets/Imagen6Register.png" alt="Imagen Register" />
        <div class="text-overlay">
          <h2>Take control of your financial future</h2>
          <p>
            Join thousands of users who are already saving smartly. Track your expenses, set goals,
            and achieve financial freedom.
          </p>
        </div>
      </div>
      <div class="right-side">
        <div class="form-wrapper">
          <h2>Create account</h2>
          <p>
            Do you already have an account?
            <router-link to="/login" class="login">Login</router-link>
          </p>
          <form @submit.prevent="handleRegister">
            <!--Mensaje de error-->
            <div v-if="errorMessage" class="error-message">
              {{ errorMessage }}
            </div>

            <!--Mensaje de exito-->
            <div v-if="successMessage" class="success-message">
              {{ successMessage }}
            </div>

            <div class="form-group">
              <label for="username">Username</label>
              <input
                type="text"
                id="username"
                v-model="username"
                required
                placeholder="Enter your username"
              />
            </div>

            <div class="form-group">
              <label for="email">Email</label>
              <input
                type="email"
                id="email"
                v-model="email"
                required
                placeholder="Enter your email"
              />
            </div>

            <div class="form-group">
              <label for="password">Password</label>
              <input
                type="password"
                id="password"
                v-model="password"
                required
                placeholder="Enter your password"
              />
            </div>

            <div class="form-group">
              <label for="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                v-model="confirmPassword"
                placeholder="Confirm your password"
                required
              />
            </div>

            <div class="terminos_condiciones">
              <input type="checkbox" id="terms" v-model="acceptedTerms" required />
              <label for="terms"> I accept the <a href="#">terms and conditions</a> </label>
            </div>
            <button type="submit" class="register-btn" :disabled="loading">
              {{ loading ? 'Registando...' : 'Register' }}
            </button>
            <div class="oauth-divider">or</div>

            <!-- Reemplaza el enlace de Google por este botón -->
            <div id="google-register-btn"></div>
          </form>

          <div class="datos-info">
            <p>Your data is encrypted and secure</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const username = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const acceptedTerms = ref(false);
const errorMessage = ref("");
const successMessage = ref("");
const loading = ref(false);

onMounted(() => {
  const token = route.query.token;
  if (token) {
    localStorage.setItem("token", token);
    router.push("/Dashboard");
  }

  window.google.accounts.id.initialize({
    client_id: "360602519490-kof8v9cb8ujs0ii4fs68jo4flsbvig6m.apps.googleusercontent.com",
    callback: handleGoogleCallback,
  });

  window.google.accounts.id.renderButton(
    document.getElementById("google-register-btn"),
    {
      theme: "filled_black",
      size: "large",
      width: "100%",
      text: "continue_with",
    }
  );
});

const handleGoogleCallback = async (response) => {
  try {
    const result = await axios.post("http://localhost:8000/api/google/", {
      token: response.credential,
    });
    const { token, user } = result.data;
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(user));
    router.push("/Dashboard");
  } catch (error) {
    errorMessage.value = "Error al registrarse con Google";
  }
};

const handleGoogleLogin = () => {
  window.google.accounts.id.prompt();
};

const handleRegister = async () => {
  errorMessage.value = "";
  successMessage.value = "";

  if (password.value !== confirmPassword.value) {
    errorMessage.value = "Passwords do not match.";
    return;
  }

  if (!acceptedTerms.value) {
    errorMessage.value = "You must accept the terms and conditions.";
    return;
  }

  loading.value = true;

  try {
    const response = await axios.post("http://localhost:8000/api/register/", {
      username: username.value,
      email: email.value,
      password: password.value,
    });

    successMessage.value = "Registration successful! You can now log in.";
    username.value = "";
    email.value = "";
    password.value = "";
    confirmPassword.value = "";
    acceptedTerms.value = false;
  } catch (error) {
    errorMessage.value =
      error.response?.data?.message || "An error occurred during registration.";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.register-container {
  width: 100%;
  min-height: 100vh;
  color: #ffffff;
  display: flex;
  flex-direction: column;
  background-color: #112218;
}

.content-wrapper {
  display: flex;
  flex: 1;
  height: calc(100vh - 60px);
}

header {
  width: 100%;
  height: 60px;
  padding: 0 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #112218;
  border-bottom: 1px solid #2e5c31;
}

.logo {
  display: flex;
  align-items: center;
  font-size: 24px;
  font-weight: bold;
  color: #ffffff;
}

.logo span {
  margin-left: 10px;
}

.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-icon img {
  width: 50px;
  height: 50px;
}

.btn-login {
  padding: 10px 50px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  text-decoration: none;
  color: #ffffff;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2e5c31;
}

.header-botoms {
  display: flex;
  gap: 10px;
}

.btn-login:hover {
  background-color: #3acf41;
  color: #000000;
}

.left-side {
  flex: 0 0 50%;
  position: relative;
  background: linear-gradient(135deg, #0d3b1f 0%, #1a5c3a 50%, #0d3b1f 100%);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.left-side img {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  opacity: 0.5;
}

.left-side::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to right, rgba(13, 59, 31, 0.8) 0%, rgba(13, 59, 31, 0.2) 100%);
  z-index: 1;
}

.right-side {
  flex: 1;
}

.text-overlay {
  position: relative;
  z-index: 2;
  color: white;
  max-width: 700px;
  padding: 40px 60px;
}

.text-overlay h2 {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 20px;
  line-height: 1.2;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.text-overlay p {
  font-size: 18px;
  line-height: 1.6;
  opacity: 0.95;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.4);
}

.form-wrapper {
  max-width: 700px;
  margin: 0 auto;
  padding: 40px 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
}

.form-wrapper h2 {
  font-size: 32px;
  margin-bottom: 10px;
  color: #ffffff;
}

.form-wrapper > p {
  margin-bottom: 30px;
  color: #cccccc;
}

.login {
  color: #3acf41;
  text-decoration: none;
}

.login:hover {
  text-decoration: underline;
}

.error-message {
  background-color: #ff4444;
  color: white;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.success-message {
  background-color: #3acf41;
  color: #000000;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 8px;
  color: #ffffff;
  font-size: 14px;
}

.form-group input {
  padding: 12px 16px;
  border: 1px solid #2e5c31;
  border-radius: 4px;
  font-size: 16px;
  background-color: #1a2e23;
  color: #ffffff;
  transition: border-color 0.3s;
}

.form-group input::placeholder {
  color: #6b8775;
}

.form-group input:focus {
  outline: none;
  border-color: #3acf41;
}

.terminos_condiciones {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.terminos_condiciones input[type='checkbox'] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.terminos_condiciones label {
  margin-left: 8px;
  font-size: 14px;
  color: #cccccc;
  cursor: pointer;
}

.terminos_condiciones a {
  color: #3acf41;
  text-decoration: none;
}

.terminos_condiciones a:hover {
  text-decoration: underline;
}

.register-btn {
  width: 100%;
  padding: 14px;
  border: none;
  border-radius: 4px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  background-color: #3acf41;
  color: #000000;
  transition: background-color 0.3s;
}

.register-btn:disabled {
  background-color: #2e5c31;
  cursor: not-allowed;
  opacity: 0.6;
}

.register-btn:hover:enabled {
  background-color: #34c239;
}

.datos-info {
  margin-top: 20px;
  font-size: 13px;
  color: #6b8775;
  text-align: center;
}

.oauth-divider {
  text-align: center;
  margin: 20px 0;
  color: #888888;
  position: relative;
}

.oauth-divider::before,
.oauth-divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 40%;
  height: 1px;
  background-color: #888888;
}
.oauth-divider::before {
  left: 0;
}
.oauth-divider::after {
  right: 0;
}

.google-btn {
  display: block;
  width: 100%;
  padding: 12px 16px;
  border: none;
  border-radius: 4px;
  font-size: 18px;
  cursor: pointer;
  background-color: #30a23b;
  color: #ffffff;
  text-align: center;
  text-decoration: none;
  transition: background-color 0.3s;
}

.google-btn:hover {
  background-color: #3acf41;
  color: #000000;
}

/* Media Queries para Responsividad */

/* Tablets y pantallas medianas */
@media (max-width: 1024px) {
  .text-overlay {
    left: 40px;
    max-width: 400px;
  }

  .text-overlay h2 {
    font-size: 36px;
  }

  .text-overlay p {
    font-size: 16px;
  }

  .logo span {
    font-size: 20px;
  }

  .btn-login {
    padding: 8px 30px;
    font-size: 14px;
  }

  .form-wrapper {
    padding: 30px 40px;
  }
}

/* Tablets pequeñas */
@media (max-width: 768px) {
  .content-wrapper {
    flex-direction: column;
  }

  .left-side {
    flex: 0 0 300px;
    min-height: 300px;
  }

  .right-side {
    flex: 1;
    overflow-y: auto;
  }

  .form-wrapper {
    padding: 30px 40px;
    height: auto;
  }

  .text-overlay {
    left: 30px;
    right: 30px;
    max-width: none;
  }

  .text-overlay h2 {
    font-size: 28px;
  }

  .text-overlay p {
    font-size: 14px;
  }

  header {
    padding: 0 20px;
  }

  .logo span {
    font-size: 18px;
  }

  .btn-login {
    padding: 8px 25px;
  }
}

/* Móviles */
@media (max-width: 480px) {
  header {
    padding: 0 15px;
    height: 50px;
  }

  .content-wrapper {
    height: auto;
    min-height: calc(100vh - 50px);
  }

  .logo-icon img {
    width: 40px;
    height: 40px;
  }

  .logo span {
    font-size: 16px;
  }

  .btn-login {
    padding: 6px 20px;
    font-size: 12px;
  }

  .left-side {
    flex: 0 0 250px;
    min-height: 250px;
  }

  .text-overlay {
    left: 20px;
    right: 20px;
  }

  .text-overlay h2 {
    font-size: 22px;
    margin-bottom: 10px;
  }

  .text-overlay p {
    font-size: 13px;
  }

  .form-wrapper {
    padding: 20px 20px;
    max-width: 100%;
  }

  .form-wrapper h2 {
    font-size: 26px;
  }

  .form-wrapper > p {
    font-size: 14px;
  }

  .form-group input {
    padding: 10px 14px;
    font-size: 14px;
  }

  .register-btn {
    padding: 12px;
    font-size: 16px;
  }
}
</style>
