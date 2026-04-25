<template>
  <div class="verify-records-container">
    <div class="page-header">
      <h2>验证记录</h2>
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
      <el-select v-model="verifyResult" placeholder="验证结果" style="width: 150px; margin-left: 10px">
        <el-option label="全部" value="" />
        <el-option label="验证成功" value="success" />
        <el-option label="验证失败" value="fail" />
        <el-option label="风险预警" value="warning" />
      </el-select>
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        style="width: 240px; margin-left: 10px"
      />
      <el-button type="primary" @click="handleSearch" style="margin-left: 10px">
        <el-icon><Search /></el-icon> 搜索
      </el-button>
    </div>

    <el-card style="margin-top: 20px">
      <el-table :data="recordsData" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="code_id" label="溯源码" width="180">
          <template #default="scope">
            <el-link type="primary">{{ scope.row.code_id }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="product_name" label="产品" />
        <el-table-column prop="verify_time" label="验证时间" width="180" />
        <el-table-column prop="verify_location" label="验证地点" width="150" />
        <el-table-column prop="verify_result" label="验证结果" width="120">
          <template #default="scope">
            <el-tag :type="getResultType(scope.row.verify_result)">
              {{ getResultText(scope.row.verify_result) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="risk_level" label="风险等级" width="100">
          <template #default="scope">
            <el-tag :type="getRiskType(scope.row.risk_level)">
              {{ getRiskText(scope.row.risk_level) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button size="small" type="primary" link>详情</el-button>
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
import { Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const searchQuery = ref('')
const verifyResult = ref('')
const dateRange = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const recordsData = ref([])

const mockRecords = Array.from({ length: 50 }, (_, index) => ({
  id: index + 1,
  code_id: `CODE${String(index + 1).padStart(6, '0')}`,
  product_name: ['智能测试产品', '优质农产品', '精选食品'][index % 3],
  verify_time: new Date(Date.now() - Math.random() * 86400000 * 7).toLocaleString(),
  verify_location: ['北京市海淀区', '上海市浦东新区', '广州市天河区'][index % 3],
  verify_result: ['success', 'fail', 'warning'][Math.floor(Math.random() * 3)],
  risk_level: Math.floor(Math.random() * 3) + 1
}))

const loadData = () => {
  loading.value = true
  setTimeout(() => {
    recordsData.value = mockRecords.slice((currentPage.value - 1) * pageSize.value, currentPage.value * pageSize.value)
    total.value = mockRecords.length
    loading.value = false
  }, 500)
}

const handleSearch = () => {
  currentPage.value = 1
  loadData()
}

const getResultType = (result) => {
  const map = { success: 'success', fail: 'danger', warning: 'warning' }
  return map[result] || 'info'
}

const getResultText = (result) => {
  const map = { success: '验证成功', fail: '验证失败', warning: '风险预警' }
  return map[result] || '未知'
}

const getRiskType = (level) => {
  const map = { 1: 'success', 2: 'warning', 3: 'danger' }
  return map[level] || 'info'
}

const getRiskText = (level) => {
  const map = { 1: '低风险', 2: '中风险', 3: '高风险' }
  return map[level] || '未知'
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.verify-records-container {
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
