<template>
  <div class="screen">
    <header class="top-bar">
      <div class="title">产品溯源实时监控系统</div>
      <div class="stats">
        <div class="stat-item">
          <span class="label">今日溯源</span>
          <span class="value">{{ todayScan.toLocaleString() }}</span>
        </div>
        <div class="stat-item">
          <span class="label">风险等级</span>
          <span class="value" :class="riskClass">{{ riskLevel }}</span>
        </div>
        <div class="stat-item danger">
          <span class="label">异常溯源码</span>
          <span class="value">{{ dangerCount }}</span>
        </div>
        <div class="stat-item">
          <span class="label">风险指数</span>
          <span class="value">{{ riskIndex }}</span>
        </div>
      </div>
    </header>

    <section class="map-area">
      <MapChina ref="mapRef" />
    </section>

    <section class="bottom">
      <LiveStream class="panel" />
      <RiskPanel class="panel" />
      <TopRegion class="panel" />
    </section>

    <section class="attack">
      <AttackGraph />
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import MapChina from '@/components/MapChina.vue'
import LiveStream from '@/components/LiveStream.vue'
import RiskPanel from '@/components/RiskPanel.vue'
import TopRegion from '@/components/TopRegion.vue'
import AttackGraph from '@/components/AttackGraph.vue'

const todayScan = ref(12843)
const riskLevel = ref('LOW')
const dangerCount = ref(12)
const riskIndex = ref(23)

const riskClass = computed(() => {
  if (riskLevel.value === 'HIGH') return 'red'
  if (riskLevel.value === 'MEDIUM') return 'orange'
  return 'green'
})

let wsScan = null
let wsAlert = null

onMounted(() => {
  wsScan = new WebSocket('ws://localhost:3000/ws/scan')
  wsScan.onmessage = (e) => {
    const data = JSON.parse(e.data)
    todayScan.value++
    if (data.risk === 'HIGH') dangerCount.value++
  }

  wsAlert = new WebSocket('ws://localhost:3000/ws/alert')
  wsAlert.onmessage = (e) => {
    const data = JSON.parse(e.data)
    if (data.level === 'HIGH') {
      riskLevel.value = 'HIGH'
      riskIndex.value = Math.min(100, riskIndex.value + 5)
    } else if (data.level === 'MEDIUM') {
      riskLevel.value = 'MEDIUM'
    }
  }
})

onUnmounted(() => {
  wsScan?.close()
  wsAlert?.close()
})
</script>

<style scoped>
.screen {
  background: #0b0f1a;
  color: #fff;
  height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: 'Arial', 'Microsoft YaHei', sans-serif;
  overflow: hidden;
}

.top-bar {
  height: 60px;
  display: flex;
  justify-content: space-between;
  padding: 0 30px;
  align-items: center;
  border-bottom: 1px solid #1f2a44;
  background: linear-gradient(180deg, #0d1322 0%, #0b0f1a 100%);
}

.title {
  font-size: 22px;
  font-weight: bold;
  letter-spacing: 2px;
  color: #00ffcc;
  text-shadow: 0 0 20px rgba(0, 255, 204, 0.3);
}

.stats {
  display: flex;
  gap: 30px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-item .label {
  font-size: 12px;
  color: #6b7a99;
  margin-bottom: 2px;
}

.stat-item .value {
  font-size: 18px;
  font-weight: bold;
}

.map-area {
  flex: 1;
  padding: 10px;
  min-height: 0;
}

.bottom {
  height: 200px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 10px;
  padding: 0 10px 10px;
}

.panel {
  background: #111827;
  border-radius: 8px;
  border: 1px solid #1f2a44;
}

.attack {
  height: 180px;
  padding: 0 10px 10px;
}

.red { color: #ff4d4f; }
.orange { color: #faad14; }
.green { color: #52c41a; }

.danger .value {
  color: #ff4d4f;
  animation: blink 1.5s infinite;
}

@keyframes blink {
  50% { opacity: 0.5; }
}

@keyframes pulse {
  0% { opacity: 0.2; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.1); }
  100% { opacity: 0.2; transform: scale(1); }
}
</style>