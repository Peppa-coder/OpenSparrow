<template>
  <div class="file-tree">
    <div
      v-for="item in items"
      :key="item.path"
      class="tree-item"
      @click="$emit('select', item)"
    >
      <span>{{ item.is_dir ? '📂' : '📄' }}</span>
      <span class="item-name">{{ item.name }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  items: Array<{ name: string; path: string; is_dir: boolean }>
}>()
defineEmits(['select'])
</script>

<style scoped>
.tree-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border-radius: 6px;
  cursor: pointer;
}
.tree-item:hover { background: #2a2a2e; }
.item-name { font-size: 14px; }
</style>
