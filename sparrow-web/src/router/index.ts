import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Chat',
    component: () => import('../views/Chat.vue'),
  },
  {
    path: '/files',
    name: 'Files',
    component: () => import('../views/Files.vue'),
  },
  {
    path: '/tasks',
    name: 'Tasks',
    component: () => import('../views/Tasks.vue'),
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../views/Settings.vue'),
  },
  {
    path: '/setup',
    name: 'Setup',
    component: () => import('../views/SetupWizard.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
