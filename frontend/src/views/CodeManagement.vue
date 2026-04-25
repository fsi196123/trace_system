<template>
  <div class="code-management">
    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input
        v-model="searchQuery"
        placeholder="搜索编码、产品或批次"
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
    </div>

    <!-- 操作按钮 -->
    <div class="action-buttons">
      <el-button type="primary" @click="handleBatchGenerate">
        <el-icon><Plus /></el-icon> 批量生成
      </el-button>
      <el-button type="primary" @click="handleSingleGenerate">
        <el-icon><Plus /></el-icon> 单个生成
      </el-button>
      <el-button type="danger" @click="handleBatchDelete" :disabled="selectedRows.length === 0">
        <el-icon><Delete /></el-icon> 批量删除
      </el-button>
      <el-select v-model="statusFilter" placeholder="状态筛选" clearable style="width: 120px; margin-left: 10px" @change="handleStatusFilter">
        <el-option label="全部" value="" />
        <el-option label="正常" value="normal" />
        <el-option label="可疑" value="warning" />
        <el-option label="高危" value="danger" />
      </el-select>
      <el-button @click="handleExportExcel">
        <el-icon><Download /></el-icon> 导出Excel
      </el-button>
      <el-button @click="handleExportQrCode">
        <el-icon><Picture /></el-icon> 导出二维码ZIP
      </el-button>
      <el-button @click="handleRefresh">
        <el-icon><Refresh /></el-icon> 刷新
      </el-button>
    </div>

    <!-- 表格列表 -->
    <div class="code-table">
      <el-table
        v-loading="loading"
        :data="codesData"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="code_id" label="编码" width="180" />
        <el-table-column prop="product_name" label="产品" width="150" />
        <el-table-column prop="batch_no" label="批次" width="150" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag
              :type="scope.row.status === 'normal' ? 'success' : scope.row.status === 'warning' ? 'warning' : 'danger'"
            >
              {{ scope.row.status === 'normal' ? '正常' : scope.row.status === 'warning' ? '可疑' : '高危' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="scan_count" label="扫码数" width="80" />
        <el-table-column prop="create_time" label="创建时间" width="180" />
        <el-table-column prop="first_scan_time" label="首次扫码" width="180" />
        <el-table-column label="操作" width="180">
          <template #default="scope">
            <el-button size="small" @click="handleViewDetail(scope.row)">
              详情
            </el-button>
            <el-button size="small" type="danger" @click="handleRemove(scope.row)">
              删除
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

    <!-- 详情抽屉 -->
    <el-drawer
      v-model="drawerVisible"
      title="编码详情"
      size="70%"
    >
      <div v-if="selectedCode" class="code-detail">
        <div class="detail-header">
          <div class="qr-code">
            <img :src="selectedCode.qr_code_url" alt="二维码" />
          </div>
          <div class="code-info">
            <h3>{{ selectedCode.code_id }}</h3>
            <div class="info-item">
              <span class="label">产品：</span>
              <span class="value">{{ selectedCode.product_name }}</span>
            </div>
            <div class="info-item">
              <span class="label">批次：</span>
              <span class="value">{{ selectedCode.batch_no }}</span>
            </div>
            <div class="info-item">
              <span class="label">状态：</span>
              <el-tag
                :type="selectedCode.status === 'normal' ? 'success' : selectedCode.status === 'warning' ? 'warning' : 'danger'"
              >
                {{ selectedCode.status === 'normal' ? '正常' : selectedCode.status === 'warning' ? '可疑' : '高危' }}
              </el-tag>
            </div>
            <div class="info-item">
              <span class="label">扫码次数：</span>
              <span class="value">{{ selectedCode.scan_count }}</span>
            </div>
            <div class="info-item">
              <span class="label">创建时间：</span>
              <span class="value">{{ selectedCode.create_time }}</span>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h4>签名信息</h4>
          <div class="signature-info">
            <pre>{{ selectedCode.signature }}</pre>
          </div>
        </div>

        <div class="detail-section">
          <h4>扫码记录</h4>
          <el-table :data="selectedCode.scan_logs" style="width: 100%">
            <el-table-column prop="scan_time" label="扫码时间" width="180" />
            <el-table-column prop="ip" label="IP地址" width="150" />
            <el-table-column prop="location" label="位置" width="150" />
            <el-table-column prop="user_agent" label="设备信息" />
          </el-table>
        </div>
      </div>
    </el-drawer>

    <!-- 批量生成对话框 -->
    <el-dialog
      v-model="generateDialogVisible"
      title="批量生成编码"
      width="500px"
    >
      <el-form :model="generateForm" label-width="100px">
        <el-form-item label="产品名称">
          <el-input v-model="generateForm.product_name" placeholder="请输入产品名称" />
        </el-form-item>
        <el-form-item label="批次编号">
          <el-input v-model="generateForm.batch_no" placeholder="请输入批次编号" />
        </el-form-item>
        <el-form-item label="生成数量">
          <el-input-number v-model="generateForm.count" :min="1" :max="1000" />
        </el-form-item>
        <el-form-item label="有效期">
          <el-date-picker
            v-model="generateForm.expire_date"
            type="date"
            placeholder="选择有效期"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="generateDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleGenerateCodes">生成</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 单个生成对话框 -->
    <el-dialog
      v-model="singleGenerateDialogVisible"
      title="单个生成编码"
      width="500px"
    >
      <el-form :model="singleGenerateForm" label-width="100px">
        <el-form-item label="产品名称">
          <el-input v-model="singleGenerateForm.product_name" placeholder="请输入产品名称" />
        </el-form-item>
        <el-form-item label="批次编号">
          <el-input v-model="singleGenerateForm.batch_no" placeholder="请输入批次编号" />
        </el-form-item>
        <el-form-item label="有效期">
          <el-date-picker
            v-model="singleGenerateForm.expire_date"
            type="date"
            placeholder="选择有效期"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="singleGenerateDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSingleGenerateCode">生成</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus, Download, Picture, Refresh, Delete } from '@element-plus/icons-vue'

// 搜索和筛选
const searchQuery = ref('')
const dateRange = ref([])
const statusFilter = ref('')

// 表格数据
const loading = ref(false)
const codesData = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const selectedRows = ref([])

// 详情抽屉
const drawerVisible = ref(false)
const selectedCode = ref(null)

// 批量生成对话框
const generateDialogVisible = ref(false)
const generateForm = ref({
  product_name: '',
  batch_no: '',
  count: 10,
  expire_date: null
})

// 单个生成对话框
const singleGenerateDialogVisible = ref(false)
const singleGenerateForm = ref({
  product_name: '',
  batch_no: '',
  expire_date: null
})

// 模拟数据
const mockCodes = Array.from({ length: 50 }, (_, index) => ({
  code_id: `CODE${String(index + 1).padStart(6, '0')}`,
  product_name: index % 3 === 0 ? '智能测试产品' : '测试产品',
  batch_no: index % 2 === 0 ? 'BATCH20260419001' : 'BATCH20260419002',
  status: index % 5 === 0 ? 'danger' : index % 3 === 0 ? 'warning' : 'normal',
  scan_count: Math.floor(Math.random() * 10),
  create_time: new Date(Date.now() - Math.random() * 86400000 * 7).toLocaleString(),
  first_scan_time: Math.random() > 0.5 ? new Date(Date.now() - Math.random() * 86400000 * 3).toLocaleString() : '-',
  qr_code_url: 'https://neeko-copilot.bytedance.net/api/text2image?prompt=QR%20code%20for%20authentication&size=512x512',
  signature: '-----BEGIN SIGNATURE-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...\n-----END SIGNATURE-----',
  scan_logs: Array.from({ length: Math.floor(Math.random() * 5) }, (_, logIndex) => ({
    scan_time: new Date(Date.now() - Math.random() * 86400000 * 2).toLocaleString(),
    ip: `192.168.1.${Math.floor(Math.random() * 255)}`,
    location: ['北京', '上海', '广州', '深圳', '杭州'][Math.floor(Math.random() * 5)],
    user_agent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'
  }))
}))

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const res = await axios.get('http://localhost:8000/api/code/list')
    codesData.value = res.data
    total.value = res.data.length
  } catch (error) {
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  loadData()
}

