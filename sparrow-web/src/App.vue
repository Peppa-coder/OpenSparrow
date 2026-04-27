<template>
  <div class="app">
    <nav class="sidebar" v-if="!isSetup">
      <div class="logo">
        <span class="logo-icon">🐦</span>
        <span class="logo-text">OpenSparrow</span>
      </div>
      <ul class="nav-links">
        <li>
          <router-link to="/">
            <span class="nav-icon">💬</span> Chat
          </router-link>
        </li>
        <li>
          <router-link to="/files">
            <span class="nav-icon">📁</span> Files
          </router-link>
        </li>
        <li>
          <router-link to="/tasks">
            <span class="nav-icon">✅</span> Tasks
          </router-link>
        </li>
        <li>
          <router-link to="/dashboard">
            <span class="nav-icon">📊</span> Dashboard
          </router-link>
        </li>
        <li>
          <router-link to="/settings">
            <span class="nav-icon">⚙️</span> Settings
          </router-link>
        </li>
      </ul>
      <div class="nav-footer">
        <span class="version">v0.1.0</span>
      </div>
    </nav>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isSetup = computed(() => route.path === '/setup')
</script>

<style scoped>
.app {
  display: flex;
  height: 100vh;
  background: #0f0f10;
  color: #e0e0e0;
}

.sidebar {
  width: 220px;
  background: #1a1a1e;
  border-right: 1px solid #2a2a2e;
  display: flex;
  flex-direction: column;
  padding: 16px 0;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 20px 20px;
  border-bottom: 1px solid #2a2a2e;
}

.logo-icon { font-size: 24px; }
.logo-text { font-size: 18px; font-weight: 600; color: #fff; }

.nav-links {
  list-style: none;
  padding: 12px 8px;
  margin: 0;
  flex: 1;
}

.nav-links li { margin: 2px 0; }

.nav-links a {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 8px;
  color: #a0a0a0;
  text-decoration: none;
  transition: all 0.2s;
}

.nav-links a:hover { background: #2a2a2e; color: #fff; }
.nav-links a.router-link-active { background: #2563eb22; color: #60a5fa; }

.nav-icon { font-size: 16px; }

.nav-footer {
  padding: 12px 20px;
  border-top: 1px solid #2a2a2e;
}

.version { font-size: 12px; color: #666; }

.content {
  flex: 1;
  overflow: auto;
}

@media (max-width: 768px) {
  .sidebar { width: 60px; }
  .logo-text, .nav-links a span:not(.nav-icon) { display: none; }
}
</style>
