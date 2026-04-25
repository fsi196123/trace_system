<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h2>系统运行总览（睿码溯源）</h2>
      <div class="dashboard-actions">
        <el-button @click="exportExcel" type="primary">导出Excel</el-button>
        <el-button @click="exportZip" type="success">导出二维码ZIP</el-button>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-title">今日溯源</div>
        <div class="stat-value">{{ stats.today }}</div>
        <div class="stat-change positive">+12.5%</div>
      </div>
      <div class="stat-card">
        <div class="stat-title">异常溯源码</div>
        <div class="stat-value">{{ stats.abnormal }}</div>
        <div class="stat-change negative">+3.2%</div>
      </div>
      <div class="stat-card">
        <div class="stat-title">总溯源量</div>
        <div class="stat-value">{{ stats.total }}</div>
        <div class="stat-change positive">+8.7%</div>
      </div>
      <div class="stat-card">
        <div class="stat-title">溯源率</div>
        <div class="stat-value">{{ stats.rate }}%</div>
        <div class="stat-change positive">+2.1%</div>
      </div>
    </div>

    <div class="charts-grid">
      <div class="chart-card">
        <div class="chart-header">
          <h3>全国溯源扫码分布</h3>
        </div>
        <div class="chart-content">
          <div class="no-data">地图数据加载中...</div>
        </div>
      </div>
      <div class="chart-card">
        <div class="chart-header">
          <h3>溯源异常预警</h3>
        </div>
        <div class="chart-content">
          <div class="alert-container">
            <div class="alert-list" v-if="alerts.length > 0">
              <div class="alert-item" v-for="(alert, index) in alerts" :key="index">
                <div class="code">🚨 异常溯源码: {{ alert.code_id }}</div>
                <div class="info">城市: {{ alert.city }} | IP: {{ alert.ip }} | 溯源: {{ alert.count }}次</div>
              </div>
            </div>
            <div class="no-data" v-else>暂无预警信息</div>
          </div>
        </div>
      </div>
    </div>

    <div class="recent-records">
      <h3>最近溯源记录</h3>
      <div class="records-table">
        <table>
          <thead>
            <tr>
              <th>时间</th>
              <th>溯源码</th>
              <th>产品</th>
              <th>地点</th>
              <th>状态</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in recentRecords" :key="record.id">
              <td>{{ record.time }}</td>
              <td>{{ record.code }}</td>
              <td>{{ record.product }}</td>
              <td>{{ record.location }}</td>
              <td>
                <span class="status-tag" :class="record.status">
                  {{ record.status === 'success' ? '正常' : '异常' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api/admin'

const stats = ref({
  today: 0,
  abnormal: 0,
  total: 0,
  rate: 0
})

const recentRecords = ref([])

const alerts = ref([])

const loadStats = async () => {
  try {
    const res = await axios.get(`${API_BASE}/dashboard/stats`)
    stats.value = {
      today: res.data.today_scan || 0,
      abnormal: 0,
      total: res.data.total_codes || 0,
      rate: res.data.total_codes > 0 ? 99.5 : 0
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

const loadRecentRecords = async () => {
  try {
    const res = await axios.get(`${API_BASE}/recent-scans`)
    recentRecords.value = res.data.slice(0, 5).map(item => ({
      id: item.id || 0,
      time: item.scan_time,
      code: item.code_id,
      product: item.product_name,
      location: '-',
      status: item.is_first ? 'success' : 'abnormal'
    }))
  } catch (error) {
    console.error('加载最近记录失败:', error)
  }
}

const exportExcel = () => {
  window.open('http://localhost:8000/api/code/export/excel')
}

const exportZip = () => {
  window.open('http://localhost:8000/api/code/export/zip')
}

onMounted(() => {
  loadStats()
  loadRecentRecords()
  setInterval(() => {
    loadStats()
    loadRecentRecords()
  }, 30000)
})
</script>

<style scoped>
.dashboard-container {
  height: 100%;
  overflow: auto;
  padding: 20px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.dashboard-header h2 {
  color: #00ffcc;
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}

.dashboard-actions {
  display: flex;
  gap: 10px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.stat-title {
  color: #94a3b8;
  font-size: 14px;
  margin-bottom: 10px;
}

.stat-value {
  color: #ffffff;
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-change {
  font-size: 12px;
  font-weight: bold;
}

.stat-change.positive {
  color: #10b981;
}

.stat-change.negative {
  color: #ef4444;
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.chart-card {
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid #334155;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.chart-header {
  padding: 15px 20px;
  border-bottom: 1px solid #334155;
  background: rgba(15, 23, 42, 0.8);
}

.chart-header h3 {
  color: #00ffcc;
  font-size: 16px;
  font-weight: bold;
  margin: 0;
}

.chart-content {
  padding: 20px;
  height: 400px;
}

.alert-container {
  height: 100%;
  overflow: hidden;
}

.alert-list {
  max-height: 100%;
  overflow-y: auto;
}

.alert-item {
  background: rgba(255, 68, 68, 0.1);
  border-left: 3px solid #ff4444;
  padding: 10px;
  margin-bottom: 8px;
  border-radius: 5px;
  animation: pulse-alert 2s infinite;
}

@keyframes pulse-alert {
  0%, 100% { background: rgba(255, 68, 68, 0.1); }
  50% { background: rgba(255, 68, 68, 0.2); }
}

.alert-item .code {
  color: #ff4444;
  font-weight: bold;
  font-size: 13px;
}

.alert-item .info {
  color: #8899aa;
  font-size: 11px;
  margin-top: 5px;
}

.recent-records {
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.recent-records h3 {
  color: #00ffcc;
  font-size: 16px;
  font-weight: bold;
  margin: 0 0 15px 0;
}

.records-table {
  overflow-x: auto;
}

.records-table table {
  width: 100%;
  border-collapse: collapse;
}

.records-table th,
.records-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #334155;
}

.records-table th {
  color: #94a3b8;
  font-size: 14px;
  font-weight: bold;
}

.records-table td {
  color: #e2e8f0;
  font-size: 14px;
}

.status-tag {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
}

.status-tag.success {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.status-tag.abnormal {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.no-data {
  text-align: center;
  color: #667788;
  padding: 30px;
  font-size: 14px;
}

@media (max-width: 768px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }
}
</style>