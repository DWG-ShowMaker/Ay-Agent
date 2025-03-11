<template>
  <div class="message-wrapper group py-6 first:pt-4 last:pb-4 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
    <div class="flex gap-4 max-w-3xl mx-auto px-4">
      <!-- 头像 -->
      <div class="w-8 h-8 flex-shrink-0">
        <template v-if="isUser">
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white shadow-lg">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
        </template>
        <template v-else>
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-emerald-400 to-emerald-600 flex items-center justify-center text-white shadow-lg">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
        </template>
      </div>

      <!-- 消息内容 -->
      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-2 mb-1">
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
            {{ isUser ? '你' : 'AI 助手' }}
          </span>
          <span class="text-xs text-gray-400 dark:text-gray-500">{{ formatTime }}</span>
        </div>
        <div class="prose dark:prose-invert prose-sm max-w-none">
          <MarkdownContent 
            :content="props.content" 
            :key="props.content"
          />
          <div v-if="isThinking && isLastMessage" class="flex items-center gap-2 mt-4">
            <div class="thinking-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="flex-shrink-0 flex items-start space-x-1 opacity-0 group-hover:opacity-100 transition-all">
        <button 
          @click="copyMessage" 
          class="p-1.5 text-gray-400 hover:text-blue-500 dark:text-gray-500 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-500/10 rounded-md transition-all duration-200"
          title="复制消息"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
        </button>
        <!-- <button 
          @click="regenerateMessage" 
          v-if="!isUser && isLastMessage"
          class="p-1.5 text-gray-400 hover:text-emerald-500 dark:text-gray-500 dark:hover:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-emerald-500/10 rounded-md transition-all duration-200"
          title="重新生成"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button> -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useChatStore } from '../stores/chat'
import MarkdownContent from './MarkdownContent.vue'

const store = useChatStore()

const props = defineProps({
  content: String,
  role: String,
  isLastMessage: {
    type: Boolean,
    default: false
  },
  timestamp: {
    type: Number,
    default: () => Date.now()
  }
})

const isUser = computed(() => props.role === 'user')
const isThinking = computed(() => store.isThinking && !isUser.value)

const formatTime = computed(() => {
  const date = new Date(props.timestamp)
  return date.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit'
  })
})

const regenerateMessage = () => {
  store.regenerateMessage()
}

const copyMessage = () => {
  navigator.clipboard.writeText(props.content)
    .then(() => {
      // TODO: 添加复制成功的提示
    })
}
</script>

<style scoped>
/* 优化代码块样式 */
:deep(.prose pre) {
  background-color: #1a1b26;
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 1rem 0;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.prose code) {
  color: #7dd3fc;
  background-color: rgba(30, 41, 59, 0.5);
  padding: 0.2em 0.4em;
  border-radius: 0.25rem;
  font-size: 0.875em;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

:deep(.prose pre code) {
  background-color: transparent;
  padding: 0;
  border-radius: 0;
  color: #e2e8f0;
}

/* 优化链接样式 */
:deep(.prose a) {
  color: #3b82f6;
  text-decoration: none;
  transition: color 0.2s;
}

:deep(.prose a:hover) {
  color: #2563eb;
  text-decoration: underline;
}

.dark :deep(.prose a) {
  color: #60a5fa;
}

.dark :deep(.prose a:hover) {
  color: #93c5fd;
}

/* 添加按钮悬停动画 */
.message-wrapper button {
  transform: scale(1);
}

.message-wrapper button:hover {
  transform: scale(1.1);
}

.message-wrapper button:active {
  transform: scale(0.95);
}

/* 思考动画 */
.thinking-dots {
  display: flex;
  gap: 4px;
  padding: 4px 8px;
  background-color: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
}

.dark .thinking-dots {
  background-color: rgba(255, 255, 255, 0.05);
}

.thinking-dots span {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background-color: #10b981;
  animation: thinking 1.4s infinite;
  opacity: 0.5;
}

.thinking-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.thinking-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes thinking {
  0%, 100% {
    transform: scale(0.2);
    opacity: 0.2;
  }
  50% {
    transform: scale(1);
    opacity: 1;
  }
}
</style>
