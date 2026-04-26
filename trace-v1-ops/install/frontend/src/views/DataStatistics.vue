<template>
  <div class="data-statistics">
    <div class="page-header">
      <h2>数据统计</h2>
    </div>
    
    <div class="stats-cards">
      <el-card class="stat-card">
        <div class="stat-item">
          <div class="stat-value">{{ todayScans }}</div>
          <div class="stat-label">今日扫码量</div>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-item">
          <div class="stat-value">{{ totalScans }}</div>
          <div class="stat-label">总扫码量</div>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-item">
          <div class="stat-value">{{ exceptionCodes }}</div>
          <div class="stat-label">异常码数量</div>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-item">
          <div class="stat-value">{{ totalCodes }}</div>
          <div class="stat-label">总溯源码数</div>
        </div>
      </el-card>
    </div>
    
    <div class="charts-container">
      <el-card class="chart-card">
        <template #header>
          <div class="chart-header">
            <span>扫码趋势</span>
          </div>
        </template>
        <div class="chart-content">
          <div ref="trendChart" class="chart"></div>
        </div>
      </el-card>
      
      <el-card class="chart-card">
        <template #header>
          <div class="chart-header">
            <span>批次排行</span>
          </div>
        </template>
        <div class="chart-content">
          <div ref="batchChart" class="chart"></div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const todayScans = ref(128)
const totalScans = ref(3245)
const exceptionCodes = ref(12)
const totalCodes = ref(10000)

const trendChart = ref(null)
const batchChart = ref(null)
let trendChartInstance = null
let batchChartInstance = null

onMounted(() => {
  initCharts()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (trendChartInstance) {
    trendChartInstance.dispose()
  }
  if (batchChartInstance) {
    batchChartInstance.dispose()
  }
})

const initCharts = () => {
  // 扫码趋势图
  if (trendChart.value) {
    trendChartInstance = echarts.init(trendChart.value)
    trendChartInstance.setOption({
      tooltip: {
        trigger: 'axis'
      },
      xAxis: {
        type: 'category',
        data: ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00']
      },
      yAxis: {
        type: 'value'
      },
      series: [{
        data: [12, 20, 15, 25, 30, 28, 35],
        type: 'line',
        smooth: true,
        areaStyle: {}
      }]
    })
  }
  
  // 批次排行图
  if (batchChart.value) {
    batchChartInstance = echarts.init(batchChart.value)
    batchChartInstance.setOption({
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      xAxis: {
        type: 'category',
        data: ['批次1', '批次2', '批次3', '批次4', '批次5']
      },
      yAxis: {
        type: 'value'
      },
      series: [{
        data: [320, 280, 240, 180, 120],
        type: 'bar'
      }]
    })
  }
}

const handleResize = () => {
  if (trendChartInstance) {
    trendChartInstance.resize()
  }
  if (batchChartInstance) {
    batchChartInstance.resize()
  }
}
</script>

<style scoped>
.data-statistics {
  padding: 20px;
  background: #fff;
  min-height: calc(100vh - 60px);
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.stat-item {
  padding: 20px 0;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #1677FF;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.charts-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.chart-card {
  height: 300px;
}

.chart-header {
  font-size: 14px;
  font-weight: bold;
  color: #333;
}

.chart-content {
  height: calc(100% - 40px);
}

.chart {
  width: 100%;
  height: 100%;
}

@media (max-width: 1200px) {
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .charts-container {
    grid-template-columns: 1fr;
  }
}
</style>