<template>
  <div class="task-center">
    <h1>任务中心</h1>
    
    <!-- 顶部统计区 -->
    <el-row :gutter="20" class="mb-4">
      <el-col :span="6">
        <el-card class="task-stats-card">
          <div class="card-content">
            <div class="card-title">进行中任务</div>
            <div class="card-value">{{ stats.running }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="task-stats-card">
          <div class="card-content">
            <div class="card-title">成功任务</div>
            <div class="card-value">{{ stats.success }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="task-stats-card">
          <div class="card-content">
            <div class="card-title">失败任务</div>
            <div class="card-value">{{ stats.failed }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="task-stats-card">
          <div class="card-content">
            <div class="card-title">总任务</div>
            <div class="card-value">{{ stats.total }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 主内容区 -->
    <el-row :gutter="20">
      <!-- 左侧：任务创建区 -->
      <el-col :span="6">
        <!-- 批量生成二维码 -->
        <el-card class="mb-4" title="批量生成二维码">
          <el-form :model="generateForm" label-width="80px">
            <el-form-item label="批次号">
              <el-input v-model="generateForm.batch_no" placeholder="请输入批次号" />
            </el-form-item>
            <el-form-item label="产品名称">
              <el-input v-model="generateForm.product_name" placeholder="请输入产品名称" />
            </el-form-item>
            <el-form-item label="数量">
              <el-input-number v-model="generateForm.count" :min="1" :max="10000" placeholder="请输入数量" />
            </el-form-item>
            <el-button type="primary" @click="createGenerateTask" :loading="loading.generate">
              创建生成任务
            </el-button>
          </el-form>
        </el-card>
        
        <!-- 导出任务 -->
        <el-card title="导出任务">
          <el-form :model="exportForm" label-width="80px">
            <el-form-item label="批次号">
              <el-input v-model="exportForm.batch_no" placeholder="请输入批次号" />
            </el-form-item>
            <el-button type="success" @click="createExportTask" :loading="loading.export">
              创建导出任务
            </el-button>
          </el-form>
        </el-card>
      </el-col>
      
      <!-- 右侧：任务列表区 -->
      <el-col :span="18">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>任务列表</span>
              <el-button type="primary" size="small" @click="fetchTaskList">
                刷新
              </el-button>
            </div>
          </template>
          <el-table :data="taskList" stripe style="width: 100%">
            <el-table-column prop="id" label="任务ID" width="80" />
            <el-table-column prop="task_type" label="类型" width="120">
              <template #default="{row}">
                <el-tag :type="row.task_type === 'generate' ? 'primary' : 'success'">
                  {{ row.task_type === 'generate' ? '生成' : '导出' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="batch_no" label="批次号" width="150" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{row}">
                <el-tag :type="getStatusType(row.status)">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="进度" width="200">
              <template #default="{row}">
                <el-progress :percentage="row.progress" :color="getProgressColor(row.status)" />
              </template>
            </el-table-column>
            <el-table-column label="结果" width="150">
              <template #default="{row}">
                <span>{{ row.success }}/{{ row.total }}</span>
              </template>
            </el-table-column>
            <el-table-column label="创建时间" width="180">
              <template #default="{row}">
                <span>{{ formatTime(row.created_at) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200">
              <template #default="{row}">
                <el-button size="small" @click="viewTask(row)">
                  查看
                </el-button>
                <el-button 
                  size="small" 
                  type="danger" 
                  v-if="row.status === 'failed'" 
                  @click="retryTask(row)"
                >
                  重试
                </el-button>
                <el-button 
                  size="small" 
                  type="success" 
                  v-if="row.status === 'success' && row.result_path" 
                  @click="download(row)"
                >
                  下载
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          
          <!-- 分页 -->
          <div class="pagination mt-4">
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
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '../utils/request'

// 表单数据
const generateForm = ref({
  batch_no: '',
  product_name: '',
  count: 100
})

const exportForm = ref({
  batch_no: ''
})

// 任务列表
const taskList = ref([])
const stats = ref({
  running: 0,
  success: 0,
  failed: 0,
  total: 0
})

// 分页
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 加载状态
const loading = ref({
  generate: false,
  export: false
})

// 定时器
let refreshTimer = null

// 获取任务列表
const fetchTaskList = async () => {
  try {
    const res = await request.get('/api/code/task/list', {
      params: {
        page: currentPage.value,
        page_size: pageSize.value
      }
    })
    taskList.value = res.data.items
    total.value = res.data.total
    
    // 更新统计数据
    stats.value = res.data.stats
  } catch (error) {
    ElMessage.error('获取任务列表失败')
  }
}

// 处理分页
const handleSizeChange = (size) => {
  pageSize.value = size
  fetchTaskList()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  fetchTaskList()
}

// 创建生成任务
const createGenerateTask = async () => {
  if (!generateForm.value.batch_no) {
    ElMessage.warning('请输入批次号')
    return
  }
  if (!generateForm.value.product_name) {
    ElMessage.warning('请输入产品名称')
    return
  }
  if (!generateForm.value.count || generateForm.value.count < 1) {
    ElMessage.warning('请输入有效的数量')
    return
  }
  
  loading.value.generate = true
  try {
    const res = await request.post('/api/code/batch_generate', {
      batch_no: generateForm.value.batch_no,
      product_name: generateForm.value.product_name,
      count: generateForm.value.count
    })
    ElMessage.success('任务创建成功')
    fetchTaskList()
  } catch (error) {
    ElMessage.error('任务创建失败')
  } finally {
    loading.value.generate = false
  }
}

// 创建导出任务
const createExportTask = async () => {
  if (!exportForm.value.batch_no) {
    ElMessage.warning('请输入批次号')
    return
  }
  
  loading.value.export = true
  try {
    const res = await request.post('/api/code/export/create', {
      batch_no: exportForm.value.batch_no
    })
    ElMessage.success('导出任务创建成功')
    fetchTaskList()
  } catch (error) {
    ElMessage.error('导出任务创建失败')
  } finally {
    loading.value.export = false
  }
}

// 查看任务详情
const viewTask = (row) => {
  ElMessage.info(`任务ID: ${row.id}\n状态: ${getStatusText(row.status)}\n进度: ${row.progress}%\n结果: ${row.success}/${row.total}`)
}

// 重试任务
const retryTask = (row) => {
  ElMessage.confirm('确定要重试此任务吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      const res = await request.post('/api/code/task/retry', {
        task_id: row.id
      })
      ElMessage.success('任务已重新提交')
      fetchTaskList()
    } catch (error) {
      ElMessage.error('重试失败')
    }
  })
}

// 下载文件
const download = (row) => {
  if (row.result_path) {
    window.open(`/api/code/download/${row.result_path}`, '_blank')
  }
}

// 获取状态类型
const getStatusType = (status) => {
  switch (status) {
    case 'running':
      return 'info'
    case 'success':
      return 'success'
    case 'failed':
      return 'danger'
    default:
      return 'warning'
  }
}

// 获取状态文本
const getStatusText = (status) => {
  switch (status) {
    case 'pending':
      return '等待中'
    case 'running':
      return '运行中'
    case 'success':
      return '成功'
    case 'failed':
      return '失败'
    case 'partial':
      return '部分成功'
    default:
      return status
  }
}

// 获取进度条颜色
const getProgressColor = (status) => {
  switch (status) {
    case 'running':
      return '#409EFF'
    case 'success':
      return '#67C23A'
    case 'failed':
      return '#F56C6C'
    default:
      return '#E6A23C'
  }
}

// 格式化时间
const formatTime = (time) => {
  if (!time) return ''
  return new Date(time).toLocaleString()
}

// 启动轮询
const startPolling = () => {
  refreshTimer = setInterval(() => {
    // 只在有运行中任务时刷新
    const hasRunningTask = taskList.value.some(task => task.status === 'running')
    if (hasRunningTask) {
      fetchTaskList()
    }
  }, 2000)
}

// 生命周期
onMounted(() => {
  fetchTaskList()
  startPolling()
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
</script>

<style scoped>
.task-center {
  padding: 20px;
}

.task-stats-card {
  height: 120px;
}

.card-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.card-title {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.card-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination {
  display: flex;
  justify-content: flex-end;
}

.mb-4 {
  margin-bottom: 20px;
}

.mt-4 {
  margin-top: 20px;
}
</style>