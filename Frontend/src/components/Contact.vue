<template>
  <div class="home-container">
    <header>
      <div class="logo">
        <div class="logo-icon">
          <img src="../assets/Logo.png" alt="Logo" />
        </div>
        <span>Finances Pro</span>
      </div>
      <div class="nav-link">
        <router-link to="/features" class="nav-item">Features</router-link>
        <router-link to="/about" class="nav-item">About Us</router-link>
        <router-link to="/contact" class="nav-item">Contact</router-link>
      </div>

      <div class="header-botoms">
        <router-link to="/login" class="btn-login">Login </router-link>
        <router-link to="/register" class="btn-signup">Sign Up</router-link>
      </div>
    </header>
    <section class="contact">
      <div class="info-principal">
        <div class="info-text">
          <h1>We are here to help you</h1>
          <p>
            Do you have questions about your account or need technical
            assistance? Our team of financial experts is available to assist you
            every step of the way.
          </p>
        </div>
        <div class="cards-contact">
          <div class="card1">
            <form>
              <h2>Contact us</h2>
              <div class="form-group">
                <label for="name">Username</label>
                <input
                  type="text"
                  id="name"
                  required
                  placeholder="Enter your username"
                />
              </div>
              <div class="form-group">
                <label for="email">Email</label>
                <input
                  type="email"
                  id="email"
                  required
                  placeholder="Enter your email"
                />
              </div>

              <div class="form-group">
                <label for="subject">Inquiry subject</label>
                <select id="subject">
                  <option value="general">General Inquiry</option>
                  <option value="support">Technical Support</option>
                  <option value="billing">Billing</option>
                  <option value="feedback">Feedback</option>
                </select>
              </div>

              <div class="form-group">
                <label for="message">Message</label>
                <textarea
                  id="message"
                  rows="4"
                  required
                  placeholder="Enter your message"
                ></textarea>
              </div>
              <button type="submit">Send Message</button>
            </form>
          </div>
          <div class="card2">
            <h2>Contact Information</h2>
            <p>
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M3.00977 5.83789C3.00977 5.28561 3.45748 4.83789 4.00977 4.83789H20C20.5523 4.83789 21 5.28561 21 5.83789V17.1621C21 18.2667 20.1046 19.1621 19 19.1621H5C3.89543 19.1621 3 18.2667 3 17.1621V6.16211C3 6.11449 3.00333 6.06765 3.00977 6.0218V5.83789ZM5 8.06165V17.1621H19V8.06199L14.1215 12.9405C12.9499 14.1121 11.0504 14.1121 9.87885 12.9405L5 8.06165ZM6.57232 6.80554H17.428L12.7073 11.5263C12.3168 11.9168 11.6836 11.9168 11.2931 11.5263L6.57232 6.80554Z"
                  fill="currentColor"
                />
              </svg>
              soporte@financespro.com
            </p>
            <p>
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M17 9H7V7H17V9Z" fill="currentColor" />
                <path d="M7 13H17V11H7V13Z" fill="currentColor" />
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M2 18V2H22V18H16V22H14C11.7909 22 10 20.2091 10 18H2ZM12 16V18C12 19.1046 12.8954 20 14 20V16H20V4H4V16H12Z"
                  fill="currentColor"
                />
              </svg>
              +1 (555) 123-4567
            </p>
            <p>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 512 512"
                id="IconChangeColor"
              >
                <title>ionicons-v5-n</title>
                <path
                  d="M256,32C167.67,32,96,96.51,96,176c0,128,160,304,160,304S416,304,416,176C416,96.51,344.33,32,256,32Zm0,224a64,64,0,1,1,64-64A64.07,64.07,0,0,1,256,256Z"
                  id="mainIconPathAttribute"
                  fill="#3acf41"
                ></path>
              </svg>
              123 Finance St., Money City, Country
            </p>
          </div>
        </div>
      </div>
    </section>
    <footer class="footer">
      <!-- Future footer content can be added here -->
      <div class="footer-content">
        <div class="footer1">
          <div class="footer-column1">
            <div class="logo">
              <div class="logo-icon">
                <img src="../assets/Logo.png" alt="Logo" />
              </div>
              <span>Finances Pro</span>
            </div>
            <p>
              The smartest way to manage your money, investments, and financial
              future.
            </p>
          </div>
          <div class="footer-column2">
            <h3>PRODUCT</h3>
            <ul>
              <li><router-link to="/features">Features</router-link></li>
              <li><router-link to="/">Prices</router-link></li>
              <li><router-link to="/">Security</router-link></li>
            </ul>
          </div>
          <div class="footer-column3">
            <h3>COMPANY</h3>
            <ul>
              <li><router-link to="/about">About Us</router-link></li>
              <li><router-link to="/contact">Contact</router-link></li>
              <li><router-link to="/">Blog</router-link></li>
            </ul>
          </div>
        </div>
        <div class="copyright">
          <p>© 2025 Finances Pro. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup></script>