// 刷新
const handleRefresh = () => {
  loadData()
}

// 分页
const handleSizeChange = (size) => {
  pageSize.value = size
  loadData()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  loadData()
}

// 选择
const handleSelectionChange = (rows) => {
  selectedRows.value = rows
}

// 查看详情
const handleViewDetail = (row) => {
  selectedCode.value = row
  drawerVisible.value = true
}

// 删除单个编码
const handleRemove = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除编码 ${row.code_id} 吗？`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    loading.value = true
    await axios.delete(`http://localhost:8000/api/code/${row.code_id}`)
    ElMessage.success('删除成功')
    loadData()
  } catch {
    // 用户取消
  } finally {
    loading.value = false
  }
}

// 批量生成
const handleBatchGenerate = () => {
  generateDialogVisible.value = true
}

// 单个生成
const handleSingleGenerate = () => {
  singleGenerateDialogVisible.value = true
}

// 生成编码
const handleGenerateCodes = async () => {
  if (!generateForm.value.product_name || !generateForm.value.batch_no) {
    ElMessage.warning('请填写产品名称和批次编号')
    return
  }
  
  loading.value = true
  try {
    await axios.post('http://localhost:8000/api/code/batch_generate', {
      product_name: generateForm.value.product_name,
      batch_no: generateForm.value.batch_no,
      count: generateForm.value.count
    })
    generateDialogVisible.value = false
    ElMessage.success(`成功生成 ${generateForm.value.count} 个编码`)
    generateForm.value = {
      product_name: '',
      batch_no: '',
      count: 10,
      expire_date: null
    }
    loadData()
  } catch (error) {
    ElMessage.error('生成失败')
  } finally {
    loading.value = false
  }
}

