<template>
  <div class="batch-management">
    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input
        v-model="searchQuery"
        placeholder="搜索批次编号或产品"
        clearable
        style="width: 300px"
        @keyup.enter="handleSearch"
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
      <el-button type="primary" @click="handleSearch" style="margin-left: 10px">
        <el-icon><Search /></el-icon> 搜索
      </el-button>
      <el-button type="primary" @click="handleCreateBatch" style="margin-left: 10px">
        <el-icon><Plus /></el-icon> 创建批次
      </el-button>
    </div>

    <!-- 批次列表 -->
    <div class="batch-table">
      <el-table
        v-loading="loading"
        :data="batchesData"
        style="width: 100%"
        @row-click="handleRowClick"
      >
        <el-table-column prop="batch_no" label="批次编号" width="180" />
        <el-table-column prop="product_name" label="产品" width="150" />
        <el-table-column prop="code_count" label="编码数量" width="100" />
        <el-table-column prop="scan_count" label="扫码次数" width="100" />
        <el-table-column prop="create_time" label="创建时间" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'active' ? 'success' : 'info'">
              {{ scope.row.status === 'active' ? '活跃' : '已结束' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button
              size="small"
              @click.stop="handleViewDetail(scope.row)"
            >
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 批次详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="selectedBatch ? `批次详情 - ${selectedBatch.batch_no}` : '批次详情'"
      width="80%"
      fullscreen
    >
      <div v-if="selectedBatch" class="batch-detail">
        <!-- 批次概览 -->
        <div class="detail-overview">
          <div class="overview-item">
            <span class="label">批次编号：</span>
            <span class="value">{{ selectedBatch.batch_no }}</span>
          </div>
          <div class="overview-item">
            <span class="label">产品名称：</span>
            <span class="value">{{ selectedBatch.product_name }}</span>
          </div>
          <div class="overview-item">
            <span class="label">编码数量：</span>
            <span class="value">{{ selectedBatch.code_count }}</span>
          </div>
          <div class="overview-item">
            <span class="label">扫码次数：</span>
            <span class="value">{{ selectedBatch.scan_count }}</span>
          </div>
          <div class="overview-item">
            <span class="label">创建时间：</span>
            <span class="value">{{ selectedBatch.create_time }}</span>
          </div>
          <div class="overview-item">
            <span class="label">状态：</span>
            <el-tag :type="selectedBatch.status === 'active' ? 'success' : 'info'">
              {{ selectedBatch.status === 'active' ? '活跃' : '已结束' }}
            </el-tag>
          </div>
        </div>

        <!-- 批次二维码总览 -->
        <div class="detail-section">
          <h4>批次二维码总览</h4>
          <div class="qr-code-grid">
            <div v-for="(code, index) in selectedBatch.qr_codes" :key="index" class="qr-code-item">
              <img :src="code.qr_code_url" alt="二维码" />
              <span class="code-text">{{ code.code_id }}</span>
            </div>
          </div>
        </div>

        <!-- 生产时间线 -->
        <div class="detail-section">
          <h4>生产时间线</h4>
          <el-timeline>
            <el-timeline-item
              v-for="(event, index) in selectedBatch.timeline"
              :key="index"
              :timestamp="event.time"
              :type="event.type"
              :icon="event.icon"
            >
              {{ event.content }}
            </el-timeline-item>
          </el-timeline>
        </div>

        <!-- 批次扫码统计 -->
        <div class="detail-section">
          <h4>批次扫码统计</h4>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-value">{{ selectedBatch.scan_stats.total }}</div>
              <div class="stat-label">总扫码次数</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">{{ selectedBatch.scan_stats.normal }}</div>
              <div class="stat-label">正常扫码</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">{{ selectedBatch.scan_stats.warning }}</div>
              <div class="stat-label">可疑扫码</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">{{ selectedBatch.scan_stats.risk }}</div>
              <div class="stat-label">高风险扫码</div>
            </div>
          </div>

          <!-- 扫码趋势图 -->
          <div class="chart-container" style="height: 300px; margin-top: 20px">
            <el-empty description="扫码趋势图开发中" />
          </div>
        </div>
      </div>
    </el-dialog>

    <!-- 创建批次对话框 -->
    <el-dialog
      v-model="createDialogVisible"
      title="创建批次"
      width="500px"
    >
      <el-form :model="createForm" label-width="100px">
        <el-form-item label="批次编号">
          <el-input v-model="createForm.batch_no" placeholder="请输入批次编号" />
        </el-form-item>
        <el-form-item label="产品名称">
          <el-select v-model="createForm.product_id" placeholder="请选择产品" style="width: 100%">
            <el-option v-for="p in products" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="编码数量">
          <el-input-number v-model="createForm.code_count" :min="1" :max="1000" />
        </el-form-item>
        <el-form-item label="生产时间">
          <el-date-picker
            v-model="createForm.production_date"
            type="date"
            placeholder="选择生产时间"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="createDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleCreateBatchSubmit">创建</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Plus } from '@element-plus/icons-vue'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api/admin'

const searchQuery = ref('')
const dateRange = ref([])

const loading = ref(false)
const batchesData = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)

