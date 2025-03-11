import { createRouter, createWebHistory } from 'vue-router'
import { defineAsyncComponent } from 'vue'
import Home from '../views/Home.vue'
import LoadingView from '../components/LoadingView.vue'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import { useChatStore } from '../stores/chat'

// 配置 NProgress
NProgress.configure({ 
  showSpinner: false,
  easing: 'ease',
  speed: 400
})

// 异步加载 Chat 组件
const ChatView = defineAsyncComponent({
  loader: () => import('../views/Chat.vue'),
  loadingComponent: LoadingView,
  // 最小延迟时间
  delay: 0,
  // 超时时间
  timeout: 20000,
  // 加载错误时的提示组件
  errorComponent: {
    template: `
      <div class="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900">
        <div class="text-center">
          <p class="text-red-500 dark:text-red-400 mb-4">加载失败，请刷新页面重试</p>
          <button @click="reload" class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
            刷新页面
          </button>
        </div>
      </div>
    `,
    methods: {
      reload() {
        window.location.reload()
      }
    }
  }
})

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: {
      title: 'Ay-Agent - 智能助手平台'
    }
  },
  {
    path: '/chat',
    name: 'chat',
    component: ChatView,
    meta: {
      title: 'AI 对话 - Ay-Agent'
    },
    async beforeEnter(to, from, next) {
      const store = useChatStore()
      try {
        await store.fetchConversations()
        next()
      } catch (error) {
        console.error('初始化聊天失败:', error)
        next(false)
      }
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 预加载 Chat 组件
router.beforeResolve((to, from, next) => {
  if (to.path === '/') {
    // 在首页预加载 Chat 组件
    import('../views/Chat.vue')
  }
  next()
})

// 路由加载进度条
router.beforeEach((to, from, next) => {
  if (to.path !== from.path) {
    NProgress.start()
  }
  document.title = to.meta.title || 'Ay-Agent'
  next()
})

router.afterEach(() => {
  NProgress.done()
})

export default router