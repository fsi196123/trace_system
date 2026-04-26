<template>
  <div class="stream-container">
    <div class="panel-header">
      <span class="icon">📡</span>
      <span>实时溯源流</span>
      <span class="count">{{ logs.length }} 条</span>
    </div>
    <div class="stream" ref="streamRef">
      <div
        v-for="item in logs"
        :key="item.id"
        class="log-item"
      >
        <span class="time">[{{ item.time }}]</span>
        <span class="city">{{ item.city }}</span>
        <span class="action">溯源</span>
        <span class="product">{{ item.product }}</span>
        <span class="status-icon" :class="item.statusType">{{ item.icon }}</span>
      </div>
      <div v-if="logs.length === 0" class="empty">
        等待溯源数据...
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const logs = ref([])
const streamRef = ref()
let ws = null
let id = 0

const cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安', '南京', '苏州', '重庆', '天津']
const products = ['牛奶001', '酸奶002', '白酒003', '红酒004', '啤酒005', '饮料006']
const statusMap = {
  success: { icon: '✅', type: 'success' },
  warning: { icon: '⚠️', type: 'warning' },
  danger: { icon: '❌', type: 'danger' }
}

onMounted(() => {
  ws = new WebSocket('ws://localhost:3000/ws/scan')

  ws.onmessage = (e) => {
    try {
      const data = JSON.parse(e.data)
      const statusKey = data.status || 'success'
      const statusInfo = statusMap[statusKey] || statusMap.success
      addLog({
        time: new Date().toLocaleTimeString('zh-CN', { hour12: false }),
        city: data.city || cities[Math.floor(Math.random() * cities.length)],
        product: data.product || products[Math.floor(Math.random() * products.length)],
        icon: statusInfo.icon,
        statusType: statusInfo.type
      })
    } catch (err) {
      const randomStatus = ['success', 'success', 'success', 'warning', 'danger'][Math.floor(Math.random() * 5)]
      const statusInfo = statusMap[randomStatus]
      addLog({
        time: new Date().toLocaleTimeString('zh-CN', { hour12: false }),
        city: cities[Math.floor(Math.random() * cities.length)],
        product: products[Math.floor(Math.random() * products.length)],
        icon: statusInfo.icon,
        statusType: statusInfo.type
      })
    }
  }

  ws.onerror = () => {
    const timer = setInterval(() => {
      const randomStatus = ['success', 'success', 'success', 'warning', 'danger'][Math.floor(Math.random() * 5)]
      const statusInfo = statusMap[randomStatus]
      addLog({
        time: new Date().toLocaleTimeString('zh-CN', { hour12: false }),
        city: cities[Math.floor(Math.random() * cities.length)],
        product: products[Math.floor(Math.random() * products.length)],
        icon: statusInfo.icon,
        statusType: statusInfo.type
      })
    }, 2000)
  }
})

const addLog = (log) => {
  log.id = ++id
  logs.value.unshift(log)
  if (logs.value.length > 20) logs.value.pop()
}

onUnmounted(() => {
  ws?.close()
})
</script>

<style scoped>
.stream-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 12px;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  font-size: 14px;
  font-weight: bold;
  color: #00ffcc;
}

.icon {
  font-size: 16px;
}

.count {
  background: #1f2a44;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
  color: #6b7a99;
  margin-left: auto;
}

.stream {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
}

.stream::-webkit-scrollbar {
  width: 4px;
}

.stream::-webkit-scrollbar-track {
  background: #1f2a44;
}

.stream::-webkit-scrollbar-thumb {
  background: #2f4f6f;
  border-radius: 2px;
}

.log-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  border-bottom: 1px solid #1a2436;
  font-size: 13px;
  animation: fadeIn 0.3s ease;
  color: #e2e8f0;
}

.log-item:last-child {
  border-bottom: none;
}

.time {
  color: #6b7a99;
  font-family: monospace;
  font-size: 12px;
  flex-shrink: 0;
}

.city {
  color: #00ffcc;
  font-weight: 500;
  flex-shrink: 0;
}

.action {
  color: #94a3b8;
  flex-shrink: 0;
}

.product {
  color: #e2e8f0;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.status-icon {
  font-size: 16px;
  flex-shrink: 0;
}

.status-icon.success {
  color: #52c41a;
}

.status-icon.warning {
  color: #faad14;
}

.status-icon.danger {
  color: #ff4d4f;
}

.empty {
  text-align: center;
  color: #6b7a99;
  padding: 20px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>