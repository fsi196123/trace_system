<template>
  <div class="header">
    <div class="header-left">
      <h3>睿码溯源系统</h3>
      <p class="platform">RuiTrace Platform</p>
    </div>
    <div class="header-right">
      <div class="connection-status" :class="{ connected: isConnected }">
        <span class="dot"></span>
        <span class="text">{{ connectionText }}</span>
      </div>
      <div class="user-info">
        <span class="username">{{ username }}</span>
        <el-button size="small" @click="handleLogout">退出</el-button>
      </div>
      <div class="time">{{ currentTime }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const isConnected = ref(false)
const connectionText = ref('连接中...')
const username = ref('admin')
const currentTime = ref('')

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  })
}

const handleLogout = () => {
  localStorage.removeItem('isLoggedIn')
  router.push('/login')
}

onMounted(() => {
  setInterval(updateTime, 1000)
  updateTime()
  
  setTimeout(() => {
    isConnected.value = true
    connectionText.value = '已连接'
  }, 1000)
})

onUnmounted(() => {
  // 清理定时器
})
</script>

<style scoped>
.header {
  height: 60px;
  background: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid #eaeaea;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  flex-direction: column;
}

.header-left h3 {
  margin: 0;
  font-size: 18px;
  color: #1f4fff;
  font-weight: bold;
}

.header-left .platform {
  margin: 0;
  font-size: 12px;
  color: #606266;
  margin-top: 2px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
}

.connection-status .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ff4d4f;
}

.connection-status.connected .dot {
  background: #52c41a;
  animation: pulse 2s infinite;
}

.connection-status .text {
  color: #666;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-info .username {
  font-size: 14px;
  color: #333;
}

.time {
  font-size: 12px;
  color: #666;
  font-family: monospace;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style>