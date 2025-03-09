import { defineStore } from 'pinia'
import request from '../utils/request'

export const useChatStore = defineStore('chat', {
  state: () => ({
    conversations: [],
    currentConversation: null,
    messages: [],
    isLoading: false,
    isThinking: false // 添加思考状态
  }),
  
  actions: {
    async fetchConversations() {
      try {
        this.conversations = await request.get('/conversations')
      } catch (error) {
        console.error('获取会话列表失败:', error)
        this.conversations = []
      }
    },
    
    async createConversation() {
      try {
        const conversation = await request.post('/conversations')
        this.conversations.push(conversation)
        this.currentConversation = conversation
      } catch (error) {
        console.error('创建会话失败:', error)
      }
    },
    
    // SSE不使用axios,保持原有实现
    async sendMessage(message) {
      if (!this.currentConversation) return
      this.isLoading = true
      this.isThinking = true // 开始思考
      
      try {
        // 添加用户消息
        this.messages.push({
          role: 'user',
          content: message,
          id: Date.now()
        })
        
        // 预创建AI消息
        let assistantMessage = {
          role: 'assistant',
          content: '',
          id: Date.now() + 1
        }
        this.messages.push(assistantMessage)
        
        const url = new URL('http://127.0.0.1:5000/api/chat/sse')
        url.searchParams.append('conversation_id', this.currentConversation.id)
        url.searchParams.append('message', message)
        
        const eventSource = new EventSource(url.toString())
        
        eventSource.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            
            if (data.type === 'message' && data.content) {
              assistantMessage.content += data.content
              this.messages = [...this.messages]  // 触发Vue的响应式更新
            } else if (data.type === 'error') {
              console.error('SSE error:', data.content)
              eventSource.close()
              this.isLoading = false
              this.isThinking = false // 停止思考
            } else if (data.type === 'done') {
              eventSource.close()
              this.isLoading = false
              this.isThinking = false // 停止思考
            }
          } catch (e) {
            console.error('SSE parsing error:', e)
          }
        }
        
        eventSource.onerror = (error) => {
          console.error('SSE connection error:', error)
          eventSource.close()
          this.isLoading = false
          this.isThinking = false // 停止思考
        }
        
      } catch (error) {
        console.error('Message sending failed:', error)
        this.isLoading = false
        this.isThinking = false // 停止思考
      }
    }
  }
})
