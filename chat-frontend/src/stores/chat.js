import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useChatStore = defineStore('chat', () => {
  const conversations = ref([])
  const currentConversationId = ref(null)
  const messages = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  const currentConversation = computed(() => 
    conversations.value.find(conv => conv.id === currentConversationId.value)
  )

  // 获取所有对话列表
  async function fetchConversations() {
    try {
      const response = await fetch('/api/conversations')
      const data = await response.json()
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
      const response = await fetch('/api/conversations', {
        method: 'POST'
      })
      const conversation = await response.json()
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
      error.value = null
      
      // 获取对话完整内容
      const response = await fetch(`/api/conversations/${conversationId}`)
      const conversation = await response.json()
      
      if (response.ok) {
        currentConversationId.value = conversationId
        messages.value = conversation.messages || []
        
        // 更新对话列表中的对话信息
        const index = conversations.value.findIndex(conv => conv.id === conversationId)
        if (index !== -1) {
          conversations.value[index] = {
            ...conversations.value[index],
            ...conversation
          }
        }
      } else {
        throw new Error(conversation.error || '加载对话失败')
      }
    } catch (e) {
      console.error('切换对话失败:', e)
      error.value = e.message || '切换对话失败'
      throw e
    } finally {
      isLoading.value = false
    }
  }

  // 删除对话
  async function deleteConversation(conversationId) {
    try {
      const response = await fetch(`/api/conversations/${conversationId}`, {
        method: 'DELETE'
      })
      
      if (response.ok) {
        conversations.value = conversations.value.filter(conv => conv.id !== conversationId)
        
        // 如果删除的是当前对话，切换到其他对话或创建新对话
        if (currentConversationId.value === conversationId) {
          if (conversations.value.length > 0) {
            await switchConversation(conversations.value[0].id)
          } else {
            await createConversation()
          }
        }
      } else {
        throw new Error('删除对话失败')
      }
    } catch (e) {
      console.error('删除对话失败:', e)
      error.value = '删除对话失败'
      throw e
    }
  }

  // 发送消息
  async function sendMessage(content, isReasoning = false) {
    if (!currentConversationId.value) {
      throw new Error('没有选择对话')
    }

    isLoading.value = true
    error.value = null

    try {
      const messageId = Date.now().toString()
      
      // 添加用户消息到本地状态
      messages.value.push({
        id: messageId,
        role: 'user',
        content,
        timestamp: Date.now()
      })

      let assistantMessage = {
        id: messageId + '_reply',
        role: 'assistant',
        content: '',
        timestamp: Date.now()
      }
      
      // 添加空的助手消息，用于流式更新
      messages.value.push(assistantMessage)

      const url = new URL('/api/chat/sse', window.location.origin)
      url.searchParams.append('conversation_id', currentConversationId.value)
      url.searchParams.append('message', content)
      url.searchParams.append('is_reasoning', isReasoning)

      const eventSource = new EventSource(url)

      return new Promise((resolve, reject) => {
        eventSource.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            if (data.type === 'message') {
              assistantMessage.content += data.content
              // 强制更新消息数组以触发视图更新
              messages.value = [...messages.value]
            } else if (data.type === 'error') {
              eventSource.close()
              reject(new Error(data.content))
            } else if (data.type === 'done') {
              eventSource.close()
              resolve()
            }
          } catch (e) {
            console.error('解析消息失败:', e)
            eventSource.close()
            reject(e)
          }
        }

        eventSource.onerror = (err) => {
          console.error('SSE连接错误:', err)
          eventSource.close()
          reject(new Error('连接错误'))
        }
      })
    } catch (e) {
      console.error('发送消息失败:', e)
      error.value = '发送消息失败'
      throw e
    } finally {
      isLoading.value = false
    }
  }

  return {
    conversations,
    currentConversation,
    currentConversationId,
    messages,
    isLoading,
    error,
    fetchConversations,
    createConversation,
    switchConversation,
    deleteConversation,
    sendMessage
  }
})
