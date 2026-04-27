<template>
  <div class="chat-view">
    <div class="chat-messages" ref="messagesRef">
      <div v-if="messages.length === 0" class="empty-state">
        <div class="empty-icon">🐦</div>
        <h2>Welcome to OpenSparrow</h2>
        <p>Ask me to manage files, run commands, or check system status.</p>
        <div class="suggestions">
          <button class="btn btn-ghost" @click="sendMessage('Show system status')">📊 System status</button>
          <button class="btn btn-ghost" @click="sendMessage('List files in workspace')">📁 List files</button>
          <button class="btn btn-ghost" @click="sendMessage('What can you do?')">❓ What can you do?</button>
        </div>
      </div>
      <div v-for="msg in messages" :key="msg.id" :class="['message', msg.from]">
        <div class="message-avatar">{{ msg.from === 'user' ? '👤' : '🐦' }}</div>
        <div class="message-body">
          <div class="message-content">{{ msg.content }}</div>
          <div class="message-time">{{ formatTime(msg.timestamp) }}</div>
        </div>
      </div>
    </div>
    <div class="chat-input">
      <textarea
        v-model="input"
        @keydown.enter.prevent="sendMessage()"
        placeholder="Ask OpenSparrow anything..."
        rows="1"
      />
      <button class="btn btn-primary" @click="sendMessage()" :disabled="!input.trim()">
        Send
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'

interface Message {
  id: number
  from: 'user' | 'sparrow'
  content: string
  timestamp: Date
}

const messages = ref<Message[]>([])
const input = ref('')
const messagesRef = ref<HTMLElement>()
let msgId = 0

function formatTime(date: Date): string {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

async function sendMessage(text?: string) {
  const content = text || input.value.trim()
  if (!content) return

  messages.value.push({ id: ++msgId, from: 'user', content, timestamp: new Date() })
  input.value = ''

  await nextTick()
  scrollToBottom()

  // Simulated response (will connect to WebSocket)
  setTimeout(() => {
    messages.value.push({
      id: ++msgId,
      from: 'sparrow',
      content: `🐦 Received: "${content}"\n\nThis is a placeholder — the agent backend will handle this in the full implementation.`,
      timestamp: new Date(),
    })
    nextTick(() => scrollToBottom())
  }, 500)
}

function scrollToBottom() {
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}
</script>

<style scoped>
.chat-view {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
  text-align: center;
  gap: 12px;
}

.empty-icon { font-size: 64px; }
.empty-state h2 { color: #fff; font-size: 24px; }
.empty-state p { color: #888; max-width: 400px; }

.suggestions {
  display: flex;
  gap: 8px;
  margin-top: 16px;
  flex-wrap: wrap;
  justify-content: center;
}

.message {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  max-width: 80%;
}

.message.user { margin-left: auto; flex-direction: row-reverse; }

.message-avatar { font-size: 24px; flex-shrink: 0; }

.message-body { display: flex; flex-direction: column; gap: 4px; }

.message-content {
  background: #1a1a1e;
  border: 1px solid #2a2a2e;
  border-radius: 12px;
  padding: 12px 16px;
  white-space: pre-wrap;
  line-height: 1.5;
}

.message.user .message-content {
  background: #2563eb;
  border-color: #2563eb;
  color: #fff;
}

.message-time {
  font-size: 11px;
  color: #666;
  padding: 0 4px;
}

.message.user .message-time { text-align: right; }

.chat-input {
  display: flex;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #2a2a2e;
  background: #1a1a1e;
}

.chat-input textarea {
  flex: 1;
  resize: none;
  min-height: 40px;
}
</style>