// 单个生成编码
const handleSingleGenerateCode = async () => {
  if (!singleGenerateForm.value.product_name || !singleGenerateForm.value.batch_no) {
    ElMessage.warning('请填写产品名称和批次编号')
    return
  }
  
  loading.value = true
  try {
    await axios.post('http://localhost:8000/api/code/generate', {
      product_name: singleGenerateForm.value.product_name,
      batch_no: singleGenerateForm.value.batch_no
    })
    singleGenerateDialogVisible.value = false
    ElMessage.success('成功生成1个编码')
    singleGenerateForm.value = {
      product_name: '',
      batch_no: '',
      expire_date: null
    }
    loadData()
  } catch (error) {
    ElMessage.error('生成失败')
  } finally {
    loading.value = false
  }
}

// 批量删除
const handleBatchDelete = async () => {
  if (selectedRows.value.length === 0) return
  
  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedRows.value.length} 条编码吗？`,
      '批量删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    loading.value = true
    // 模拟API请求
    setTimeout(() => {
      ElMessage.success('批量删除成功')
      loading.value = false
      loadData()
    }, 1000)
  } catch {
    // 用户取消
  }
}

// 状态筛选
const handleStatusFilter = () => {
  currentPage.value = 1
  loadData()
}

// 导出Excel
const handleExportExcel = () => {
  download('http://localhost:8000/api/code/export/excel')
}

// 导出二维码ZIP
const handleExportQrCode = () => {
  download('http://localhost:8000/api/code/export/zip')
}

// 标准下载方法
const download = (url) => {
  const link = document.createElement('a')
  link.href = url
  link.click()
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.code-management {
  padding: 20px;
  height: 100%;
  overflow: auto;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.action-buttons {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.code-table {
  margin-bottom: 20px;
}

.pagination {
  text-align: right;
}

.code-detail {
  padding: 20px;
}

.detail-header {
  display: flex;
  margin-bottom: 30px;
  gap: 30px;
}

.qr-code {
  flex-shrink: 0;
}

.qr-code img {
  width: 150px;
  height: 150px;
}

.code-info {
  flex: 1;
}

.code-info h3 {
  margin-bottom: 20px;
  color: #1677FF;
}

.info-item {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.info-item .label {
  width: 80px;
  color: #666;
}

.info-item .value {
  flex: 1;
}

.detail-section {
  margin-bottom: 30px;
}

.detail-section h4 {
  margin-bottom: 15px;
  color: #333;
}

.signature-info {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
  overflow-x: auto;
}

.signature-info pre {
  margin: 0;
  font-family: monospace;
  font-size: 12px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>