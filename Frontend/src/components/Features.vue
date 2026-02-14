<template>
  <div class="home-container">
    <!-- Header -->
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
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="new-features">
        <p>New features</p>
      </div>
      <div class="info-secction">
        <h1>Powerful features for modern finance</h1>
        <p>
          Explore the set of tools designed to simplify every aspect of your
          financial life, from your daily budget to your future wealth.
        </p>
      </div>
    </section>

    <!-- Additional Sections -->
    <section class="second-section">
      <div class="card-infos">
        <div class="cards">
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
              d="M12 0C5.37258 0 0 5.37258 0 12C0 18.6274 5.37258 24 12 24C18.6274 24 24 18.6274 24 12C24 5.37258 18.6274 0 12 0ZM4.14355 13.5165C4.85219 17.2096 8.10023 20 12 20C16.4183 20 20 16.4183 20 12C20 7.58172 16.4183 4 12 4C8.0886 4 4.83283 6.80704 4.13728 10.5165L6.72824 10.5071C7.37819 8.20738 9.49236 6.52222 12.0001 6.52222C15.0254 6.52222 17.4779 8.9747 17.4779 12C17.4779 15.0253 15.0254 17.4778 12.0001 17.4778C9.49752 17.4778 7.3869 15.7995 6.73228 13.5071L4.14355 13.5165ZM9.52234 12C9.52234 13.3684 10.6317 14.4778 12.0001 14.4778C13.3685 14.4778 14.4779 13.3684 14.4779 12C14.4779 10.6316 13.3685 9.52222 12.0001 9.52222C10.6317 9.52222 9.52234 10.6316 9.52234 12Z"
              fill="currentColor"
            />
          </svg>
          <h2>Dynamic Budgets</h2>
          <p>
            Create spending limits that automatically adjust to your monthly
            income. Receive alerts before you go over budget.
          </p>
        </div>
        <div class="cards">
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
              d="M5 4H19C19.5523 4 20 4.44771 20 5V19C20 19.5523 19.5523 20 19 20H5C4.44772 20 4 19.5523 4 19V5C4 4.44772 4.44771 4 5 4ZM2 5C2 3.34315 3.34315 2 5 2H19C20.6569 2 22 3.34315 22 5V19C22 20.6569 20.6569 22 19 22H5C3.34315 22 2 20.6569 2 19V5ZM12 12C9.23858 12 7 9.31371 7 6H9C9 8.56606 10.6691 10 12 10C13.3309 10 15 8.56606 15 6H17C17 9.31371 14.7614 12 12 12Z"
              fill="currentColor"
            />
          </svg>
          <h2>Bank Synchronization</h2>
          <p>
            Securely connect your accounts from over 50 banks. Your transactions
            are imported and categorized automatically.
          </p>
        </div>
        <div class="cards">
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
              d="M15 8H19V20H5V10H9V4H15V8ZM13 6H11V18H13V6ZM15 10V18H17V10H15ZM9 12V18H7V12H9Z"
              fill="currentColor"
            />
          </svg>
          <h2>Real-Time Investments</h2>
          <p>
            View the performance of your stocks, cryptocurrencies, and funds in
            a single unified dashboard.
          </p>
        </div>
        <div class="cards">
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path d="M7 18H17V16H7V18Z" fill="currentColor" />
            <path d="M17 14H7V12H17V14Z" fill="currentColor" />
            <path d="M7 10H11V8H7V10Z" fill="currentColor" />
            <path
              fill-rule="evenodd"
              clip-rule="evenodd"
              d="M6 2C4.34315 2 3 3.34315 3 5V19C3 20.6569 4.34315 22 6 22H18C19.6569 22 21 20.6569 21 19V9C21 5.13401 17.866 2 14 2H6ZM6 4H13V9H19V19C19 19.5523 18.5523 20 18 20H6C5.44772 20 5 19.5523 5 19V5C5 4.44772 5.44772 4 6 4ZM15 4.10002C16.6113 4.4271 17.9413 5.52906 18.584 7H15V4.10002Z"
              fill="currentColor"
            />
          </svg>
          <h2>Receipt Scanner</h2>
          <p>
            Take a photo of your receipts and our AI will extract the relevant
            data for your financial records.
          </p>
        </div>
        <div class="cards">
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
          <h2>Shared Finances</h2>
          <p>
            Manage household expenses with your partner or roommates without
            mixing personal accounts.
          </p>
        </div>
        <div class="cards">
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
              d="M18 10.5C19.6569 10.5 21 11.8431 21 13.5V19.5C21 21.1569 19.6569 22.5 18 22.5H6C4.34315 22.5 3 21.1569 3 19.5V13.5C3 11.8431 4.34315 10.5 6 10.5V7.5C6 4.18629 8.68629 1.5 12 1.5C15.3137 1.5 18 4.18629 18 7.5V10.5ZM12 3.5C14.2091 3.5 16 5.29086 16 7.5V10.5H8V7.5C8 5.29086 9.79086 3.5 12 3.5ZM18 12.5H6C5.44772 12.5 5 12.9477 5 13.5V19.5C5 20.0523 5.44772 20.5 6 20.5H18C18.5523 20.5 19 20.0523 19 19.5V13.5C19 12.9477 18.5523 12.5 18 12.5Z"
              fill="currentColor"
            />
          </svg>
          <h2>Biometric Security</h2>
          <p>
            Protected access with Face ID or fingerprint. Your data is encrypted
            using military-grade standards (AES-256).
          </p>
        </div>
      </div>
    </section>

    <section class="third-section">
      <div class="card-section">
        <div class="info2-secction">
          <h1>Understand where every penny goes.</h1>
          <p>
            Our monthly reports not only show you numbers, they tell you a
            story. Identify consumption patterns, detect forgotten
            subscriptions, and find savings opportunities you didn’t know
            existed.
          </p>

          <p>
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M10.2426 16.3137L6 12.071L7.41421 10.6568L10.2426 13.4853L15.8995 7.8284L17.3137 9.24262L10.2426 16.3137Z"
                fill="currentColor"
              />
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M1 12C1 5.92487 5.92487 1 12 1C18.0751 1 23 5.92487 23 12C23 18.0751 18.0751 23 12 23C5.92487 23 1 18.0751 1 12ZM12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12C21 16.9706 16.9706 21 12 21Z"
                fill="currentColor"
              />
            </svg>
            Month-to-month comparison
          </p>
          <p>
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M10.2426 16.3137L6 12.071L7.41421 10.6568L10.2426 13.4853L15.8995 7.8284L17.3137 9.24262L10.2426 16.3137Z"
                fill="currentColor"
              />
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M1 12C1 5.92487 5.92487 1 12 1C18.0751 1 23 5.92487 23 12C23 18.0751 18.0751 23 12 23C5.92487 23 1 18.0751 1 12ZM12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12C21 16.9706 16.9706 21 12 21Z"
                fill="currentColor"
              />
            </svg>
            Projection of future expenses
          </p>
          <p>
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M10.2426 16.3137L6 12.071L7.41421 10.6568L10.2426 13.4853L15.8995 7.8284L17.3137 9.24262L10.2426 16.3137Z"
                fill="currentColor"
              />
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M1 12C1 5.92487 5.92487 1 12 1C18.0751 1 23 5.92487 23 12C23 18.0751 18.0751 23 12 23C5.92487 23 1 18.0751 1 12ZM12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12C21 16.9706 16.9706 21 12 21Z"
                fill="currentColor"
              />
            </svg>
            Export to Excel and PDF
          </p>
        </div>
        <div class="image-section">
          <img src="../assets/Imagen6.png" alt="Hero Image" />
        </div>
      </div>
    </section>
    <section class="fourth-section">
      <div class="card3-section">
        <div class="images-section">
          <img src="../assets/Imagen7.png" alt="Feature Image 1" />
          <img src="../assets/Imagen8.png" alt="Feature Image 2" />
        </div>

        <div class="info3-secction">
          <h1>Turn your dreams into an achievable plan.</h1>
          <p>
            Define what you’re saving for and let FinanzasPro calculate how much
            you need to set aside each month. Visualize your goal timeline and
            celebrate every milestone along the way.
          </p>
        </div>
      </div>
      <div class="card-section2">
        <h1>Ready to take control?</h1>
        <p>
          All these features are just a click away. Start your 30-day free trial
          today.
        </p>
        <router-link to="/register" class="btn-creat-account">
          Create a free account
        </router-link>
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