const detailDialogVisible = ref(false)
const selectedBatch = ref(null)

const createDialogVisible = ref(false)
const createForm = ref({
  batch_no: '',
  product_id: null,
  product_name: '',
  code_count: 100,
  production_date: new Date()
})

const products = ref([])

const loadProducts = async () => {
  try {
    const res = await axios.get(`${API_BASE}/products`)
    products.value = res.data
  } catch (error) {
    console.error('加载产品失败:', error)
  }
}

const loadData = async () => {
  loading.value = true
  try {
    const res = await axios.get(`${API_BASE}/batches`)
    batchesData.value = res.data
    total.value = res.data.length
  } catch (error) {
    console.error('加载批次失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadData()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  loadData()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  loadData()
}

const handleRowClick = (row) => {
  handleViewDetail(row)
}

const handleViewDetail = async (row) => {
  selectedBatch.value = row
  detailDialogVisible.value = true
}

const handleCreateBatch = () => {
  createForm.value = {
    batch_no: '',
    product_id: null,
    product_name: '',
    code_count: 100,
    production_date: new Date()
  }
  createDialogVisible.value = true
}

const handleCreateBatchSubmit = async () => {
  if (!createForm.value.batch_no || !createForm.value.product_id) {
    ElMessage.warning('请填写批次编号和选择产品')
    return
  }
  loading.value = true
  try {
    const product = products.value.find(p => p.id === createForm.value.product_id)
    await axios.post('http://localhost:8000/api/code/batch_generate', {
      product_name: product.name,
      batch_no: createForm.value.batch_no,
      count: createForm.value.code_count
    })
    createDialogVisible.value = false
    ElMessage.success('批次创建成功')
    loadData()
  } catch (error) {
    console.error('创建批次失败:', error)
    ElMessage.error('创建批次失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadProducts()
  loadData()
})
</script>

<style scoped>
.batch-management {
  padding: 20px;
  height: 100%;
  overflow: auto;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.batch-table {
  margin-bottom: 20px;
}

.pagination {
  text-align: right;
}

.batch-detail {
  padding: 20px;
}

.detail-overview {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 30px;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
}

.overview-item {
  display: flex;
  align-items: center;
  min-width: 200px;
}

.overview-item .label {
  width: 100px;
  color: #666;
}

.overview-item .value {
  font-weight: bold;
  color: #333;
}

.detail-section {
  margin-bottom: 30px;
}

.detail-section h4 {
  margin-bottom: 15px;
  color: #333;
  border-bottom: 1px solid #eaeaea;
  padding-bottom: 10px;
}

.qr-code-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
}

.qr-code-item {
  text-align: center;
}

.qr-code-item img {
  width: 100px;
  height: 100px;
  margin-bottom: 10px;
}

.qr-code-item .code-text {
  font-size: 12px;
  color: #666;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  background: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #1677FF;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>