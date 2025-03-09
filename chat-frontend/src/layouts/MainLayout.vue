<template>
  <div :class="['layout', { dark: isDarkMode }]">
    <aside class="sidebar">
      <ConversationList />
    </aside>
    <main class="main flex-1 flex flex-col bg-gray-100 dark:bg-gray-900">
      <slot></slot>
    </main>
  </div>
</template>

<script setup>
import { ref, watchEffect } from 'vue'
import ConversationList from '../components/ConversationList.vue'

const isDarkMode = ref(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)

watchEffect(() => {
  document.body.classList.toggle('dark', isDarkMode.value)
})
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background: var(--ai-chat-bg-light); /* 白天模式背景颜色 */
  color: var(--ai-text-dark); /* 白天模式字体颜色 */
}

.layout.dark {
  background: var(--ai-chat-bg-dark); /* 暗黑模式背景颜色 */
  color: var(--ai-text); /* 暗黑模式字体颜色 */
}

.sidebar {
  flex-shrink: 0;
  border-right: 1px solid var(--ai-border);
  background: var(--ai-sidebar); /* 设置侧边栏背景颜色 */
}

.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  height: 100vh;
  background: var(--ai-chat-bg); /* 设置主区域背景颜色 */
}
</style>
