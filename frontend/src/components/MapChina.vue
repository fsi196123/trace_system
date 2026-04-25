<template>
  <div class="map-container">
    <div ref="mapRef" class="map"></div>
    <div class="map-overlay">
      <div class="legend">
        <div class="legend-item">
          <span class="dot high"></span>
          <span>高风险</span>
        </div>
        <div class="legend-item">
          <span class="dot medium"></span>
          <span>中风险</span>
        </div>
        <div class="legend-item">
          <span class="dot low"></span>
          <span>低风险</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import * as echarts from 'echarts'
import { ref, onMounted, onUnmounted, watch } from 'vue'
import china from '@/assets/china.json'

const mapRef = ref()
let chart = null
let timer = null

const scanData = ref([])

const initChart = () => {
  if (!mapRef.value) return

  chart = echarts.init(mapRef.value)
  echarts.registerMap('china', china)

  updateChart()
}

const updateChart = () => {
  if (!chart) return

  const option = {
    backgroundColor: 'transparent',
    geo: {
      map: 'china',
      roam: false,
      zoom: 1.2,
      center: [105, 36],
      itemStyle: {
        areaColor: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: '#1a2d4a' },
            { offset: 1, color: '#0f1c2e' }
          ]
        },
        borderColor: '#2f4f6f',
        borderWidth: 1
      },
      emphasis: {
        itemStyle: {
          areaColor: '#2a4a6a'
        }
      }
    },
    series: [
      {
        type: 'effectScatter',
        coordinateSystem: 'geo',
        data: scanData.value.filter(d => d.level === 'HIGH').map(d => ({
          name: d.city,
          value: [d.lng, d.lat, d.value],
          itemStyle: { color: '#ff4d4f' },
          symbolSize: 16
        })),
        rippleEffect: {
          brushType: 'stroke',
          scale: 3,
          period: 4
        }
      },
      {
        type: 'effectScatter',
        coordinateSystem: 'geo',
        data: scanData.value.filter(d => d.level === 'MEDIUM').map(d => ({
          name: d.city,
          value: [d.lng, d.lat, d.value],
          itemStyle: { color: '#faad14' },
          symbolSize: 12
        })),
        rippleEffect: {
          brushType: 'stroke',
          scale: 2.5,
          period: 5
        }
      },
      {
        type: 'heatmap',
        coordinateSystem: 'geo',
        data: scanData.value.map(d => [d.lng, d.lat, d.value]),
        pointSize: 8,
        blurSize: 20,
        gradientColors: ['#52c41a', '#faad14', '#ff4d4f']
      }
    ]
  }

  chart.setOption(option)
}

const addScanPoint = (data) => {
  scanData.value.push(data)
  if (scanData.value.length > 200) {
    scanData.value.shift()
  }
  updateChart()
}

onMounted(() => {
  initChart()

  timer = setInterval(() => {
    const mockData = {
      city: ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安'][Math.floor(Math.random() * 8)],
      lng: 100 + Math.random() * 30,
      lat: 20 + Math.random() * 30,
      value: Math.floor(Math.random() * 100),
      level: ['HIGH', 'MEDIUM', 'LOW'][Math.floor(Math.random() * 3)]
    }
    addScanPoint(mockData)
  }, 2000)

  const ws = new WebSocket('ws://localhost:3000/ws/scan')
  ws.onmessage = (e) => {
    const data = JSON.parse(e.data)
    if (data.lng && data.lat) {
      addScanPoint({ ...data, level: data.risk === 'HIGH' ? 'HIGH' : data.risk === 'MEDIUM' ? 'MEDIUM' : 'LOW' })
    }
  }
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
  if (chart) chart.dispose()
})

defineExpose({ addScanPoint })
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100%;
  position: relative;
  background: linear-gradient(180deg, #0d1322 0%, #0a0e1a 100%);
  border-radius: 8px;
  overflow: hidden;
}

.map {
  width: 100%;
  height: 100%;
}

.map-overlay {
  position: absolute;
  bottom: 20px;
  left: 20px;
  background: rgba(11, 15, 26, 0.8);
  padding: 12px 16px;
  border-radius: 6px;
  border: 1px solid #1f2a44;
}

.legend {
  display: flex;
  gap: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #a0aec0;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.dot.high { background: #ff4d4f; box-shadow: 0 0 8px #ff4d4f; }
.dot.medium { background: #faad14; box-shadow: 0 0 8px #faad14; }
.dot.low { background: #52c41a; box-shadow: 0 0 8px #52c41a; }
</style>