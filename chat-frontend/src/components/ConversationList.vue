<template>
  <div class="h-full flex flex-col bg-gray-50 dark:bg-gray-900">
    <div class="flex-1 overflow-y-auto">
      <div class="space-y-2 p-2">
        <div
          v-for="conv in store.conversations"
          :key="conv.id"
          @click="store.currentConversation = conv"
          class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors duration-200 cursor-pointer"
          :class="[
            store.currentConversation?.id === conv.id
              ? 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100'
              : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
          ]"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M8 10h.01M12 10h.01M16 10h.01M9 16h6m-7 4h8a2 2 0 002-2V8a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2z"
            ></path>
          </svg>
          <span class="flex-1 truncate">{{ conv.title || '新对话' }}</span>
          <button
            v-if="store.currentConversation?.id === conv.id"
            @click.stop="deleteConversation(conv.id)"
            class="opacity-0 group-hover:opacity-100 hover:text-red-500"
            title="删除对话"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              ></path>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- 底部设置区域 -->
    <div class="flex flex-col gap-2 p-4 border-t border-gray-200 dark:border-gray-700">
      <button
        @click="store.createConversation"
        class="flex items-center justify-center gap-2 w-full px-3 py-2 text-sm font-medium text-white bg-blue-500 hover:bg-blue-600 rounded-lg transition-colors duration-200"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 4v16m8-8H4"
          ></path>
        </svg>
        新建对话
      </button>
      
      <button
        @click="clearConversations"
        class="flex items-center justify-center gap-2 w-full px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors duration-200"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
          ></path>
        </svg>
        清空所有对话
      </button>
    </div>
  </div>
</template>

<script setup>
import { useChatStore } from '../stores/chat'

const store = useChatStore()

const deleteConversation = (id) => {
  if (confirm('确定要删除这个对话吗？')) {
    store.deleteConversation(id)
  }
}

const clearConversations = () => {
  if (confirm('确定要清空所有对话吗？')) {
    store.clearConversations()
  }
}
</script>

<style scoped>
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
</style>
