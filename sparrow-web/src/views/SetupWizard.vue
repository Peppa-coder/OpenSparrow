<template>
  <div class="setup">
    <div class="setup-card">
      <div class="setup-header">
        <span class="setup-icon">🐦</span>
        <h1>Welcome to OpenSparrow</h1>
        <p>Let's get you set up in just a few steps.</p>
      </div>

      <div class="step" v-if="step === 1">
        <h2>Step 1: Choose your LLM</h2>
        <p class="hint">Which AI model provider would you like to use?</p>
        <div class="options">
          <button :class="['option', { active: provider === 'ollama' }]" @click="provider = 'ollama'">
            <span>🦙</span>
            <strong>Ollama</strong>
            <small>Free, runs locally</small>
          </button>
          <button :class="['option', { active: provider === 'openai' }]" @click="provider = 'openai'">
            <span>🤖</span>
            <strong>OpenAI</strong>
            <small>GPT-4o, cloud</small>
          </button>
          <button :class="['option', { active: provider === 'anthropic' }]" @click="provider = 'anthropic'">
            <span>🧠</span>
            <strong>Anthropic</strong>
            <small>Claude, cloud</small>
          </button>
        </div>
        <button class="btn btn-primary" @click="step = 2">Next →</button>
      </div>

      <div class="step" v-if="step === 2">
        <h2>Step 2: API Key</h2>
        <p class="hint" v-if="provider === 'ollama'">
          Ollama runs locally — no API key needed! Make sure Ollama is running.
        </p>
        <div v-else class="form-group">
          <label>{{ provider === 'openai' ? 'OpenAI' : 'Anthropic' }} API Key</label>
          <input v-model="apiKey" type="password" placeholder="sk-..." />
        </div>
        <div class="step-actions">
          <button class="btn btn-ghost" @click="step = 1">← Back</button>
          <button class="btn btn-primary" @click="step = 3">Next →</button>
        </div>
      </div>

      <div class="step" v-if="step === 3">
        <h2>Step 3: All Set! 🎉</h2>
        <p>Your OpenSparrow is ready to go.</p>
        <div class="summary">
          <div><strong>LLM:</strong> {{ provider }}</div>
          <div><strong>Workspace:</strong> ~/sparrow-workspace</div>
        </div>
        <div class="step-actions">
          <button class="btn btn-ghost" @click="step = 2">← Back</button>
          <button class="btn btn-primary" @click="finish">🚀 Launch OpenSparrow</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const step = ref(1)
const provider = ref('ollama')
const apiKey = ref('')

function finish() {
  // TODO: POST to /api/admin/setup
  router.push('/')
}
</script>

<style scoped>
.setup {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 24px;
}

.setup-card {
  background: #1a1a1e;
  border: 1px solid #2a2a2e;
  border-radius: 16px;
  padding: 40px;
  max-width: 520px;
  width: 100%;
}

.setup-header {
  text-align: center;
  margin-bottom: 32px;
}

.setup-icon { font-size: 48px; }
.setup-header h1 { color: #fff; margin: 12px 0 8px; }
.setup-header p { color: #888; }

.step h2 { color: #fff; margin-bottom: 8px; }
.hint { color: #888; margin-bottom: 16px; font-size: 14px; }

.options {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  border-radius: 10px;
  border: 1px solid #333;
  background: transparent;
  color: #e0e0e0;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s;
}

.option:hover { border-color: #555; }
.option.active { border-color: #2563eb; background: #2563eb11; }
.option span { font-size: 24px; }
.option strong { display: block; }
.option small { color: #888; font-size: 12px; }

.step-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.form-group { margin-bottom: 16px; }
.form-group label { display: block; color: #888; font-size: 13px; margin-bottom: 6px; }

.summary {
  background: #0f0f10;
  border-radius: 8px;
  padding: 16px;
  margin: 16px 0;
  font-size: 14px;
  line-height: 2;
}
</style>