<script setup>
// No script logic needed for this component
</script>

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

/* ============================================ */
/* SECCIÓN HERO (PRINCIPAL) */
/* ============================================ */

/* Contenedor principal de la sección hero */
.hero-section {
  display: flex;
  padding: 40px 60px;
  background-color: #112218;
  align-items: center;
  justify-content: center;
  width: 100%;
  flex-direction: column;
}

.new-features p {
  color: #3acf41;
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 10px;
  border: white 0.1px solid;
  padding: 5px 10px;
  border-radius: 50px;
}

.info-secction {
  text-align: center;
  max-width: 800px;
  margin-top: 20px;
  gap: 20px;
}

.info-secction h1 {
  font-size: 48px;
  margin-bottom: 20px;
}

.info-secction p {
  font-size: 20px;
  line-height: 1.6;
  color: #d1d5db;
}

/* ============================================ */
/* SEGUNDA SECCIÓN (CARACTERÍSTICAS) */
/* ============================================ */

/* Contenedor principal de la segunda sección */
.second-section {
  display: flex;
  padding: 60px 80px;
  align-items: center;
  justify-content: center;
  width: 100%;
}

/* Contenedor de las tarjetas de características */
.card-infos {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  max-width: 1200px;
}

/* Tarjetas individuales (Expense Tracking, Investment, Savings) */
.cards {
  background-color: #112218;
  border: 1px solid #2e5c31;
  border-radius: 8px;
  padding: 20px;
  text-align: left;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.cards svg {
  color: #3acf41;
  margin-right: 12px;
  vertical-align: middle;
  flex-shrink: 0;
}

/* Efecto hover de las tarjetas con sombra y movimiento */
.cards:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  transform: translateY(-5px);
  transition: all 0.3s ease;
}

