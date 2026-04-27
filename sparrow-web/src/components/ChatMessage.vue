<template>
  <div :class="['chat-msg', props.from]">
    <div class="msg-avatar">{{ props.from === 'user' ? '👤' : '🐦' }}</div>
    <div class="msg-bubble">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ from: 'user' | 'sparrow' }>()
</script>

<style scoped>
.chat-msg {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
}
.chat-msg.user { flex-direction: row-reverse; }
.msg-avatar { font-size: 20px; }
.msg-bubble {
  background: #1a1a1e;
  border: 1px solid #2a2a2e;
  border-radius: 12px;
  padding: 10px 14px;
  max-width: 70%;
}
.chat-msg.user .msg-bubble {
  background: #2563eb;
  border-color: #2563eb;
}
</style>