<style scoped>
/* ============================================ */
/* ESTILOS GLOBALES Y CONTENEDOR PRINCIPAL */
/* ============================================ */

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* Contenedor principal de toda la página */
.home-container {
  width: 100%;
  min-height: 100vh;
  color: #ffffff;
}

/* ============================================ */
/* ENCABEZADO (HEADER) */
/* ============================================ */

/* Barra superior con logo, navegación y botones */
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

/* Logo y texto "Finances Pro" */
.logo {
  display: flex;
  align-items: center;
  font-size: 24px;
  font-weight: bold;
  color: #ffffff;
}

/* Espaciado del texto del logo */
.logo span {
  margin-left: 10px;
}

/* Contenedor del ícono del logo */
.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Imagen del ícono del logo */
.logo-icon img {
  width: 50px;
  height: 50px;
}

/* Contenedor de los links de navegación */
.nav-link {
  display: flex;
  gap: 20px;
}

/* Estilos individuales de cada link (Features, About Us, Prices) */
.nav-item {
  color: #ffffff;
  text-decoration: none;
  font-size: 18px;
  transition: color 0.3s;
  padding: 10px 15px;
}

/* Efecto hover en los links de navegación */
.nav-item:hover {
  background-color: #2e5c31;
  border-radius: 4px;
}

/* Contenedor de los botones (Login y Sign Up) */
.header-botoms {
  display: flex;
  gap: 10px;
}

/* Botón Login - Estilo base */
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
}

