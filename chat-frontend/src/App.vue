<template>
  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<script setup>
import { onMounted } from 'vue'

// 初始化暗色模式
onMounted(() => {
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  document.documentElement.classList.toggle('dark', prefersDark)
})
</script>

<style>
:root {
  --ai-dark: #202123;
  --ai-sidebar: #202123;
  --ai-chat-bg-dark: #343541;
  --ai-chat-bg-light: #ffffff;
  --ai-assistant-bg: #444654;
  --ai-border: rgba(255,255,255,.1);
  --ai-text: #ececf1;
  --ai-text-dark: #000000;
  --ai-green: #10a37f;
  color-scheme: light dark;
}

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: Söhne,ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,Noto Sans,sans-serif;
  background: var(--ai-chat-bg-light);
  color: var(--ai-text-dark);
  -webkit-font-smoothing: antialiased;
}

body.dark {
  background: var(--ai-chat-bg-dark);
  color: var(--ai-text);
}

#app {
  height: 100vh;
}

/* NProgress 样式覆盖 */
#nprogress {
  pointer-events: none;
}

#nprogress .bar {
  background: #3b82f6;
  height: 3px;
}

#nprogress .peg {
  box-shadow: 0 0 10px #3b82f6, 0 0 5px #3b82f6;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Markdown 样式 */
.markdown-body {
  font-size: 14px;
  line-height: 1.6;
  color: var(--ai-text-dark);
  margin: 0.5em 0;
}

body.dark .markdown-body {
  color: var(--ai-text);
}

.markdown-body pre {
  background: var(--ai-dark);
  border-radius: 6px;
  padding: 1rem;
  overflow: auto;
}

.markdown-body code {
  font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, monospace;
  font-size: 12px;
  background: var(--ai-dark);
}

.markdown-body h1, .markdown-body h2, .markdown-body h3, .markdown-body h4, .markdown-body h5, .markdown-body h6 {
  margin: 0.5em 0;
  font-weight: bold;
}

.markdown-body ul, .markdown-body ol {
  margin: 0.5em 0;
  padding-left: 1.5em;
}

.markdown-body blockquote {
  margin: 0.5em 0;
  padding-left: 1em;
  border-left: 4px solid var(--ai-border);
  color: var(--ai-text-dark);
}

body.dark .markdown-body blockquote {
  color: var(--ai-text);
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}

.dark ::-webkit-scrollbar-thumb {
  background-color: rgba(75, 85, 99, 0.5);
}

/* 平滑过渡效果 */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}
</style>
