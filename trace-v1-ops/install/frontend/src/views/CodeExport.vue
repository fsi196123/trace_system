<template>
  <div class="code-export-container">
    <div class="page-header">
      <h2>导出中心</h2>
    </div>

    <div class="export-cards">
      <el-card class="export-card">
        <template #header>
          <div class="card-header">
            <el-icon size="24"><Document /></el-icon>
            <span>Excel导出</span>
          </div>
        </template>
        <div class="card-content">
          <p>将溯源码数据导出为Excel格式，方便统计和存档</p>
          <el-form :model="excelForm" label-width="100px">
            <el-form-item label="批次筛选">
              <el-select v-model="excelForm.batch_no" placeholder="全部批次" style="width: 100%">
                <el-option label="全部批次" value="" />
                <el-option label="BATCH20260401" value="BATCH20260401" />
                <el-option label="BATCH20260402" value="BATCH20260402" />
              </el-select>
            </el-form-item>
            <el-form-item label="日期范围">
              <el-date-picker
                v-model="excelForm.dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                style="width: 100%"
              />
            </el-form-item>
            <el-form-item label="状态筛选">
              <el-checkbox-group v-model="excelForm.status">
                <el-checkbox label="active">正常</el-checkbox>
                <el-checkbox label="warning">预警</el-checkbox>
                <el-checkbox label="danger">异常</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </el-form>
          <el-button type="primary" @click="handleExportExcel" :loading="excelLoading">
            导出Excel
          </el-button>
        </div>
      </el-card>

      <el-card class="export-card">
        <template #header>
          <div class="card-header">
            <el-icon size="24"><Picture /></el-icon>
            <span>二维码ZIP导出</span>
          </div>
        </template>
        <div class="card-content">
          <p>将溯源码对应的二维码图片打包为ZIP文件</p>
          <el-form :model="zipForm" label-width="100px">
            <el-form-item label="批次筛选">
              <el-select v-model="zipForm.batch_no" placeholder="全部批次" style="width: 100%">
                <el-option label="全部批次" value="" />
                <el-option label="BATCH20260401" value="BATCH20260401" />
                <el-option label="BATCH20260402" value="BATCH20260402" />
              </el-select>
            </el-form-item>
            <el-form-item label="二维码尺寸">
              <el-radio-group v-model="zipForm.size">
                <el-radio label="200">200x200</el-radio>
                <el-radio label="300">300x300</el-radio>
                <el-radio label="500">500x500</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="图片格式">
              <el-radio-group v-model="zipForm.format">
                <el-radio label="png">PNG</el-radio>
                <el-radio label="jpg">JPG</el-radio>
                <el-radio label="svg">SVG</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-form>
          <el-button type="success" @click="handleExportZip" :loading="zipLoading">
            导出二维码ZIP
          </el-button>
        </div>
      </el-card>
    </div>

    <el-card style="margin-top: 20px">
      <template #header>
        <span>最近导出记录</span>
      </template>
      <el-table :data="exportHistory" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="type" label="导出类型" width="120">
          <template #default="scope">
            <el-tag :type="scope.row.type === 'excel' ? 'primary' : 'success'">
              {{ scope.row.type === 'excel' ? 'Excel' : '二维码ZIP' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="batch_no" label="批次编号" />
        <el-table-column prop="count" label="数量" width="100" />
        <el-table-column prop="create_time" label="导出时间" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'success' ? 'success' : 'info'">
              {{ scope.row.status === 'success' ? '成功' : '处理中' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button size="small" type="primary" link>下载</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Document, Picture } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const excelForm = ref({
  batch_no: '',
  dateRange: [],
  status: ['active']
})

const zipForm = ref({
  batch_no: '',
  size: '300',
  format: 'png'
})

const excelLoading = ref(false)
const zipLoading = ref(false)

const exportHistory = ref([
  { id: 1, type: 'excel', batch_no: 'BATCH20260401', count: 500, create_time: '2026-04-19 10:30:00', status: 'success' },
  { id: 2, type: 'zip', batch_no: 'BATCH20260401', count: 500, create_time: '2026-04-19 10:25:00', status: 'success' },
  { id: 3, type: 'excel', batch_no: 'BATCH20260402', count: 1000, create_time: '2026-04-18 15:20:00', status: 'success' }
])

const handleExportExcel = async () => {
  excelLoading.value = true
  try {
    const batchNo = excelForm.value.batch_no
    window.open(`http://localhost:8000/api/code/export/excel?batch_no=${batchNo}`, '_blank')
    ElMessage.success('Excel导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  } finally {
    excelLoading.value = false
  }
}

const handleExportZip = async () => {
  zipLoading.value = true
  try {
    const batchNo = zipForm.value.batch_no
    window.open(`http://localhost:8000/api/code/export/zip?batch_no=${batchNo}`, '_blank')
    ElMessage.success('二维码ZIP导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  } finally {
    zipLoading.value = false
  }
}
</script>

<style scoped>
.code-export-container {
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

.export-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.export-card .card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: bold;
}

.export-card .card-content p {
  color: #666;
  margin-bottom: 15px;
  font-size: 14px;
}
</style>
