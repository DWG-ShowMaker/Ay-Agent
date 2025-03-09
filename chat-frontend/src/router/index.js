import { createRouter, createWebHistory } from 'vue-router'
import Chat from '../views/Chat.vue'

const routes = [
  {
    path: '/chat',
    component: Chat,
    meta: {
      title: '聊天',
      requiresAuth: false
    }
  }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