/* Botón Sign Up - Estilo base */
.btn-signup {
  padding: 10px 40px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  text-decoration: none;
  color: #000000;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Color base del botón Login */
.btn-login {
  background-color: #2e5c31;
}

/* Efecto hover del botón Login */
.btn-login:hover {
  background-color: #3acf41;
  color: #000000;
}

/* Color base del botón Sign Up */
.btn-signup {
  background-color: #3acf41;
}

/* Efecto hover del botón Sign Up */
.btn-signup:hover {
  background-color: #2e5c31;
  color: #ffffff;
}

.contact {
  padding: 60px 80px;
  background: linear-gradient(
    180deg,
    rgba(26, 42, 29, 0.3) 0%,
    transparent 100%
  );
}

.info-principal {
  max-width: 1200px;
  margin: 0 auto;
}

.info-text {
  text-align: center;
  margin-bottom: 50px;
}

.info-text h1 {
  font-size: 42px;
  margin-bottom: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #ffffff 0%, #b3b3b3 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.info-text p {
  font-size: 18px;
  color: #b3b3b3;
  line-height: 1.6;
  max-width: 700px;
  margin: 0 auto;
}

.cards-contact {
  display: flex;
  gap: 50px;
  justify-content: center;
  flex-wrap: wrap;
  animation: fadeInUp 0.6s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card1,
.card2 {
  background: linear-gradient(135deg, #112218 0%, #1a2a1d 100%);
  padding: 40px;
  border-radius: 12px;
  box-shadow:
    0 0 30px rgba(58, 207, 65, 0.1),
    0 8px 24px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(58, 207, 65, 0.2);
  width: 100%;
  max-width: 500px;
  border: 1px solid rgba(58, 207, 65, 0.15);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.card1::before,
.card2::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(58, 207, 65, 0.3),
    transparent
  );
}

.card1:hover,
.card2:hover {
  border-color: rgba(58, 207, 65, 0.4);
  box-shadow:
    0 0 40px rgba(58, 207, 65, 0.2),
    0 12px 32px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(58, 207, 65, 0.3);
  transform: translateY(-4px);
}

.card1 h2,
.card2 h2 {
  margin-bottom: 25px;
  text-align: center;
  font-size: 24px;
  color: #ffffff;
  background: linear-gradient(135deg, #3acf41 0%, #2a9d35 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.form-group {
  margin-bottom: 22px;
}

.form-group label {
  display: block;
  margin-bottom: 10px;
  font-size: 14px;
  font-weight: 500;
  color: #b3b3b3;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 12px 15px;
  border: 1.5px solid rgba(58, 207, 65, 0.2);
  border-radius: 6px;
  background-color: rgba(26, 42, 29, 0.6);
  color: #ffffff;
  font-size: 14px;
  transition: all 0.3s ease;
  backdrop-filter: blur(4px);
}

.form-group input:hover,
.form-group textarea:hover,
.form-group select:hover {
  border-color: rgba(58, 207, 65, 0.4);
  background-color: rgba(26, 42, 29, 0.8);
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #3acf41;
  background-color: rgba(26, 42, 29, 1);
  box-shadow: 0 0 12px rgba(58, 207, 65, 0.3);
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: rgba(179, 179, 179, 0.6);
}

button[type="submit"] {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #3acf41 0%, #2a9d35 100%);
  border: none;
  border-radius: 6px;
  color: #000000;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 15px rgba(58, 207, 65, 0.3);
  position: relative;
  overflow: hidden;
}

button[type="submit"]::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.2);
  transition: left 0.3s ease;
}

button[type="submit"]:hover {
  background: linear-gradient(135deg, #2a9d35 0%, #1f7a28 100%);
  box-shadow: 0 6px 20px rgba(58, 207, 65, 0.4);
  transform: translateY(-2px);
}

button[type="submit"]:hover::before {
  left: 100%;
}

.card2 p {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
  color: #b3b3b3;
  font-size: 14px;
  transition: all 0.3s ease;
  padding: 12px 15px;
  border-radius: 6px;
  border-left: 3px solid transparent;
}

.card2 p:hover {
  border-left-color: #3acf41;
  background-color: rgba(58, 207, 65, 0.05);
  color: #ffffff;
  transform: translateX(4px);
}

.card2 p svg {
  color: #3acf41;
  min-width: 24px;
  height: 24px;
  flex-shrink: 0;
}

/* ============================================ */
/* PIE DE PÁGINA (FOOTER) */
/* ============================================ */

.footer {
  width: 100%;
  padding: 40px 60px;
  background-color: #112218;
}

.footer-content {
  margin: 0 auto;
  max-width: 1500px;
}

.footer1 {
  display: flex;
  gap: 80px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #2e5c31;
}

.footer-column1 {
  max-width: 300px;
  color: #b3b3b3;
}

.footer-column2 {
  margin-left: auto;
  color: white;
}

.footer-column3 {
  color: white;
}

.footer-column1 p {
  margin-top: 10px;
  line-height: 1.5;
  color: #b3b3b3;
}

.footer-column2 h3,
.footer-column3 h3 {
  margin-bottom: 10px;
}

.footer-column2 ul,
.footer-column3 ul {
  list-style: none;
}
.footer-column2 ul li,
.footer-column3 ul li {
  margin-bottom: 8px;
}

.footer-column2 ul li a,
.footer-column3 ul li a {
  color: #b3b3b3;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-column2 ul li a:hover,
.footer-column3 ul li a:hover {
  color: #3acf41;
}

.copyright {
  text-align: center;
  color: #b3b3b3;
  font-size: 14px;
}
</style>