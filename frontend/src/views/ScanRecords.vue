<template>
  <div class="scan-records">
    <div class="page-header">
      <h2>扫码记录</h2>
      <div class="filter-bar">
        <el-select v-model="filters.batch" placeholder="选择批次" style="width: 150px; margin-right: 10px;">
          <el-option label="全部批次" value="" />
          <el-option label="批次1" value="batch1" />
          <el-option label="批次2" value="batch2" />
        </el-select>
        <el-select v-model="filters.product" placeholder="选择产品" style="width: 150px; margin-right: 10px;">
          <el-option label="全部产品" value="" />
          <el-option label="产品A" value="productA" />
          <el-option label="产品B" value="productB" />
        </el-select>
        <el-checkbox v-model="filters.repeat" style="margin-right: 10px;">重复扫码</el-checkbox>
        <el-checkbox v-model="filters.highFrequency" style="margin-right: 10px;">高频扫码 (>3次)</el-checkbox>
        <el-button type="primary" @click="applyFilters">应用筛选</el-button>
      </div>
    </div>
    
    <el-table :data="filteredRecords" style="width: 100%">
      <el-table-column prop="time" label="时间" width="180" />
      <el-table-column prop="code" label="编码" width="180" />
      <el-table-column prop="product" label="产品" width="120" />
      <el-table-column prop="ip" label="IP" width="150" />
      <el-table-column prop="region" label="地区" width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.status === '正常' ? 'success' : 'danger'">
            {{ scope.row.status }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>
    
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="filteredRecords.length"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const currentPage = ref(1)
const pageSize = ref(20)
const filters = ref({
  batch: '',
  product: '',
  repeat: false,
  highFrequency: false
})

const records = ref([
  { time: '2026-04-19 10:00:00', code: 'CODE001', product: '产品A', ip: '192.168.1.1', region: '北京', status: '正常' },
  { time: '2026-04-19 10:01:00', code: 'CODE002', product: '产品B', ip: '192.168.1.2', region: '上海', status: '正常' },
  { time: '2026-04-19 10:02:00', code: 'CODE001', product: '产品A', ip: '192.168.1.1', region: '北京', status: '重复' },
  { time: '2026-04-19 10:03:00', code: 'CODE003', product: '产品A', ip: '192.168.1.3', region: '广州', status: '正常' },
  { time: '2026-04-19 10:04:00', code: 'CODE004', product: '产品B', ip: '192.168.1.4', region: '深圳', status: '正常' },
  { time: '2026-04-19 10:05:00', code: 'CODE001', product: '产品A', ip: '192.168.1.1', region: '北京', status: '高频' },
  { time: '2026-04-19 10:06:00', code: 'CODE005', product: '产品A', ip: '192.168.1.5', region: '杭州', status: '正常' },
  { time: '2026-04-19 10:07:00', code: 'CODE006', product: '产品B', ip: '192.168.1.6', region: '成都', status: '正常' }
])

const filteredRecords = computed(() => {
  let result = [...records.value]
  
  if (filters.value.batch) {
    result = result.filter(item => item.batch === filters.value.batch)
  }
  
  if (filters.value.product) {
    result = result.filter(item => item.product === filters.value.product)
  }
  
  if (filters.value.repeat) {
    result = result.filter(item => item.status === '重复')
  }
  
  if (filters.value.highFrequency) {
    result = result.filter(item => item.status === '高频')
  }
  
  return result
})

const applyFilters = () => {
  currentPage.value = 1
}

const handleSizeChange = (size) => {
  pageSize.value = size
}

const handleCurrentChange = (current) => {
  currentPage.value = current
}

onMounted(() => {
  // 模拟加载数据
  console.log('加载扫码记录数据')
})
</script>

<style scoped>
.scan-records {
  padding: 20px;
  background: #fff;
  min-height: calc(100vh - 60px);
}

.page-header {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header h2 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.filter-bar {
  display: flex;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>