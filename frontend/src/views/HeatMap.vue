<template>
  <div ref="chartRef" class="heatmap-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

const chartRef = ref(null)
let chart = null
let heatData = []
let ws = null

const initChart = () => {
  if (!chartRef.value) return

  chart = echarts.init(chartRef.value)

  const option = {
    backgroundColor: 'transparent',
    title: {
      text: '全国扫码实时热力图',
      left: 'center',
      textStyle: {
        color: '#00ffcc',
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: function(params) {
        return params.name + '<br/>扫码次数: ' + params.value[2]
      },
      backgroundColor: 'rgba(26, 39, 68, 0.9)',
      borderColor: '#00ffcc',
      textStyle: {
        color: '#00ffcc'
      }
    },
    visualMap: {
      min: 0,
      max: 10,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '10px',
      textStyle: {
        color: '#00ffcc'
      },
      inRange: {
        color: ['#00ffcc', '#0088ff', '#0044ff', '#ff0088']
      }
    },
    geo: {
      map: 'china',
      roam: true,
      zoom: 1.2,
      label: {
        show: false
      },
      itemStyle: {
        areaColor: '#1b1b1b',
        borderColor: '#4f4f4f'
      },
      emphasis: {
        itemStyle: {
          areaColor: '#2a3a5e',
          borderColor: '#00ffcc'
        },
        label: {
          show: true,
          color: '#00ffcc'
        }
      }
    },
    series: [
      {
        name: '扫码热力',
        type: 'heatmap',
        coordinateSystem: 'geo',
        data: heatData,
        pointSize: 6,
        blurSize: 10,
        label: {
          show: false
        },
        emphasis: {
          label: {
            show: true,
            formatter: function(params) {
              return params.name + ': ' + params.value[2]
            },
            color: '#00ffcc'
          }
        }
      },
      {
        name: '高风险点',
        type: 'effectScatter',
        coordinateSystem: 'geo',
        data: [],
        symbolSize: function(val) {
          return Math.max(10, Math.min(25, val[2] * 1.5))
        },
        showEffectOn: 'render',
        rippleEffect: {
          brushType: 'stroke',
          scale: 3
        },
        itemStyle: {
          color: '#ff4444',
          shadowBlur: 10,
          shadowColor: '#ff4444'
        },
        emphasis: {
          scale: true
        }
      }
    ]
  }

  chart.setOption(option)

  window.addEventListener('resize', () => {
    chart.resize()
  })
}

const fetchChinaMap = async () => {
  try {
    const response = await fetch('https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json')
    const chinaMap = await response.json()
    echarts.registerMap('china', chinaMap)
    initChart()
  } catch (error) {
    console.error('Fetch china map error:', error)
    initChart()
  }
}

import { createWS } from '../utils/ws'

const initWebSocket = () => {
  const ws = createWS()
  
  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      if (data.lng && data.lat) {
        const existingPoint = heatData.find(point => point[0] === data.lng && point[1] === data.lat)
        if (existingPoint) {
          existingPoint[2]++
        } else {
          heatData.push([data.lng, data.lat, 1])
        }
        
        if (data.risk_level === 'high') {
          const scatterData = chart.getOption().series[1].data
          scatterData.push([data.lng, data.lat, 1])
          if (scatterData.length > 20) {
            scatterData.shift()
          }
          chart.setOption({
            series: [
              { data: heatData },
              { data: scatterData }
            ]
          })
        } else {
          chart.setOption({
            series: [
              { data: heatData },
              {}
            ]
          })
        }
      }
    } catch (error) {
      console.error('WebSocket message error:', error)
    }
  }
  
  ws.onclose = () => {
    console.log('WebSocket disconnected')
    setTimeout(() => {
      initWebSocket()
    }, 5000)
  }
  
  return ws
}

const getCityCoords = (city) => {
  const cityCoords = {
    '北京': [116.40, 39.90],
    '上海': [121.47, 31.23],
    '广州': [113.26, 23.13],
    '深圳': [114.06, 22.54],
    '杭州': [120.21, 30.25],
    '成都': [104.07, 30.67],
    '重庆': [106.55, 29.56],
    '武汉': [114.30, 30.58],
    '西安': [108.94, 34.34],
    '南京': [118.78, 32.06],
    '天津': [117.20, 39.12],
    '苏州': [120.62, 31.30],
    '郑州': [113.62, 34.75],
    '长沙': [112.98, 28.20],
    '沈阳': [123.43, 41.80],
    '青岛': [120.38, 36.07],
    '宁波': [121.55, 29.87],
    '东莞': [113.75, 23.04],
    '无锡': [120.29, 31.57],
    '昆明': [102.71, 25.04],
    '合肥': [117.28, 31.86],
    '福州': [119.30, 26.08],
    '厦门': [118.09, 24.48],
    '哈尔滨': [126.63, 45.80],
    '长春': [125.32, 43.82],
    '石家庄': [114.48, 38.03],
    '南昌': [115.89, 28.69],
    '贵阳': [106.71, 26.60],
    '太原': [112.55, 37.87],
    '南宁': [108.33, 22.82],
    '海口': [110.35, 20.02],
    '济南': [116.99, 36.67],
    '大连': [121.62, 38.91]
  }
  return cityCoords[city] || [116.40, 39.90]
}

onMounted(() => {
  fetchChinaMap()
  ws = initWebSocket()
})

onUnmounted(() => {
  if (chart) {
    chart.dispose()
  }
  if (ws) {
    ws.close()
  }
  window.removeEventListener('resize', () => {
    chart.resize()
  })
})
</script>

<style scoped>
.heatmap-container {
  width: 100%;
  height: 100%;
  min-height: 400px;
}
</style>