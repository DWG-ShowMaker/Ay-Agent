<template>
  <div class="relative">
    <div class="relative flex flex-col gap-2">
      <div class="flex items-center gap-2">
        <div 
          class="flex-1 min-h-[44px] rounded-lg border transition-all duration-200 bg-white dark:bg-gray-800 overflow-hidden shadow-sm"
          :class="[
            isReasoningMode 
              ? 'border-purple-300 dark:border-purple-500 focus-within:ring-2 focus-within:ring-purple-500 dark:focus-within:ring-purple-400'
              : 'border-gray-200 dark:border-gray-700 focus-within:ring-2 focus-within:ring-blue-500 dark:focus-within:ring-blue-400'
          ]"
        >
          <div class="flex items-center px-3">
            <textarea
              v-model="message"
              ref="textareaRef"
              rows="1"
              class="flex-1 resize-none bg-transparent py-3 text-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 outline-none"
              :style="{ height: textareaHeight + 'px' }"
              placeholder="发送消息..."
              @input="adjustTextareaHeight"
              @keydown.enter.exact.prevent="handleSend"
              @keydown.enter.shift.exact="newline"
              @keydown.enter.meta.exact="newline"
              @keydown.esc="clearMessage"
              @focus="isFocused = true"
              @blur="isFocused = false"
            ></textarea>
            
            <!-- 推理按钮 -->
            <button
              @click="toggleReasoning"
              class="flex-shrink-0 p-1.5 rounded-md transition-all duration-200"
              :class="[
                isReasoningMode
                  ? 'text-purple-500 dark:text-purple-400 bg-purple-50 dark:bg-purple-500/10'
                  : 'text-gray-400 hover:text-purple-500 dark:text-gray-500 dark:hover:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-500/10'
              ]"
              title="开启推理模式"
            >
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </button>

            <!-- 发送按钮 -->
            <button
              @click="handleSend"
              class="flex-shrink-0 p-1.5 ml-1 rounded-md transition-all duration-200"
              :class="[
                message.trim() 
                  ? isReasoningMode
                    ? 'text-purple-500 dark:text-purple-400 bg-purple-50 dark:bg-purple-500/10'
                    : 'text-blue-500 dark:text-blue-400 bg-blue-50 dark:bg-blue-500/10'
                  : 'text-gray-400 dark:text-gray-500 cursor-not-allowed opacity-50'
              ]"
              :disabled="!message.trim()"
              title="发送消息"
            >
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"
                ></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      <!-- 底部提示 -->
      <div class="flex items-center justify-between text-xs">
        <div class="text-gray-400 dark:text-gray-500 flex items-center gap-2">
          <span>按 Enter 发送，Shift + Enter 换行</span>
          <span v-if="isReasoningMode" class="flex items-center gap-1 text-purple-500 dark:text-purple-400">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            推理模式已开启
          </span>
        </div>
        <div class="text-gray-400 dark:text-gray-500 flex items-center gap-2">
          <span v-if="message.length > 0">{{ message.length }} / 4000</span>
          <span v-if="isFocused">ESC 清空</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['send'])
const message = ref('')
const textareaRef = ref(null)
const textareaHeight = ref(0)
const isFocused = ref(false)
const isReasoningMode = ref(false)

const handleSend = () => {
  if (!message.value.trim()) return
  emit('send', {
    content: message.value,
    isReasoning: isReasoningMode.value
  })
  message.value = ''
  adjustTextareaHeight()
}

const toggleReasoning = () => {
  isReasoningMode.value = !isReasoningMode.value
}

const adjustTextareaHeight = () => {
  const textarea = textareaRef.value
  if (!textarea) return
  
  textarea.style.height = 'auto'
  textarea.style.height = Math.min(textarea.scrollHeight, 160) + 'px'
  textareaHeight.value = Math.min(textarea.scrollHeight, 160)
}

const newline = (e) => {
  const start = e.target.selectionStart
  const end = e.target.selectionEnd
  message.value = message.value.substring(0, start) + '\n' + message.value.substring(end)
  nextTick(() => {
    e.target.selectionStart = e.target.selectionEnd = start + 1
  })
}

const clearMessage = () => {
  message.value = ''
  adjustTextareaHeight()
}

onMounted(() => {
  adjustTextareaHeight()
})
</script>

<style scoped>
textarea {
  line-height: 1.5;
  font-size: 0.875rem;
}

textarea::placeholder {
  color: #9CA3AF;
}

.dark textarea::placeholder {
  color: #6B7280;
}

/* 自定义滚动条 */
textarea::-webkit-scrollbar {
  width: 6px;
}

textarea::-webkit-scrollbar-track {
  background: transparent;
}

textarea::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}

.dark textarea::-webkit-scrollbar-thumb {
  background-color: rgba(75, 85, 99, 0.5);
}

/* 按钮动画 */
button {
  transform: scale(1);
  transition: transform 0.2s;
}

button:hover:not(:disabled) {
  transform: scale(1.1);
}

button:active:not(:disabled) {
  transform: scale(0.95);
}
</style>
