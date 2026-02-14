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
    <section class="hero-section">
      <div class="story-about">
        <p>OUR STORY</p>
      </div>
      <div class="info-secction">
        <h1>Building a more accessible financial future for everyone.</h1>
        <p>
          We were born with a simple idea. Personal finance shouldn't be
          complicated or boring. We believe in empowering people to take control
          of their money with smart tools and human-centered design.
        </p>
      </div>
    </section>

    <section class="second-section">
      <div class="info">
        <h2>50K+</h2>
        <p>Active users</p>
      </div>
      <div class="info">
        <h2>12M+</h2>
        <p>Generated savings</p>
      </div>
      <div class="info">
        <h2>24/7</h2>
        <p>Customer Support</p>
      </div>
      <div class="info">
        <h2>4.9/5</h2>
        <p>App Store rating</p>
      </div>
    </section>

    <section class="third-section">
      <div class="image-section">
        <img src="../assets/Imagen2.png" alt="About Us Illustration" />
      </div>
      <div class="info2-secction">
        <span>OUR MISSION</span>
        <h1>Simplify wealth, amplify life.</h1>
        <p>
          It's not just about numbers on a screen. It's about the peace of mind
          that comes from knowing you're covered in case of unexpected events,
          or the joy of planning those dream vacations without debt. Our
          platform uses advanced technology to automate the boring stuff and
          give you clear insights on what matters, allowing you to focus on
          living your life while your money works for you.
        </p>
        <div class="text-bold">
          <div class="text-bold1">
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M14 12C14 13.1046 13.1046 14 12 14C10.8954 14 10 13.1046 10 12C10 10.8954 10.8954 10 12 10C13.1046 10 14 10.8954 14 12Z"
                fill="currentColor"
              />
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M12 3C6.40848 3 1.71018 6.82432 0.378052 12C1.71018 17.1757 6.40848 21 12 21C17.5915 21 22.2898 17.1757 23.6219 12C22.2898 6.82432 17.5915 3 12 3ZM16 12C16 14.2091 14.2091 16 12 16C9.79086 16 8 14.2091 8 12C8 9.79086 9.79086 8 12 8C14.2091 8 16 9.79086 16 12Z"
                fill="currentColor"
              />
            </svg>
            <h3>Transparency</h3>
            <p>No small print or hidden costs. Total transparency.</p>
          </div>
          <div class="text-bold1">
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
            <h3>Security</h3>
            <p>Your data is yours. Protected with the highest standard.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="fourth-section">
      <div class="info3-secction">
        <h1>The team behind the magic</h1>
        <p>
          We are a diverse group of engineers, designers, and financial experts
          united by one passion: improving global financial health.
        </p>
      </div>
      <div class="cards">
        <div class="card">
          <img src="../assets/Imagen3.png" alt="Persona 1" />
          <h3>Jonathan Rosas</h3>
          <p>CEO & Founder</p>
        </div>
        <div class="card">
          <img src="../assets/Imagen4.png" alt="Persona 2" />
          <h3>Heidy Rios</h3>
          <p>CTO & Co-Founder</p>
        </div>
        <div class="card">
          <img src="../assets/Imagen5.png" alt="Persona 3" />
          <h3>Ana Rosas</h3>
          <p>Marketing Director</p>
        </div>
      </div>
    </section>

    <section class="fifth-section">
      <div class="info4-section">
        <div class="info-left">
          <h1>Our values</h1>
          <p>
            These principles guide every decision we make, from the code we
            write to how we respond to your emails.
          </p>
          <router-link to="/register" class="unete-btn">
            Join the team ->
          </router-link>
        </div>
        <div class="info-right">
          <div class="infos">
            <h3>User first, always</h3>
            <p>
              We don't design for banks; we design for people. Every feature
              comes from a real need of our users.
            </p>
          </div>
          <div class="infos">
            <h3>Radical simplicity</h3>
            <p>
              Finance is complex; our tool is not. We work hard to distill
              complexity into simple experiences.
            </p>
          </div>
          <div class="infos">
            <h3>Continuous improvement</h3>
            <p>
              We never finish. Let’s constantly learn, iterate, and improve our
              platform and processes.
            </p>
          </div>
        </div>
      </div>

      <div class="card-section2">
        <h1>Ready to be part of our story?</h1>
        <p>
          Start today to write the next chapter of your financial life with
          Finances Pro.
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

