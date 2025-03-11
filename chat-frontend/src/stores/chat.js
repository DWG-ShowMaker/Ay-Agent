import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import request from '../utils/request'

export const useChatStore = defineStore('chat', () => {
  const conversations = ref([])
  const currentConversationId = ref(null)
  const messages = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  const isThinking = ref(false)

  const currentConversation = computed(() => 
    conversations.value.find(conv => conv.id === currentConversationId.value)
  )

  // 获取所有对话列表
  async function fetchConversations() {
    try {
      const data = await request.get('/conversations')
      conversations.value = data
      return data
    } catch (e) {
      console.error('获取对话列表失败:', e)
      error.value = '获取对话列表失败'
      throw e
    }
  }

  // 创建新对话
  async function createConversation() {
    try {
      const conversation = await request.post('/conversations')
      conversations.value.unshift(conversation)
      await switchConversation(conversation.id)
      return conversation
    } catch (e) {
      console.error('创建对话失败:', e)
      error.value = '创建对话失败'
      throw e
    }
  }

  // 切换对话
  async function switchConversation(conversationId) {
    try {
      isLoading.value = true
      currentConversationId.value = conversationId
      if (conversationId) {
        const data = await request.get(`/conversations/${conversationId}`)
        messages.value = data.messages || []
      } else {
        messages.value = []
      }
    } catch (e) {
      console.error('切换对话失败:', e)
      error.value = '切换对话失败'
      throw e
    } finally {
      isLoading.value = false
    }
  }

  // 发送消息
  async function sendMessage(content, isReasoning = false) {
    if (!content.trim()) return
    
    // 如果没有当前对话，先创建一个
    if (!currentConversationId.value) {
      await createConversation()
    }

    // 添加用户消息
    messages.value.push({
      role: 'user',
      content: content
    })

    isThinking.value = true
    const eventSource = new EventSource(
      `/api/chat/sse?message=${encodeURIComponent(content)}&conversation_id=${currentConversationId.value}&is_reasoning=${isReasoning}`
    )

    // 添加助手消息占位
    const assistantMessageIndex = messages.value.length
    messages.value.push({
      role: 'assistant',
      content: ''
    })

    return new Promise((resolve, reject) => {
      eventSource.onmessage = (event) => {
        if (event.data === '[DONE]') {
          eventSource.close()
          isThinking.value = false
          resolve()
          return
        }

        try {
          // 更新助手消息内容
          messages.value[assistantMessageIndex].content += event.data
        } catch (err) {
          console.error('处理消息失败:', err)
        }
      }

      eventSource.onerror = (err) => {
        eventSource.close()
        isThinking.value = false
        error.value = '连接中断'
        reject(err)
      }
    })
  }

  // 删除对话
  async function deleteConversation(conversationId) {
    try {
      await request.delete(`/conversations/${conversationId}`)
      const index = conversations.value.findIndex(conv => conv.id === conversationId)
      if (index !== -1) {
        conversations.value.splice(index, 1)
      }
      if (currentConversationId.value === conversationId) {
        currentConversationId.value = null
        messages.value = []
      }
    } catch (e) {
      console.error('删除对话失败:', e)
      error.value = '删除对话失败'
      throw e
    }
  }

  return {
    conversations,
    currentConversationId,
    currentConversation,
    messages,
    isLoading,
    error,
    isThinking,
    fetchConversations,
    createConversation,
    switchConversation,
    sendMessage,
    deleteConversation
  }
})
