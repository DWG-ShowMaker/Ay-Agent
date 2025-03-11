<template>
  <div class="flex flex-col h-full">
    <!-- 新建对话按钮 -->
    <div class="p-4 border-b border-gray-200 dark:border-gray-800">
      <button
        @click="handleNewChat"
        class="w-full flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
        </svg>
        新建对话
      </button>
    </div>

    <!-- 对话列表 -->
    <div class="flex-1 overflow-y-auto">
      <div v-if="store.conversations.length === 0" class="p-4 text-center text-gray-500 dark:text-gray-400">
        暂无对话记录
      </div>
      <div v-else class="space-y-1 p-2">
        <button
          v-for="conversation in store.conversations"
          :key="conversation.id"
          @click="handleSelectChat(conversation.id)"
          class="w-full flex items-center gap-3 px-3 py-2 text-left text-sm rounded-lg transition-colors"
          :class="[
            conversation.id === store.currentConversationId
              ? 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white'
              : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800/50'
          ]"
        >
          <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16h6m-7 4h8a2 2 0 002-2V8a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
          </svg>
          <span class="flex-1 truncate">{{ conversation.title }}</span>
          <button
            v-if="conversation.id === store.currentConversationId"
            @click.stop="showDeleteConfirm(conversation.id)"
            class="p-1 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            title="删除对话"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
            </svg>
          </button>
        </button>
      </div>
    </div>

    <!-- 确认删除对话框 -->
    <ConfirmDialog
      v-model:show="showConfirmDialog"
      title="删除对话"
      message="确定要删除这个对话吗？删除后将无法恢复。"
      @confirm="handleDeleteConfirm"
      @cancel="handleDeleteCancel"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useChatStore } from '../stores/chat'
import ConfirmDialog from './ConfirmDialog.vue'

const store = useChatStore()
const showConfirmDialog = ref(false)
const pendingDeleteId = ref(null)

const handleNewChat = async () => {
  try {
    await store.createConversation()
  } catch (e) {
    console.error('创建新对话失败:', e)
  }
}

const handleSelectChat = async (conversationId) => {
  try {
    await store.switchConversation(conversationId)
  } catch (e) {
    console.error('切换对话失败:', e)
  }
}

const showDeleteConfirm = (conversationId) => {
  pendingDeleteId.value = conversationId
  showConfirmDialog.value = true
}

const handleDeleteConfirm = async () => {
  if (pendingDeleteId.value) {
    try {
      await store.deleteConversation(pendingDeleteId.value)
    } catch (e) {
      console.error('删除对话失败:', e)
    }
  }
  pendingDeleteId.value = null
}

const handleDeleteCancel = () => {
  pendingDeleteId.value = null
}
</script>

<style scoped>
.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 2px;
}

.dark .overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: rgba(75, 85, 99, 0.5);
}
</style>