.story-about {
  color: #3acf41;
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 10px;
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

/* Contenedor principal de la segunda sección */
.second-section {
  display: flex;
  padding: 60px 80px;
  align-items: center;
  justify-content: center;
  width: 100%;
  gap: 60px;
  flex-wrap: wrap;
}

.info {
  text-align: center;
  flex: 1;
  min-width: 200px;
  max-width: 250px;
}

.info h2 {
  font-size: 36px;
  margin-bottom: 10px;
}

.info p {
  font-size: 18px;
  color: #d1d5db;
}

.third-section {
  display: flex;
  flex-direction: row;
  padding: 60px 80px;
  align-items: center;
  justify-content: center;
  width: 100%;
  background-color: #112218;
}

.image-section img {
  width: 500px;
  height: auto;
  margin-right: 60px;
}

.info2-secction {
  max-width: 600px;
}

.info2-secction span {
  color: #3acf41;
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 10px;
  display: inline-block;
}

.info2-secction h1 {
  font-size: 42px;
  margin-bottom: 20px;
}

.info2-secction p {
  font-size: 20px;
  line-height: 1.6;
  font-weight: 600;
  margin-bottom: 10px;
  color: #d1d5db;
}

.text-bold {
  display: flex;
  flex-direction: row;
  gap: 20px;
  margin-top: 20px;
}

.text-bold1 {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 10px;
}
.text-bold1 h3 {
  font-size: 22px;
  margin-top: 10px;
}

.text-bold1 p {
  font-size: 16px;
  color: #d1d5db;
}

.text-bold1 svg {
  color: #3acf41;
  margin-right: 12px;
  vertical-align: middle;
  flex-shrink: 0;
}

.fourth-section {
  display: flex;
  flex-direction: column;
  padding: 60px 80px;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.info3-secction {
  text-align: center;
  max-width: 800px;
  margin-bottom: 40px;
  gap: 20px;
}

.info3-secction h1 {
  font-size: 42px;
  margin-bottom: 20px;
}

.info3-secction p {
  font-size: 20px;
  line-height: 1.6;
  color: #d1d5db;
}

.cards {
  display: flex;
  gap: 40px;
  justify-content: center;
  align-items: flex-start;
  flex-wrap: wrap;
}

.card {
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid #2e5c31;
  border-radius: 12px;
  overflow: hidden;
  width: 280px;
  background-color: #1a3a1e;
}

.card img {
  width: 100%;
  height: 280px;
  object-fit: cover;
  display: block;
}

.card h3 {
  font-size: 20px;
  margin-top: 16px;
  color: #ffffff;
}

.card p {
  font-size: 16px;
  color: #3acf41;
  margin-bottom: 16px;
}

.card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: translateY(-5px);
  transition: all 0.3s ease;
}

.fifth-section {
  display: flex;
  flex-direction: column;
  padding: 60px 80px;
  align-items: center;
  justify-content: center;
  width: 100%;
  background-color: #112218;
}

.info4-section {
  display: flex;
  flex-direction: row;
  width: 100%;
  max-width: 1200px;
  margin-bottom: 40px;
}

.info-left {
  flex: 1;
  margin-right: 40px;
}

.info-left h1 {
  font-size: 36px;
  margin-bottom: 20px;
}

.info-left p {
  font-size: 18px;
  line-height: 1.5;
  margin-bottom: 20px;
  color: #d1d5db;
}

.unete-btn {
  color: #3acf41;
  text-decoration: none;
  font-size: 16px;
}

.info-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.infos h3 {
  font-size: 22px;
  margin-bottom: 10px;
}

.infos p {
  font-size: 16px;
  line-height: 1.5;
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

/* Pantallas grandes - Ajustes finos */
@media (max-width: 1200px) {
  header {
    padding: 0 20px;
  }

  .second-section {
    gap: 50px;
    padding: 60px 40px;
  }

  .third-section {
    padding: 60px 40px;
  }

  .image-section img {
    width: 400px;
    margin-right: 40px;
  }

  .fourth-section {
    padding: 60px 40px;
  }

  .fifth-section {
    padding: 60px 40px;
  }

  .footer {
    padding: 30px 40px;
  }

  .footer1 {
    gap: 40px;
  }
}

/* Tablets grandes y pantallas medianas */
@media (max-width: 992px) {
  header {
    padding: 0 15px;
  }

  .nav-link {
    gap: 10px;
  }

  .nav-item {
    font-size: 16px;
    padding: 8px 10px;
  }

  .btn-login,
  .btn-signup {
    padding: 8px 30px;
    font-size: 14px;
  }

  .hero-section {
    padding: 40px 30px;
  }

  .info-secction h1 {
    font-size: 40px;
    margin-bottom: 15px;
  }

  .info-secction p {
    font-size: 18px;
  }

  .second-section {
    gap: 40px;
    padding: 40px 30px;
  }

  .info {
    flex: 0 1 calc(50% - 20px);
    min-width: 150px;
  }

  .info h2 {
    font-size: 28px;
  }

  .info p {
    font-size: 16px;
  }

  .third-section {
    flex-direction: column;
    text-align: center;
    padding: 40px 30px;
  }

  .image-section img {
    margin-right: 0;
    margin-bottom: 30px;
    width: 100%;
    max-width: 350px;
  }

  .info2-secction {
    max-width: 100%;
  }

  .info2-secction h1 {
    font-size: 36px;
  }

  .text-bold {
    gap: 15px;
  }

  .cards {
    gap: 30px;
  }

  .info3-secction h1 {
    font-size: 36px;
  }

  .info4-section {
    flex-direction: column;
    text-align: center;
  }

  .info-left {
    margin-right: 0;
    margin-bottom: 20px;
  }

  .info-left h1 {
    font-size: 32px;
  }

  .fourth-section,
  .fifth-section {
    padding: 40px 30px;
  }

  .footer {
    padding: 30px 20px;
  }

  .footer1 {
    gap: 40px;
  }
}

/* Tablets pequeñas */
@media (max-width: 768px) {
  header {
    height: 70px;
    padding: 0 15px;
  }

  .nav-link {
    gap: 8px;
  }

  .nav-item {
    font-size: 15px;
    padding: 6px 8px;
  }

  .btn-login,
  .btn-signup {
    padding: 8px 25px;
    font-size: 13px;
  }

  .hero-section {
    padding: 30px 20px;
  }

  .info-secction h1 {
    font-size: 32px;
    margin-bottom: 12px;
  }

  .info-secction p {
    font-size: 16px;
  }

  .second-section {
    gap: 30px;
    padding: 30px 20px;
  }

  .info {
    flex: 0 1 calc(50% - 15px);
    min-width: 140px;
    max-width: 100%;
  }

  .info h2 {
    font-size: 24px;
    margin-bottom: 8px;
  }

  .info p {
    font-size: 14px;
  }

  .image-section img {
    max-width: 280px;
    margin-bottom: 20px;
  }

  .info2-secction h1 {
    font-size: 30px;
    margin-bottom: 15px;
  }

  .info2-secction p {
    font-size: 16px;
  }

  .text-bold {
    flex-direction: column;
    gap: 15px;
  }

  .text-bold1 h3 {
    font-size: 18px;
  }

  .text-bold1 p {
    font-size: 14px;
  }

  .cards {
    gap: 20px;
    flex-wrap: wrap;
  }

  .card {
    width: 100%;
    max-width: 250px;
  }

  .info3-secction h1 {
    font-size: 30px;
    margin-bottom: 15px;
  }

  .info-left h1 {
    font-size: 28px;
    margin-bottom: 15px;
  }

  .card-section2 {
    padding: 30px 20px;
  }

  .card-section2 h1 {
    font-size: 28px;
  }

  .card-section2 p {
    font-size: 16px;
  }

  .fourth-section,
  .fifth-section {
    padding: 30px 20px;
  }

  .footer {
    padding: 25px 15px;
  }

  .footer1 {
    gap: 30px;
    margin-bottom: 15px;
  }
}

/* Dispositivos móviles - Pantallas medianas */
@media (max-width: 600px) {
  header {
    height: auto;
    padding: 10px 12px;
    flex-wrap: wrap;
    justify-content: space-between;
  }

  .logo {
    font-size: 18px;
  }

  .logo-icon img {
    width: 40px;
    height: 40px;
  }

  .nav-link {
    display: none;
  }

  .header-botoms {
    flex-direction: column;
    gap: 6px;
    width: 100%;
    margin-top: 8px;
  }

  .btn-login,
  .btn-signup {
    padding: 8px 20px;
    font-size: 13px;
    width: 100%;
    text-align: center;
  }

  .hero-section {
    padding: 20px 15px;
  }

  .story-about {
    font-size: 14px;
    margin-bottom: 8px;
  }

  .info-secction h1 {
    font-size: 24px;
    margin-bottom: 10px;
  }

  .info-secction p {
    font-size: 14px;
    line-height: 1.5;
  }

  .second-section {
    flex-direction: column;
    gap: 20px;
    padding: 25px 15px;
  }

  .info {
    flex: 0 1 100%;
    min-width: 100%;
    max-width: 100%;
  }

  .info h2 {
    font-size: 20px;
    margin-bottom: 6px;
  }

  .info p {
    font-size: 13px;
  }

  .third-section {
    padding: 25px 15px;
  }

  .image-section img {
    width: 100%;
    max-width: 200px;
    margin-bottom: 15px;
  }

  .info2-secction h1 {
    font-size: 24px;
    margin-bottom: 12px;
  }

  .info2-secction p {
    font-size: 14px;
  }

  .text-bold {
    flex-direction: column;
    gap: 12px;
  }

  .text-bold1 h3 {
    font-size: 16px;
    margin-top: 6px;
  }

  .text-bold1 p {
    font-size: 12px;
  }

  .text-bold1 svg {
    width: 20px;
    height: 20px;
    margin-right: 8px;
  }

  .fourth-section {
    padding: 25px 15px;
  }

  .info3-secction h1 {
    font-size: 24px;
    margin-bottom: 12px;
  }

  .info3-secction p {
    font-size: 14px;
  }

  .cards {
    gap: 15px;
    flex-direction: column;
    align-items: center;
  }

  .card {
    width: 100%;
    max-width: 220px;
  }

  .card h3 {
    font-size: 16px;
  }

  .card p {
    font-size: 14px;
  }

  .fifth-section {
    padding: 25px 15px;
  }

  .info4-section {
    flex-direction: column;
    text-align: center;
    margin-bottom: 20px;
  }

  .info-left h1 {
    font-size: 22px;
    margin-bottom: 12px;
  }

  .info-left p {
    font-size: 14px;
    margin-bottom: 15px;
  }

  .infos h3 {
    font-size: 16px;
    margin-bottom: 8px;
  }

  .infos p {
    font-size: 13px;
  }

  .card-section2 {
    padding: 20px 12px;
  }

  .card-section2 h1 {
    font-size: 20px;
  }

  .card-section2 p {
    font-size: 13px;
  }

  .btn-creat-account {
    padding: 10px 20px;
    font-size: 14px;
    max-width: 200px;
  }

  .footer {
    padding: 20px 12px;
  }

  .footer1 {
    flex-direction: column;
    gap: 20px;
    margin-bottom: 15px;
  }

  .footer-column1,
  .footer-column2,
  .footer-column3 {
    max-width: 100%;
  }

  .footer-column2 {
    margin-left: 0;
  }

  .footer-column1 p {
    font-size: 13px;
  }

  .footer-column2 h3,
  .footer-column3 h3 {
    font-size: 14px;
  }

  .copyright {
    font-size: 12px;
    margin-top: 10px;
  }
}

/* Dispositivos móviles muy pequeños */
@media (max-width: 400px) {
  .logo {
    font-size: 16px;
  }

  .logo-icon img {
    width: 35px;
    height: 35px;
  }

  .logo span {
    margin-left: 6px;
  }

  .info-secction h1 {
    font-size: 20px;
  }

  .info-secction p {
    font-size: 12px;
  }

  .info h2 {
    font-size: 18px;
  }

  .info p {
    font-size: 12px;
  }

  .info2-secction h1 {
    font-size: 20px;
  }

  .info2-secction span {
    font-size: 14px;
  }

  .info3-secction h1 {
    font-size: 20px;
  }

  .info-left h1 {
    font-size: 18px;
  }

  .card-section2 h1 {
    font-size: 18px;
  }

  .footer-column1 {
    font-size: 12px;
  }
}
</style>