<template>
  <div class="code-generate-container">
    <div class="page-header">
      <h2>单个溯源码生成</h2>
    </div>

    <div class="generate-form">
      <el-card>
        <el-form :model="form" label-width="120px">
          <el-form-item label="产品名称">
            <el-input v-model="form.product_name" placeholder="请输入产品名称" />
          </el-form-item>
          <el-form-item label="批次编号">
            <el-select v-model="form.batch_no" placeholder="请选择批次" style="width: 100%">
              <el-option label="BATCH20260401" value="BATCH20260401" />
              <el-option label="BATCH20260402" value="BATCH20260402" />
              <el-option label="BATCH20260403" value="BATCH20260403" />
            </el-select>
          </el-form-item>
          <el-form-item label="产品信息">
            <el-input v-model="form.product_info" type="textarea" rows="3" placeholder="请输入产品详细信息" />
          </el-form-item>
          <el-form-item label="生成数量">
            <el-input-number v-model="form.count" :min="1" :max="100" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleGenerate" :loading="loading">
              生成溯源码
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card v-if="generatedCode" style="margin-top: 20px">
        <div class="result-section">
          <h3>生成成功</h3>
          <div class="code-info">
            <p><strong>溯源码ID：</strong>{{ generatedCode.code_id }}</p>
            <p><strong>批次编号：</strong>{{ generatedCode.batch_no }}</p>
            <p><strong>产品名称：</strong>{{ generatedCode.product_name }}</p>
            <p><strong>生成时间：</strong>{{ generatedCode.create_time }}</p>
          </div>
          <div class="qrcode-section">
            <img :src="generatedCode.qrcode_url" alt="二维码" class="qrcode-img" />
          </div>
          <div class="action-buttons">
            <el-button type="primary" @click="handleDownload">下载二维码</el-button>
            <el-button @click="handleCopy">复制链接</el-button>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const form = ref({
  product_name: '',
  batch_no: '',
  product_info: '',
  count: 1
})

const loading = ref(false)
const generatedCode = ref(null)

const handleGenerate = async () => {
  if (!form.value.product_name || !form.value.batch_no) {
    ElMessage.warning('请填写产品名称和批次编号')
    return
  }

  loading.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    generatedCode.value = {
      code_id: `CODE${Date.now()}`,
      batch_no: form.value.batch_no,
      product_name: form.value.product_name,
      create_time: new Date().toLocaleString(),
      qrcode_url: `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent('https://trace.example.com/verify/' + Date.now())}`
    }
    ElMessage.success('生成成功')
  } catch (error) {
    ElMessage.error('生成失败')
  } finally {
    loading.value = false
  }
}

const handleDownload = () => {
  ElMessage.info('下载功能开发中')
}

const handleCopy = () => {
  ElMessage.info('复制功能开发中')
}
</script>

<style scoped>
.code-generate-container {
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

.generate-form {
  max-width: 600px;
}

.result-section h3 {
  margin: 0 0 15px 0;
  color: #67c23a;
}

.code-info {
  margin-bottom: 20px;
}

.code-info p {
  margin: 8px 0;
  font-size: 14px;
}

.qrcode-section {
  text-align: center;
  margin: 20px 0;
}

.qrcode-img {
  width: 200px;
  height: 200px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.action-buttons {
  text-align: center;
}
</style>
