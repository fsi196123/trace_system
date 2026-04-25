<template>
  <div class="risk-warning-container">
    <div class="page-header">
      <h2>风险预警</h2>
    </div>

    <div class="stats-row">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card>
            <div class="stat-item">
              <div class="stat-label">今日预警</div>
              <div class="stat-value warning">{{ stats.today }}</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card>
            <div class="stat-item">
              <div class="stat-label">本周预警</div>
              <div class="stat-value warning">{{ stats.week }}</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card>
            <div class="stat-item">
              <div class="stat-label">本月预警</div>
              <div class="stat-value">{{ stats.month }}</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card>
            <div class="stat-item">
              <div class="stat-label">黑名单</div>
              <div class="stat-value danger">{{ stats.blacklist }}</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <el-card style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <span>风险预警列表</span>
          <el-select v-model="riskLevel" placeholder="风险等级" style="width: 150px">
            <el-option label="全部" value="" />
            <el-option label="高风险" value="3" />
            <el-option label="中风险" value="2" />
            <el-option label="低风险" value="1" />
          </el-select>
        </div>
      </template>
      <el-table :data="warningData" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="code_id" label="溯源码" width="180">
          <template #default="scope">
            <el-link type="primary">{{ scope.row.code_id }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="warning_type" label="预警类型" width="150">
          <template #default="scope">
            <el-tag :type="getWarningType(scope.row.warning_type)">
              {{ scope.row.warning_type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="预警描述" />
        <el-table-column prop="location" label="发生地点" width="150" />
        <el-table-column prop="ip" label="IP地址" width="150" />
        <el-table-column prop="risk_level" label="风险等级" width="100">
          <template #default="scope">
            <el-tag :type="getRiskType(scope.row.risk_level)">
              {{ getRiskText(scope.row.risk_level) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="发生时间" width="180" />
        <el-table-column label="操作" width="180">
          <template #default="scope">
            <el-button size="small" type="primary" link>处理</el-button>
            <el-button size="small" type="success" link>标记已处理</el-button>
            <el-button
              v-if="scope.row.risk_level === 3"
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

      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const riskLevel = ref('')
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const stats = ref({
  today: 12,
  week: 45,
  month: 156,
  blacklist: 23
})

const warningData = ref([])

const mockWarnings = Array.from({ length: 30 }, (_, index) => ({
  id: index + 1,
  code_id: `CODE${String(index + 1).padStart(6, '0')}`,
  warning_type: ['频繁验证', '异地验证', '异常设备', '疑似造假'][index % 4],
  description: '该溯源码在短时间内被多次验证，或验证地点异常',
  location: ['北京市海淀区', '上海市浦东新区', '广州市天河区', '深圳市南山区'][index % 4],
  ip: `192.168.1.${100 + index}`,
  risk_level: Math.floor(Math.random() * 3) + 1,
  create_time: new Date(Date.now() - Math.random() * 86400000 * 7).toLocaleString(),
  status: Math.random() > 0.5 ? 'pending' : 'resolved'
}))

const loadData = () => {
  loading.value = true
  setTimeout(() => {
    warningData.value = mockWarnings.slice((currentPage.value - 1) * pageSize.value, currentPage.value * pageSize.value)
    total.value = mockWarnings.length
    loading.value = false
  }, 500)
}

const getWarningType = (type) => {
  const map = { '频繁验证': 'warning', '异地验证': 'danger', '异常设备': 'danger', '疑似造假': 'danger' }
  return map[type] || 'info'
}

const getRiskType = (level) => {
  const map = { 1: 'success', 2: 'warning', 3: 'danger' }
  return map[level] || 'info'
}

const getRiskText = (level) => {
  const map = { 1: '低风险', 2: '中风险', 3: '高风险' }
  return map[level] || '未知'
}

const handleBlacklist = (row) => {
  ElMessage.warning(`已将 ${row.ip} 加入黑名单`)
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.risk-warning-container {
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

.stat-value.warning {
  color: #e6a23c;
}

.stat-value.danger {
  color: #f56c6c;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
