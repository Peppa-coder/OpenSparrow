<template>
  <div class="page">
    <h1 class="page-title">⚙️ Settings</h1>

    <div class="card section">
      <h2>LLM Provider</h2>
      <div class="form-group">
        <label>Provider</label>
        <select v-model="settings.llmProvider">
          <option value="ollama">Ollama (Local)</option>
          <option value="openai">OpenAI</option>
          <option value="anthropic">Anthropic</option>
        </select>
      </div>
      <div class="form-group">
        <label>Model</label>
        <input v-model="settings.llmModel" placeholder="e.g. llama3, gpt-4o, claude-sonnet-4-20250514" />
      </div>
      <div class="form-group" v-if="settings.llmProvider !== 'ollama'">
        <label>API Key</label>
        <input v-model="settings.llmApiKey" type="password" placeholder="sk-..." />
      </div>
    </div>

    <div class="card section">
      <h2>Telegram Bot</h2>
      <div class="form-group">
        <label>Bot Token</label>
        <input v-model="settings.telegramToken" type="password" placeholder="Paste your bot token from @BotFather" />
      </div>
    </div>

    <div class="card section">
      <h2>Workspace</h2>
      <div class="form-group">
        <label>Workspace Root</label>
        <input v-model="settings.workspaceRoot" placeholder="~/sparrow-workspace" />
      </div>
    </div>

    <button class="btn btn-primary" @click="save" style="margin-top: 16px;">
      💾 Save Settings
    </button>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'

const settings = reactive({
  llmProvider: 'ollama',
  llmModel: 'llama3',
  llmApiKey: '',
  telegramToken: '',
  workspaceRoot: '~/sparrow-workspace',
})

function save() {
  // TODO: POST to /api/admin/setup
  alert('Settings saved (placeholder)')
}
</script>

<style scoped>
.section { margin-bottom: 20px; }
.section h2 { font-size: 18px; margin-bottom: 16px; color: #ccc; }

.form-group { margin-bottom: 14px; }
.form-group label {
  display: block;
  font-size: 13px;
  color: #888;
  margin-bottom: 6px;
}

select {
  background: #0f0f10;
  border: 1px solid #333;
  border-radius: 8px;
  padding: 10px 14px;
  color: #e0e0e0;
  font-size: 14px;
  width: 100%;
}
</style>
