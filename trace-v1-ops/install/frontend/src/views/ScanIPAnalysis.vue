<template>
  <div class="scan-ip-container">
    <div class="page-header">
      <h2>IP分析</h2>
    </div>

    <div class="stats-row">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card>
            <div class="stat-item">
              <div class="stat-label">总IP数</div>
              <div class="stat-value">{{ stats.total }}</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card>
            <div class="stat-item">
              <div class="stat-label">活跃IP</div>
              <div class="stat-value">{{ stats.active }}</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card>
            <div class="stat-item">
              <div class="stat-label">异常IP</div>
              <div class="stat-value danger">{{ stats.danger }}</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card>
            <div class="stat-item">
              <div class="stat-label">黑名单IP</div>
              <div class="stat-value danger">{{ stats.blacklist }}</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <el-card style="margin-top: 20px">
      <template #header>
        <span>IP分布TOP20</span>
      </template>
      <el-table :data="ipData" v-loading="loading" style="width: 100%">
        <el-table-column prop="rank" label="排名" width="80" />
        <el-table-column prop="ip" label="IP地址" width="180" />
        <el-table-column prop="location" label="地理位置" />
        <el-table-column prop="scan_count" label="扫码次数" width="120" />
        <el-table-column prop="code_count" label="扫码码数" width="120" />
        <el-table-column prop="first_time" label="首次扫码" width="180" />
        <el-table-column prop="last_time" label="最近扫码" width="180" />
        <el-table-column prop="risk_level" label="风险等级" width="100">
          <template #default="scope">
            <el-tag :type="getRiskType(scope.row.risk_level)">
              {{ getRiskText(scope.row.risk_level) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button size="small" type="primary" link @click="handleViewDetail(scope.row)">
              详情
            </el-button>
            <el-button
              v-if="scope.row.risk_level > 1"
              size="small"
              type="danger"
              link
              @click="handleBlacklist(scope.row)"
            >
              黑名单
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-card style="margin-top: 20px">
      <template #header>
        <span>扫码时间分布</span>
      </template>
      <div ref="chartRef" style="width: 100%; height: 300px"></div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const chartRef = ref(null)

const stats = ref({
  total: 1256,
  active: 892,
  danger: 45,
  blacklist: 12
})

const ipData = ref([
  { rank: 1, ip: '192.168.1.101', location: '北京市海淀区', scan_count: 1256, code_count: 456, first_time: '2026-04-01 08:00:00', last_time: '2026-04-19 10:30:00', risk_level: 1 },
  { rank: 2, ip: '192.168.1.102', location: '上海市浦东新区', scan_count: 892, code_count: 321, first_time: '2026-04-01 09:00:00', last_time: '2026-04-19 09:20:00', risk_level: 1 },
  { rank: 3, ip: '192.168.1.103', location: '广州市天河区', scan_count: 756, code_count: 289, first_time: '2026-04-02 10:00:00', last_time: '2026-04-19 08:15:00', risk_level: 2 },
  { rank: 4, ip: '192.168.1.104', location: '深圳市南山区', scan_count: 623, code_count: 234, first_time: '2026-04-01 11:00:00', last_time: '2026-04-18 22:30:00', risk_level: 1 },
  { rank: 5, ip: '192.168.1.105', location: '杭州市西湖区', scan_count: 456, code_count: 178, first_time: '2026-04-03 14:00:00', last_time: '2026-04-19 07:45:00', risk_level: 3 }
])

const getRiskType = (level) => {
  const map = { 1: 'success', 2: 'warning', 3: 'danger' }
  return map[level] || 'info'
}

const getRiskText = (level) => {
  const map = { 1: '低风险', 2: '中风险', 3: '高风险' }
  return map[level] || '未知'
}

const handleViewDetail = (row) => {
  ElMessage.info(`查看IP详情: ${row.ip}`)
}

const handleBlacklist = (row) => {
  ElMessage.warning(`已将 ${row.ip} 加入黑名单`)
}

onMounted(() => {
  loading.value = false
})
</script>

<style scoped>
.scan-ip-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.stat-item {
  text-align: center;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #333;
}

.stat-value.danger {
  color: #f56c6c;
}
</style>
