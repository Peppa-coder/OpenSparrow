<template>
  <div class="approval-card">
    <div class="approval-header">
      <span class="risk" :class="props.riskLevel">{{ props.riskLevel }}</span>
      <span class="skill">{{ props.skillName }}</span>
    </div>
    <p class="desc">{{ props.description }}</p>
    <div class="actions">
      <button class="btn btn-primary btn-sm" @click="$emit('approve')">✅ Approve</button>
      <button class="btn btn-danger btn-sm" @click="$emit('reject')">❌ Reject</button>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  skillName: string
  description: string
  riskLevel: string
}>()
defineEmits(['approve', 'reject'])
</script>

<style scoped>
.approval-card {
  background: #1a1a1e;
  border: 1px solid #2a2a2e;
  border-radius: 10px;
  padding: 16px;
  margin-bottom: 10px;
}
.approval-header { display: flex; gap: 8px; align-items: center; margin-bottom: 8px; }
.risk { padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; text-transform: uppercase; }
.risk.high { background: #dc262633; color: #f87171; }
.risk.medium { background: #d9770633; color: #fb923c; }
.risk.low { background: #16a34a33; color: #4ade80; }
.skill { color: #ccc; font-weight: 500; }
.desc { color: #999; font-size: 14px; margin-bottom: 12px; }
.actions { display: flex; gap: 8px; }
.btn-sm { padding: 6px 12px; font-size: 13px; }
</style>
