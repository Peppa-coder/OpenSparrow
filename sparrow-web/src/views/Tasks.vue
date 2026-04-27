<template>
  <div class="page">
    <h1 class="page-title">✅ Tasks & Approvals</h1>

    <div class="section">
      <h2>Pending Approvals</h2>
      <div v-if="pendingTasks.length === 0" class="card empty">
        No pending approvals. All clear! ✨
      </div>
      <div v-for="task in pendingTasks" :key="task.id" class="card task-card">
        <div class="task-header">
          <span class="risk-badge" :class="task.risk_level">{{ task.risk_level }}</span>
          <span class="task-skill">{{ task.skill_name }}</span>
        </div>
        <p class="task-desc">{{ task.description }}</p>
        <div class="task-actions">
          <button class="btn btn-primary" @click="approve(task.id)">✅ Approve</button>
          <button class="btn btn-danger" @click="reject(task.id)">❌ Reject</button>
        </div>
      </div>
    </div>

    <div class="section">
      <h2>Recent History</h2>
      <div class="card">
        <p class="empty">Task history will appear here.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Task {
  id: string
  skill_name: string
  description: string
  risk_level: string
}

const pendingTasks = ref<Task[]>([])

function approve(id: string) {
  // TODO: Call API
}

function reject(id: string) {
  // TODO: Call API
}
</script>

<style scoped>
.section { margin-bottom: 32px; }
.section h2 { font-size: 18px; margin-bottom: 12px; color: #ccc; }

.task-card { margin-bottom: 12px; }
.task-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.task-desc { color: #aaa; margin-bottom: 12px; }

.task-actions { display: flex; gap: 8px; }

.risk-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}
.risk-badge.high { background: #dc262633; color: #f87171; }
.risk-badge.medium { background: #d9770633; color: #fb923c; }
.risk-badge.low { background: #16a34a33; color: #4ade80; }

.empty { color: #666; text-align: center; padding: 20px; }
</style>
