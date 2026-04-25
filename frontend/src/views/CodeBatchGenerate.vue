<template>
  <div class="code-batch-container">
    <div class="page-header">
      <h2>批量生成溯源码</h2>
    </div>

    <div class="batch-form">
      <el-card>
        <el-form :model="form" label-width="120px">
          <el-form-item label="产品名称">
            <el-input v-model="form.product_name" placeholder="请输入产品名称" />
          </el-form-item>
          <el-form-item label="批次编号">
            <el-input v-model="form.batch_no" placeholder="请输入批次编号" />
          </el-form-item>
          <el-form-item label="生成数量">
            <el-input-number v-model="form.count" :min="1" :max="10000" />
          </el-form-item>
          <el-form-item label="前缀标识">
            <el-input v-model="form.prefix" placeholder="如：PROD" style="width: 200px" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleBatchGenerate" :loading="loading">
              批量生成
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card v-if="batchResult" style="margin-top: 20px">
        <div class="result-section">
          <el-result icon="success" title="批量生成成功">
            <template #extra>
              <p>成功生成 <strong>{{ batchResult.count }}</strong> 个溯源码</p>
              <p>批次编号：{{ batchResult.batch_no }}</p>
              <div class="action-buttons">
                <el-button type="primary" @click="handleExportExcel">导出Excel</el-button>
                <el-button type="success" @click="handleExportZip">导出二维码ZIP</el-button>
                <el-button @click="handleViewList">查看列表</el-button>
              </div>
            </template>
          </el-result>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const form = ref({
  product_name: '',
  batch_no: '',
  count: 100,
  prefix: 'CODE'
})

const loading = ref(false)
const batchResult = ref(null)

const handleBatchGenerate = async () => {
  if (!form.value.product_name || !form.value.batch_no) {
    ElMessage.warning('请填写产品名称和批次编号')
    return
  }

  loading.value = true
  try {
    const response = await axios.post('http://localhost:8000/api/code/batch_generate', {
      product_name: form.value.product_name,
      batch_no: form.value.batch_no,
      count: form.value.count
    })
    batchResult.value = {
      count: form.value.count,
      batch_no: form.value.batch_no,
      product_name: form.value.product_name,
      create_time: new Date().toLocaleString()
    }
    ElMessage.success(`成功生成 ${form.value.count} 个溯源码`)
  } catch (error) {
    console.error('生成失败:', error)
    ElMessage.error('生成失败，请检查网络或后端服务')
  } finally {
    loading.value = false
  }
}

const handleExportExcel = async () => {
  if (!batchResult.value) {
    ElMessage.warning('请先生成溯源码')
    return
  }
  try {
    const batchNo = batchResult.value.batch_no
    window.open(`http://localhost:8000/api/code/export/excel?batch_no=${batchNo}`, '_blank')
    ElMessage.success('Excel导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

const handleExportZip = async () => {
  if (!batchResult.value) {
    ElMessage.warning('请先生成溯源码')
    return
  }
  try {
    const batchNo = batchResult.value.batch_no
    window.open(`http://localhost:8000/api/code/export/zip?batch_no=${batchNo}`, '_blank')
    ElMessage.success('ZIP导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

const handleViewList = () => {
  ElMessage.info('查看列表功能开发中')
}
</script>

<style scoped>
.code-batch-container {
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

.batch-form {
  max-width: 600px;
}

.result-section {
  text-align: center;
}

.action-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 10px;
}
</style>
