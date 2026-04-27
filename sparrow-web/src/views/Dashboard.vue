<template>
  <div class="page">
    <h1 class="page-title">📊 Dashboard</h1>
    <div class="grid">
      <div class="card stat-card">
        <div class="stat-icon">🖥️</div>
        <div class="stat-info">
          <span class="stat-label">CPU</span>
          <span class="stat-value">{{ stats.cpu }}%</span>
        </div>
      </div>
      <div class="card stat-card">
        <div class="stat-icon">🧠</div>
        <div class="stat-info">
          <span class="stat-label">Memory</span>
          <span class="stat-value">{{ stats.memory }}%</span>
        </div>
      </div>
      <div class="card stat-card">
        <div class="stat-icon">💾</div>
        <div class="stat-info">
          <span class="stat-label">Disk</span>
          <span class="stat-value">{{ stats.disk }}%</span>
        </div>
      </div>
      <div class="card stat-card">
        <div class="stat-icon">🔌</div>
        <div class="stat-info">
          <span class="stat-label">Agent</span>
          <span class="stat-value status" :class="stats.agentStatus">{{ stats.agentStatus }}</span>
        </div>
      </div>
    </div>

    <div class="card" style="margin-top: 24px;">
      <h2 style="margin-bottom: 16px;">System Health</h2>
      <div class="health-row">
        <span>🤖 LLM Provider</span>
        <span class="status disconnected">Unconfigured</span>
      </div>
      <div class="health-row">
        <span>🐦 Local Agent</span>
        <span class="status disconnected">Disconnected</span>
      </div>
      <div class="health-row">
        <span>💬 Telegram Bot</span>
        <span class="status disconnected">Unconfigured</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'

const stats = reactive({
  cpu: '--',
  memory: '--',
  disk: '--',
  agentStatus: 'disconnected' as 'connected' | 'disconnected',
})
</script>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon { font-size: 32px; }
.stat-label { display: block; font-size: 13px; color: #888; }
.stat-value { display: block; font-size: 24px; font-weight: 600; color: #fff; }

.status { font-size: 14px; font-weight: 500; }
.status.connected { color: #4ade80; }
.status.disconnected { color: #f87171; }

.health-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #2a2a2e;
}
.health-row:last-child { border-bottom: none; }
</style>
