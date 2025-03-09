<template>
  <div class="flex h-screen bg-white dark:bg-gray-900 transition-colors">
    <!-- 侧边栏 -->
    <div class="w-64 flex flex-col border-r border-gray-200 dark:border-gray-800">
      <ConversationList />
    </div>

    <!-- 主聊天区域 -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
      <!-- 顶部导航栏 -->
      <div class="flex items-center justify-between h-14 px-4 border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm">
        <h1 class="text-lg font-medium text-gray-900 dark:text-gray-100">
          {{ store.currentConversation?.title || 'AI 助手' }}
        </h1>
        <div class="flex items-center gap-3">
          <button 
            @click="toggleDarkMode" 
            class="p-2 text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-100 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            title="切换主题"
          >
            <template v-if="isDarkMode">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m8.66-8.66h-1M4.34 12H3m15.66 4.34l-.707-.707M6.34 6.34l-.707-.707m12.02 12.02l-.707-.707M6.34 17.66l-.707-.707M12 5a7 7 0 100 14 7 7 0 000-14z"></path>
              </svg>
            </template>
            <template v-else>
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
              </svg>
            </template>
          </button>
        </div>
      </div>

      <!-- 消息列表 -->
      <div class="flex-1 overflow-y-auto scroll-smooth bg-gray-50 dark:bg-gray-900" ref="messagesRef">
        <div class="max-w-3xl mx-auto">
          <template v-if="store.messages.length">
            <ChatMessage
              v-for="(msg, index) in store.messages"
              :key="msg.id"
              :content="msg.content"
              :role="msg.role"
              :timestamp="msg.timestamp"
              :is-last-message="index === store.messages.length - 1"
            />
          </template>
          <div v-else class="flex flex-col items-center justify-center h-[calc(100vh-8rem)] text-center px-4">
            <div class="w-16 h-16 mb-6 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white shadow-lg">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16h6m-7 4h8a2 2 0 002-2V8a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
              </svg>
            </div>
            <h2 class="text-xl font-medium text-gray-900 dark:text-gray-100 mb-2">开始新的对话</h2>
            <p class="text-sm text-gray-500 dark:text-gray-400 max-w-sm">
              发送消息开始与 AI 助手对话，探索无限可能...
            </p>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="border-t border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm">
        <div class="max-w-3xl mx-auto p-4">
          <ChatInput @send="handleSend" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { useChatStore } from '../stores/chat'
import MainLayout from '../layouts/MainLayout.vue'
import ChatMessage from '../components/ChatMessage.vue'
import ChatInput from '../components/ChatInput.vue'
import ConversationList from '../components/ConversationList.vue'

const store = useChatStore()
const messagesRef = ref(null)
const isDarkMode = ref(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)

const scrollToBottom = async (smooth = true) => {
  await nextTick()
  if (messagesRef.value) {
    messagesRef.value.scrollTo({
      top: messagesRef.value.scrollHeight,
      behavior: smooth ? 'smooth' : 'auto'
    })
  }
}

watch(() => store.messages, () => {
  scrollToBottom()
}, { deep: true })

onMounted(async () => {
  await store.fetchConversations()
  if (!store.currentConversation) {
    await store.createConversation()
  }
  scrollToBottom(false)
})

const handleSend = async ({ content, isReasoning }) => {
  await store.sendMessage(content, isReasoning)
}

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  document.documentElement.classList.toggle('dark', isDarkMode.value)
}

// 初始化暗色模式
onMounted(() => {
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  document.documentElement.classList.toggle('dark', prefersDark)
})
</script>

<style>
:root {
  color-scheme: light dark;
}

/* 自定义滚动条样式 */
.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}

.dark .overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: rgba(75, 85, 99, 0.5);
}

/* 平滑过渡效果 */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}
</style>
