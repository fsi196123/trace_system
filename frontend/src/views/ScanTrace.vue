<template>
  <div class="scan-trace-container">
    <div class="page-header">
      <h2>单码追踪</h2>
    </div>

    <div class="search-section">
      <el-card>
        <el-form :model="searchForm" inline>
          <el-form-item label="溯源码ID">
            <el-input v-model="searchForm.code_id" placeholder="请输入溯源码ID" style="width: 250px" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch" :loading="loading">
              <el-icon><Search /></el-icon> 查询
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>

    <div v-if="codeInfo" class="code-info-section">
      <el-card>
        <template #header>
          <span>溯源码信息</span>
        </template>
        <el-descriptions :column="3" border>
          <el-descriptions-item label="溯源码ID">{{ codeInfo.code_id }}</el-descriptions-item>
          <el-descriptions-item label="产品名称">{{ codeInfo.product_name }}</el-descriptions-item>
          <el-descriptions-item label="批次编号">{{ codeInfo.batch_no }}</el-descriptions-item>
          <el-descriptions-item label="生产日期">{{ codeInfo.production_date }}</el-descriptions-item>
          <el-descriptions-item label="当前状态">
            <el-tag :type="getStatusType(codeInfo.status)">
              {{ getStatusText(codeInfo.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="扫码次数">{{ codeInfo.scan_count }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <el-card style="margin-top: 20px">
        <template #header>
          <span>扫码轨迹</span>
        </template>
        <el-timeline>
          <el-timeline-item
            v-for="(item, index) in traceData"
            :key="index"
            :timestamp="item.scan_time"
            :type="getTraceType(item.status)"
            :hollow="item.status === 'normal'"
          >
            <div class="trace-content">
              <div class="trace-header">
                <span class="location">{{ item.location }}</span>
                <el-tag size="small" :type="getStatusType(item.status)">
                  {{ getStatusText(item.status) }}
                </el-tag>
              </div>
              <div class="trace-detail">
                <p>IP地址：{{ item.ip }}</p>
                <p>设备：{{ item.device }}</p>
                <p>扫码结果：{{ item.result }}</p>
              </div>
            </div>
          </el-timeline-item>
        </el-timeline>
      </el-card>
    </div>

    <el-empty v-else-if="!loading" description="请输入溯源码ID进行查询" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const searchForm = ref({
  code_id: ''
})

const loading = ref(false)
const codeInfo = ref(null)
const traceData = ref([])

const handleSearch = async () => {
  if (!searchForm.value.code_id) {
    ElMessage.warning('请输入溯源码ID')
    return
  }

  loading.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    codeInfo.value = {
      code_id: searchForm.value.code_id,
      product_name: '智能测试产品',
      batch_no: 'BATCH20260401',
      production_date: '2026-04-01',
      status: 'warning',
      scan_count: 5
    }
    traceData.value = [
      { scan_time: '2026-04-01 10:00:00', location: '北京市海淀区', ip: '192.168.1.101', device: 'iPhone 15', status: 'normal', result: '首次验证成功' },
      { scan_time: '2026-04-05 14:30:00', location: '上海市浦东新区', ip: '192.168.1.102', device: 'HUAWEI Mate 60', status: 'warning', result: '异地提示' },
      { scan_time: '2026-04-10 09:15:00', location: '广州市天河区', ip: '192.168.1.103', device: '小米 14', status: 'warning', result: '频繁验证' },
      { scan_time: '2026-04-15 16:45:00', location: '深圳市南山区', ip: '192.168.1.104', device: 'OPPO Find X7', status: 'danger', result: '异常验证' },
      { scan_time: '2026-04-19 20:00:00', location: '杭州市西湖区', ip: '192.168.1.105', device: 'vivo X100', status: 'danger', result: '风险拦截' }
    ]
    ElMessage.success('查询成功')
  } catch (error) {
    ElMessage.error('查询失败')
  } finally {
    loading.value = false
  }
}

const getStatusType = (status) => {
  const map = { normal: 'success', warning: 'warning', danger: 'danger' }
  return map[status] || 'info'
}

const getStatusText = (status) => {
  const map = { normal: '正常', warning: '预警', danger: '异常' }
  return map[status] || '未知'
}

const getTraceType = (status) => {
  const map = { normal: 'success', warning: 'warning', danger: 'danger' }
  return map[status] || 'primary'
}
</script>

<style scoped>
.scan-trace-container {
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

.search-section {
  margin-bottom: 20px;
}

.trace-content {
  padding: 5px 0;
}

.trace-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.trace-header .location {
  font-weight: bold;
  font-size: 14px;
}

.trace-detail p {
  margin: 4px 0;
  font-size: 13px;
  color: #666;
}
</style>