/* Títulos de las tarjetas */
.cards h2 {
  font-size: 24px;
  margin: 15px 0;
  text-align: left;
}

/* Descripción de las tarjetas */
.cards p {
  font-size: 16px;
  line-height: 1.4;
  text-align: left;
}
/* Contenedor principal de la tercera sección */
.third-section {
  display: flex;
  flex-direction: column;
  padding: 60px 80px;
  align-items: center;
  justify-content: center;
  width: 100%;
  background-color: #112218;
}

/* Contenedor con el texto y la imagen de la sección hero */
.card-section {
  display: flex;
  gap: 60px;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px;
}

/* Sección izquierda: Título, descripción y botón de crear cuenta */
.info2-secction {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  max-width: 500px;
  gap: 20px;
  justify-content: center;
  text-align: left;
}

/* Título principal de la sección hero */
.info2-secction h1 {
  font-size: 48px;
  font-weight: bold;
  line-height: 1.2;
}

/* Párrafo de descripción en la sección hero */
.info2-secction p {
  font-size: 18px;
  line-height: 1.6;
  color: #d1d5db;
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Alineación de checkmarks con texto */
.info2-secction p svg {
  color: #3acf41;
  margin-right: 12px;
  vertical-align: middle;
  flex-shrink: 0;
}

/* Sección derecha: Imagen de la sección hero */
.image-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Imagen de la sección hero con borde */
.image-section img {
  width: 100%;
  max-width: 450px;
  border-radius: 15px;
  border: #3acf41 solid 2px;
  object-fit: contain;
}

.fourth-section {
  display: flex;
  flex-direction: column;
  padding: 60px 80px;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.card3-section {
  display: flex;
  gap: 60px;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px;
}

.images-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 40px;
  flex: 1;
}

.images-section img {
  width: 100%;
  border-radius: 15px;
  object-fit: contain;
}

.info3-secction {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  max-width: 500px;
  gap: 20px;
  justify-content: center;
  text-align: left;
}

.info3-secction h1 {
  font-size: 48px;
  font-weight: bold;
  line-height: 1.2;
}

.info3-secction p {
  font-size: 18px;
  line-height: 1.6;
  color: #d1d5db;
}

/* Tarjeta final de llamada a la acción */
.card-section2 {
  display: flex;
  flex-direction: column;
  gap: 20px;
  justify-content: center;
  align-items: center;
  text-align: center;
  background-color: #173122;
  padding: 40px;
  border: 1px solid #2e5c31;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Título de la tarjeta final */
.card-section2 h1 {
  font-size: 36px;
  font-weight: bold;
}

/* Descripción de la tarjeta final */
.card-section2 p {
  font-size: 18px;
  line-height: 1.5;
}

.btn-creat-account {
  display: inline-block;
  padding: 12px 30px;
  background-color: #3acf41;
  max-width: 250px;
  color: #000000;
  text-decoration: none;
  font-size: 18px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

/* Efecto hover del botón crear cuenta */
.btn-creat-account:hover {
  background-color: #2e5c31;
  color: #ffffff;
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

/* ============================================ */
/* MEDIA QUERIES - RESPONSIVIDAD */
/* ============================================ */

/* Pantallas XL - Ajustes finos */
@media (max-width: 1400px) {
  .card-section,
  .card3-section {
    gap: 50px;
  }

  .second-section {
    padding: 50px 60px;
  }

  .fourth-section {
    padding: 50px 60px;
  }

  .images-section {
    gap: 15px;
  }
}

/* Pantallas grandes */
@media (max-width: 1200px) {
  header {
    padding: 0 20px;
  }

  .hero-section {
    padding: 40px 40px;
  }

  .second-section {
    padding: 40px 40px;
  }

  .third-section {
    padding: 40px 40px;
  }

  .fourth-section {
    padding: 40px 40px;
  }

  .info-secction h1 {
    font-size: 40px;
  }

  .info2-secction h1,
  .info3-secction h1 {
    font-size: 40px;
  }

  .card-infos {
    gap: 25px;
  }

  .footer {
    padding: 30px 40px;
  }

  .footer1 {
    gap: 60px;
  }
}

/* Tablets */
@media (max-width: 1024px) {
  header {
    padding: 0 15px;
  }

  .nav-link {
    gap: 12px;
  }

  .nav-item {
    font-size: 15px;
    padding: 8px 10px;
  }

  .btn-login,
  .btn-signup {
    padding: 8px 20px;
    font-size: 13px;
  }

  .hero-section {
    padding: 30px 30px;
  }

  .info-secction h1 {
    font-size: 36px;
    margin-bottom: 15px;
  }

  .info-secction p {
    font-size: 18px;
  }

  .new-features p {
    font-size: 16px;
  }

  .second-section {
    padding: 35px 30px;
  }

  .card-infos {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }

  .cards h2 {
    font-size: 20px;
  }

  .cards p {
    font-size: 15px;
  }

  .third-section {
    padding: 35px 30px;
  }

  .card-section {
    gap: 40px;
  }

  .info2-secction h1 {
    font-size: 36px;
  }

  .info2-secction p {
    font-size: 16px;
  }

  .image-section img {
    max-width: 350px;
  }

  .fourth-section {
    padding: 35px 30px;
  }

  .card3-section {
    gap: 40px;
  }

  .info3-secction h1 {
    font-size: 36px;
  }

  .info3-secction p {
    font-size: 16px;
  }

  .images-section {
    gap: 15px;
  }

  .card-section2 {
    padding: 30px 25px;
  }

  .card-section2 h1 {
    font-size: 28px;
  }

  .card-section2 p {
    font-size: 16px;
  }

  .btn-creat-account {
    padding: 10px 25px;
    font-size: 16px;
  }

  .footer {
    padding: 30px 30px;
  }

  .footer1 {
    gap: 40px;
  }
}

/* Tablets medianas */
@media (max-width: 892px) {
  header {
    flex-wrap: wrap;
    height: auto;
    padding: 10px 12px;
    gap: 10px;
  }

  .logo {
    font-size: 18px;
  }

  .logo-icon img {
    width: 38px;
    height: 38px;
  }

  .nav-link {
    order: 3;
    width: 100%;
    justify-content: center;
    gap: 8px;
  }

  .nav-item {
    font-size: 13px;
    padding: 6px 8px;
  }

  .header-botoms {
    gap: 8px;
  }

  .btn-login,
  .btn-signup {
    padding: 6px 15px;
    font-size: 12px;
  }

  .hero-section {
    padding: 25px 20px;
  }

  .info-secction h1 {
    font-size: 30px;
    margin-bottom: 12px;
  }

  .info-secction p {
    font-size: 15px;
  }

  .new-features p {
    font-size: 14px;
    padding: 4px 8px;
  }

  .second-section {
    padding: 30px 20px;
  }

  .card-infos {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }

  .cards {
    padding: 15px;
  }

  .cards h2 {
    font-size: 18px;
    margin: 12px 0;
  }

  .cards p {
    font-size: 13px;
  }

  .third-section {
    padding: 30px 20px;
  }

  .card-section {
    flex-direction: column;
    gap: 25px;
    width: 100%;
  }

  .info2-secction {
    max-width: 100%;
    text-align: center;
  }

  .info2-secction h1 {
    font-size: 28px;
  }

  .info2-secction p {
    font-size: 14px;
    justify-content: center;
  }

  .image-section img {
    max-width: 100%;
    width: 100%;
    max-width: 280px;
  }

  .fourth-section {
    padding: 30px 20px;
  }

  .card3-section {
    flex-direction: column;
    gap: 25px;
    width: 100%;
  }

  .images-section {
    gap: 12px;
    order: 2;
  }

  .info3-secction {
    max-width: 100%;
    text-align: center;
    order: 1;
  }

  .info3-secction h1 {
    font-size: 28px;
  }

  .info3-secction p {
    font-size: 14px;
  }

  .card-section2 {
    padding: 25px 20px;
    margin-top: 20px;
  }

  .card-section2 h1 {
    font-size: 26px;
  }

  .card-section2 p {
    font-size: 14px;
  }

  .btn-creat-account {
    padding: 10px 20px;
    font-size: 14px;
  }

  .footer {
    padding: 25px 20px;
  }

  .footer1 {
    gap: 30px;
  }
}

/* Tablets pequeñas */
@media (max-width: 768px) {
  header {
    padding: 10px 12px;
  }

  .logo {
    font-size: 16px;
  }

  .logo-icon img {
    width: 35px;
    height: 35px;
  }

  .nav-link {
    width: 100%;
  }

  .header-botoms {
    width: 100%;
    margin-top: 8px;
  }

  .hero-section {
    padding: 20px 15px;
  }

  .info-secction h1 {
    font-size: 26px;
    margin-bottom: 10px;
  }

  .info-secction p {
    font-size: 14px;
  }

  .second-section {
    padding: 25px 15px;
  }

  .card-infos {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .cards {
    padding: 12px;
  }

  .cards h2 {
    font-size: 16px;
    margin: 10px 0;
  }

  .cards p {
    font-size: 12px;
  }

  .third-section {
    padding: 25px 15px;
  }

  .card-section {
    gap: 15px;
  }

  .info2-secction h1 {
    font-size: 24px;
    margin-bottom: 10px;
  }

  .info2-secction p {
    font-size: 13px;
  }

  .image-section img {
    max-width: 200px;
  }

  .fourth-section {
    padding: 25px 15px;
  }

  .card3-section {
    gap: 15px;
  }

  .images-section {
    gap: 10px;
  }

  .info3-secction h1 {
    font-size: 24px;
    margin-bottom: 10px;
  }

  .info3-secction p {
    font-size: 13px;
  }

  .card-section2 {
    padding: 20px 15px;
    margin-top: 15px;
  }

  .card-section2 h1 {
    font-size: 22px;
  }

  .card-section2 p {
    font-size: 12px;
  }

  .btn-creat-account {
    padding: 10px 20px;
    font-size: 13px;
    max-width: 180px;
  }

  .footer {
    padding: 20px 15px;
  }

  .footer1 {
    flex-direction: column;
    gap: 20px;
    margin-bottom: 12px;
  }

  .footer-column1 {
    max-width: 100%;
  }

  .footer-column2,
  .footer-column3 {
    margin-left: 0;
  }

  .copyright {
    font-size: 12px;
  }
}

/* Dispositivos móviles - Medianos */
@media (max-width: 600px) {
  header {
    padding: 8px 10px;
  }

  .logo {
    font-size: 14px;
  }

  .logo span {
    margin-left: 5px;
  }

  .logo-icon img {
    width: 32px;
    height: 32px;
  }

  .nav-link {
    display: none;
  }

  .header-botoms {
    width: 100%;
    gap: 4px;
    margin-top: 6px;
  }

  .btn-login,
  .btn-signup {
    padding: 7px 12px;
    font-size: 11px;
  }

  .hero-section {
    padding: 18px 12px;
  }

  .new-features p {
    font-size: 12px;
    padding: 3px 6px;
    margin-bottom: 6px;
  }

  .info-secction h1 {
    font-size: 22px;
    margin-bottom: 8px;
  }

  .info-secction p {
    font-size: 12px;
  }

  .second-section {
    padding: 20px 12px;
  }

  .card-infos {
    gap: 10px;
  }

  .cards {
    padding: 10px;
  }

  .cards h2 {
    font-size: 14px;
    margin: 8px 0;
  }

  .cards p {
    font-size: 11px;
  }

  .cards svg {
    width: 18px;
    height: 18px;
  }

  .third-section {
    padding: 20px 12px;
  }

  .card-section {
    gap: 12px;
  }

  .info2-secction h1 {
    font-size: 20px;
    margin-bottom: 8px;
  }

  .info2-secction p {
    font-size: 11px;
    gap: 6px;
  }

  .image-section img {
    max-width: 150px;
  }

  .fourth-section {
    padding: 20px 12px;
  }

  .card3-section {
    gap: 12px;
  }

  .images-section {
    gap: 8px;
  }

  .info3-secction h1 {
    font-size: 20px;
    margin-bottom: 8px;
  }

  .info3-secction p {
    font-size: 11px;
  }

  .card-section2 {
    padding: 15px 12px;
    margin-top: 12px;
    gap: 15px;
  }

  .card-section2 h1 {
    font-size: 18px;
  }

  .card-section2 p {
    font-size: 11px;
  }

  .btn-creat-account {
    padding: 8px 15px;
    font-size: 12px;
    max-width: 160px;
  }

  .footer {
    padding: 15px 10px;
  }

  .footer1 {
    gap: 15px;
    margin-bottom: 10px;
  }

  .footer-column1 p {
    font-size: 11px;
  }

  .footer-column2 h3,
  .footer-column3 h3 {
    font-size: 12px;
  }

  .footer-column2 ul li,
  .footer-column3 ul li {
    font-size: 11px;
  }

  .copyright {
    font-size: 10px;
  }
}

/* Dispositivos móviles muy pequeños */
@media (max-width: 400px) {
  .logo {
    font-size: 12px;
  }

  .logo-icon img {
    width: 28px;
    height: 28px;
  }

  .info-secction h1 {
    font-size: 18px;
    margin-bottom: 6px;
  }

  .info-secction p {
    font-size: 11px;
  }

  .cards h2 {
    font-size: 12px;
  }

  .cards p {
    font-size: 10px;
  }

  .info2-secction h1,
  .info3-secction h1 {
    font-size: 18px;
  }

  .info2-secction p,
  .info3-secction p {
    font-size: 10px;
  }

  .card-section2 h1 {
    font-size: 16px;
  }

  .card-section2 p {
    font-size: 10px;
  }

  .btn-creat-account {
    font-size: 11px;
    padding: 6px 12px;
  }

  .copyright {
    font-size: 9px;
  }
}
</style>