import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Features from '../components/Features.vue'
import About from '../components/About.vue'
import Contact from '../components/Contact.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import AuthSuccess from '../components/AuthSuccess.vue'
import MainPage from '../components/MainPage.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/features', name: 'Features', component: Features },
  { path: '/about', name: 'About', component: About },
  { path: '/contact', name: 'Contact', component: Contact },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/auth-success', name: 'AuthSuccess', component: AuthSuccess },
  {
    path: '/Dashboard',
    component: MainPage,
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('../components/Dashboard.vue'),
      },
      {
        path: '/budgets',
        name: 'Budgets',
        component: () => import('../components/Budgets.vue'),
      },
      {
        path: '/goals',
        name: 'Goals',
        component: () => import('../components/Goals.vue'),
      },
      {
        path: '/categories',
        name: 'Categories',
        component: () => import('../components/Categories.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
