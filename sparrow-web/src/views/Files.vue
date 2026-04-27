<template>
  <div class="page">
    <h1 class="page-title">📁 File Browser</h1>
    <div class="card">
      <div class="file-toolbar">
        <span class="current-path">~/sparrow-workspace/{{ currentPath }}</span>
        <button class="btn btn-ghost" @click="refresh">🔄 Refresh</button>
      </div>
      <div class="file-list">
        <div class="file-item" v-if="currentPath" @click="goUp">
          <span>📂</span>
          <span>..</span>
        </div>
        <div class="file-item" v-for="file in files" :key="file.path" @click="openItem(file)">
          <span>{{ file.is_dir ? '📂' : '📄' }}</span>
          <span class="file-name">{{ file.name }}</span>
          <span class="file-size">{{ file.is_dir ? '' : formatSize(file.size) }}</span>
        </div>
        <div v-if="files.length === 0" class="empty">
          No files in workspace. Start by uploading or creating files.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface FileItem {
  name: string
  path: string
  is_dir: boolean
  size: number
}

const currentPath = ref('')
const files = ref<FileItem[]>([])

function formatSize(bytes: number): string {
  if (bytes === 0) return ''
  const units = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${units[i]}`
}

function refresh() {
  // TODO: Fetch from API
}

function openItem(file: FileItem) {
  if (file.is_dir) {
    currentPath.value = file.path
    refresh()
  }
}

function goUp() {
  const parts = currentPath.value.split('/').filter(Boolean)
  parts.pop()
  currentPath.value = parts.join('/')
  refresh()
}
</script>

<style scoped>
.file-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #2a2a2e;
}

.current-path {
  font-family: monospace;
  color: #888;
  font-size: 13px;
}

.file-list { display: flex; flex-direction: column; }

.file-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s;
}

.file-item:hover { background: #2a2a2e; }
.file-name { flex: 1; }
.file-size { color: #666; font-size: 13px; font-family: monospace; }
.empty { color: #666; text-align: center; padding: 40px 0; }
</style>
