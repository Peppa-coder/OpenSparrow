<template>
  <span :class="['health-badge', props.status]">
    <span class="dot"></span>
    {{ label }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ status: 'ok' | 'error' | 'unknown' }>()

const label = computed(() => {
  switch (props.status) {
    case 'ok': return 'Connected'
    case 'error': return 'Error'
    default: return 'Unknown'
  }
})
</script>

<style scoped>
.health-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 500;
}
.dot { width: 8px; height: 8px; border-radius: 50%; }
.ok .dot { background: #4ade80; }
.error .dot { background: #f87171; }
.unknown .dot { background: #888; }
.ok { color: #4ade80; }
.error { color: #f87171; }
.unknown { color: #888; }
</style>
