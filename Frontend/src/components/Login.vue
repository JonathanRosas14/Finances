<template>
  <div class="login-container">
    <header>
      <div class="logo">
        <div class="logo-icon">
          <img src="../assets/Logo.png" alt="Logo" />
        </div>
        <span>Finances Pro</span>
      </div>
      <div class="header-botoms">
        <router-link to="/help" class="btn-help">Help</router-link>
      </div>
    </header>
    <div class="form-container">
      <h2>Welcome back</h2>
      <p>Manage your finances securely</p>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" required placeholder="Enter your email" />
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

        <a class="forget-password" href="#">Did you forget your password?</a>

        <button type="submit" class="btn-login">Login</button>
        <div class="oauth-divider">or</div>

        
        <div id="google-login-btn"></div>
      </form>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <p class="register-link">
        Don't have an account?
        <router-link to="/register">Register</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");
const errorMessage = ref("");
const router = useRouter();

onMounted(() => {
  window.google.accounts.id.initialize({
    client_id: "360602519490-kof8v9cb8ujs0ii4fs68jo4flsbvig6m.apps.googleusercontent.com",
    callback: handleGoogleCallback,
  });

  window.google.accounts.id.renderButton(
    document.getElementById("google-login-btn"),
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
    errorMessage.value = "Error al iniciar sesión con Google";
  }
};

const handleLogin = async () => {
  try {
    const response = await axios.post("http://localhost:8000/api/login/", {
      email: email.value,
      password: password.value,
    });

    const { token, user } = response.data;
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(user));
    router.push("/Dashboard");
  } catch (error) {
    errorMessage.value =
      error.response?.data?.message || "Error al iniciar sesión";
  }
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.login-container {
  width: 100%;
  min-height: 100vh;
  color: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0a1a0f 0%, #112218 100%);
  padding: 80px 20px 20px 20px;
  margin-top: 0;
}

header {
  position: fixed;
  top: 0;
  width: 100%;
  height: 60px;
  padding: 0 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #112218;
  border-bottom: 1px solid #2e5c31;
  z-index: 100;
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

.btn-help {
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

.btn-help:hover {
  background-color: #3acf41;
  color: #000000;
}

.form-container {
  width: 500px;
  padding: 50px 60px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  background: rgba(17, 34, 24, 0.95);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid #2e5c31;
  backdrop-filter: blur(10px);
  max-height: 90vh;
  overflow-y: auto;
}

.form-container h2 {
  font-size: 32px;
  margin-bottom: 10px;
  color: #ffffff;
  text-align: center;
}

.form-container p {
  font-size: 18px;
  margin-bottom: 30px;
  color: #cccccc;
  text-align: center;
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

.forget-password {
  display: block;
  margin-bottom: 20px;
  font-size: 14px;
  color: #3acf41;
  text-decoration: none;
}

.forget-password:hover {
  text-decoration: underline;
}

.btn-login {
  width: 100%;
  padding: 12px 16px;
  border: none;
  border-radius: 4px;
  font-size: 18px;
  cursor: pointer;
  background-color: #2e5c31;
  color: #ffffff;
  transition: background-color 0.3s;
}

.btn-login:hover {
  background-color: #3acf41;
  color: #000000;
}

.error-message {
  margin-top: 20px;
  color: #ff4d4f;
  font-size: 14px;
}

.register-link {
  margin-top: 20px;
  font-size: 14px;
  color: #cccccc;
}

.register-link a {
  color: #3acf41;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
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

/* Media Queries para responsividad */
@media (max-width: 768px) {
  .login-container {
    padding: 80px 20px 20px 20px;
    justify-content: center;
    min-height: 100vh;
  }

  .form-container {
    width: 90%;
    max-width: 500px;
    padding: 40px 30px;
    max-height: none;
  }

  header {
    height: 60px;
    padding: 0 15px;
  }

  .logo {
    font-size: 20px;
  }

  .logo-icon img {
    width: 40px;
    height: 40px;
  }

  .btn-help {
    padding: 8px 30px;
    font-size: 14px;
  }

  .form-container h2 {
    font-size: 28px;
    margin-bottom: 8px;
  }

  .form-container p {
    font-size: 16px;
    margin-bottom: 25px;
  }
}

@media (max-width: 600px) {
  .login-container {
    padding: 80px 15px 20px 15px;
    padding-bottom: 20px;
    justify-content: center;
  }

  .form-container {
    width: 95%;
    max-width: 100%;
    padding: 30px 20px;
    border-radius: 8px;
    max-height: none;
  }

  header {
    padding: 0 12px;
  }

  .logo {
    font-size: 18px;
  }

  .logo-icon img {
    width: 35px;
    height: 35px;
  }

  .logo span {
    margin-left: 8px;
  }

  .btn-help {
    padding: 8px 25px;
    font-size: 13px;
  }

  .form-container h2 {
    font-size: 24px;
    margin-bottom: 6px;
  }

  .form-container p {
    font-size: 14px;
    margin-bottom: 20px;
  }

  .form-group {
    margin-bottom: 16px;
  }

  .form-group label {
    margin-bottom: 6px;
    font-size: 13px;
  }

  .form-group input {
    padding: 10px 12px;
    font-size: 14px;
  }

  .forget-password {
    margin-bottom: 16px;
    font-size: 12px;
  }

  .btn-login {
    padding: 10px 12px;
    font-size: 16px;
  }

  .google-btn {
    padding: 10px 12px;
    font-size: 16px;
  }

  .oauth-divider {
    margin: 16px 0;
    font-size: 14px;
  }

  .register-link {
    margin-top: 16px;
    font-size: 12px;
  }
}

@media (max-width: 400px) {
  .form-container {
    padding: 25px 15px;
  }

  .form-container h2 {
    font-size: 20px;
  }

  .form-container p {
    font-size: 13px;
    margin-bottom: 18px;
  }

  .form-group input {
    padding: 8px 10px;
    font-size: 13px;
  }

  .btn-login,
  .google-btn {
    padding: 8px 10px;
    font-size: 14px;
  }
}
</style>
