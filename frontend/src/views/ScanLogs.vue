<template>
  <div class="scan-logs-container">
    <div class="page-header">
      <h2>扫码日志</h2>
    </div>

    <div class="search-bar">
      <el-input
        v-model="searchQuery"
        placeholder="搜索溯源码或产品"
        clearable
        style="width: 300px"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        style="width: 240px; margin-left: 10px"
      />
      <el-select v-model="statusFilter" placeholder="状态筛选" style="width: 150px; margin-left: 10px">
        <el-option label="全部" value="" />
        <el-option label="正常" value="normal" />
        <el-option label="预警" value="warning" />
        <el-option label="异常" value="danger" />
      </el-select>
      <el-button type="primary" @click="handleSearch" style="margin-left: 10px">
        <el-icon><Search /></el-icon> 搜索
      </el-button>
    </div>

    <el-card style="margin-top: 20px">
      <el-table :data="logsData" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="code_id" label="溯源码" width="180">
          <template #default="scope">
            <el-link type="primary" @click="handleViewCode(scope.row)">
              {{ scope.row.code_id }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column prop="ip" label="IP地址" width="150" />
        <el-table-column prop="scan_time" label="扫码时间" width="180">
          <template #default="scope">
            {{ new Date(scope.row.scan_time).toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="is_first" label="首扫" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.is_first ? 'success' : 'info'">
              {{ scope.row.is_first ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="user_agent" label="设备" width="200" />
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button size="small" type="primary" link @click="handleViewDetail(scope.row)">
              详情
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
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api/admin'

const searchQuery = ref('')
const dateRange = ref([])
const statusFilter = ref('')
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const logsData = ref([])

const loadData = async () => {
  loading.value = true
  try {
    const res = await axios.get(`${API_BASE}/scan-logs`)
    logsData.value = res.data
    total.value = res.data.length
  } catch (error) {
    console.error('加载扫码日志失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadData()
}

const handleSizeChange = () => {
  loadData()
}

const handleCurrentChange = () => {
  loadData()
}

const handleViewCode = (row) => {
  ElMessage.info(`查看溯源码: ${row.code_id}`)
}

const handleViewDetail = (row) => {
  ElMessage.info(`查看详情: ${row.code_id}`)
}

const getStatusType = (status) => {
  const map = { normal: 'success', warning: 'warning', danger: 'danger' }
  return map[status] || 'info'
}

const getStatusText = (status) => {
  const map = { normal: '正常', warning: '预警', danger: '异常' }
  return map[status] || '未知'
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.scan-logs-container {
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

.search-bar {
  display: flex;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
