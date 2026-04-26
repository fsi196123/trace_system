<template>
  <div class="panel-container">
    <div class="panel-header">
      <span class="icon">🚨</span>
      <span>风险预警</span>
      <span class="badge" :class="severityClass">{{ risks.length }} 条</span>
    </div>
    <div class="alert-list">
      <div
        v-for="(r, index) in risks"
        :key="r.id"
        class="alert-item"
        :class="r.level.toLowerCase()"
        :style="{ animationDelay: index * 0.1 + 's' }"
      >
        <div class="alert-header">
          <span class="level-badge" :class="r.level.toLowerCase()">{{ r.level }}</span>
          <span class="time">{{ r.time }}</span>
        </div>
        <div class="alert-msg">{{ r.msg }}</div>
        <div class="alert-meta">
          <span>📍 {{ r.city }}</span>
          <span>📱 {{ r.ip }}</span>
          <span>🔢 {{ r.count }}次</span>
        </div>
      </div>
      <div v-if="risks.length === 0" class="empty">
        <span class="safe">✓ 暂无风险预警</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const risks = ref([])
let ws = null
let id = 0

const severityClass = computed(() => {
  if (risks.value.some(r => r.level === 'HIGH')) return 'high'
  if (risks.value.some(r => r.level === 'MEDIUM')) return 'medium'
  return 'low'
})

onMounted(() => {
  ws = new WebSocket('ws://localhost:3000/ws/alert')

  ws.onmessage = (e) => {
    try {
      const data = JSON.parse(e.data)
      addRisk({
        id: ++id,
        level: data.level || 'MEDIUM',
        msg: data.msg || data.message || '检测到异常溯源行为',
        city: data.city || '未知城市',
        ip: data.ip || '0.0.0.0',
        count: data.count || 1,
        time: new Date().toLocaleTimeString()
      })
    } catch (err) {
      addRisk({
        id: ++id,
        level: 'MEDIUM',
        msg: '检测到异常溯源行为',
        city: '未知城市',
        ip: '0.0.0.0',
        count: 1,
        time: new Date().toLocaleTimeString()
      })
    }
  }

  ws.onerror = () => {
    let timer = setTimeout(function auto() {
      if (Math.random() > 0.6) {
        addRisk({
          id: ++id,
          level: Math.random() > 0.5 ? 'HIGH' : 'MEDIUM',
          msg: ['重复溯源异常', 'IP聚集异常', '批量验证异常', '仿冒码检测'][Math.floor(Math.random() * 4)],
          city: ['北京', '上海', '广州', '深圳', '杭州'][Math.floor(Math.random() * 5)],
          ip: `192.168.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`,
          count: Math.floor(Math.random() * 50) + 5,
          time: new Date().toLocaleTimeString()
        })
      }
      timer = setTimeout(auto, 3000)
    }, 3000)
  }
})

const addRisk = (risk) => {
  risks.value.unshift(risk)
  if (risks.value.length > 20) risks.value.pop()
}

onUnmounted(() => {
  ws?.close()
})
</script>

<style scoped>
.panel-container {
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
  color: #ff4d4f;
}

.icon {
  font-size: 16px;
}

.badge {
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: normal;
}

.badge.high { background: #ff4d4f; color: #fff; }
.badge.medium { background: #faad14; color: #000; }
.badge.low { background: #52c41a; color: #fff; }

.alert-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.alert-list::-webkit-scrollbar {
  width: 4px;
}

.alert-list::-webkit-scrollbar-track {
  background: #1f2a44;
}

.alert-list::-webkit-scrollbar-thumb {
  background: #2f4f6f;
  border-radius: 2px;
}

.alert-item {
  padding: 8px 10px;
  border-radius: 4px;
  background: #1a2436;
  animation: slideIn 0.3s ease;
}

.alert-item.high {
  border-left: 3px solid #ff4d4f;
  background: rgba(255, 77, 79, 0.1);
}

.alert-item.medium {
  border-left: 3px solid #faad14;
  background: rgba(250, 173, 20, 0.1);
}

.alert-item.low {
  border-left: 3px solid #52c41a;
}

.alert-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.level-badge {
  padding: 1px 6px;
  border-radius: 3px;
  font-size: 10px;
  font-weight: bold;
}

.level-badge.high { background: #ff4d4f; color: #fff; }
.level-badge.medium { background: #faad14; color: #000; }
.level-badge.low { background: #52c41a; color: #fff; }

.time {
  font-size: 10px;
  color: #6b7a99;
}

.alert-msg {
  font-size: 12px;
  color: #d0d7e0;
  margin-bottom: 4px;
}

.alert-meta {
  display: flex;
  gap: 12px;
  font-size: 10px;
  color: #6b7a99;
}

.empty {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.safe {
  color: #52c41a;
  font-size: 14px;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 1; transform: translateX(0); }
}
</style>