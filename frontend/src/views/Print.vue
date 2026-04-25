<template>
  <div class="print-page">
    <div class="print-header">
      <h2>批次 {{ batchNo }} 二维码打印</h2>
      <div class="print-actions">
        <el-button @click="handlePrint">打印</el-button>
        <el-button @click="handleBack">返回</el-button>
      </div>
    </div>

    <div class="print-info">
      <p>产品：{{ batchInfo.product_name }}</p>
      <p>批次：{{ batchNo }}</p>
      <p>数量：{{ codesList.length }} 个</p>
    </div>

    <div class="page">
      <div v-for="code in codesList" :key="code.code_id" class="item">
        <div class="logo">
          <div class="logo-text">产品溯源</div>
        </div>
        <div class="qr-code">
          <img :src="code.qr_code_url" alt="QR Code" />
        </div>
        <div class="qr-info">
          <div class="code-text">{{ code.code_id }}</div>
          <div class="batch-text">{{ code.batch_no }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const batchNo = ref('')
const batchInfo = ref({ product_name: '' })
const codesList = ref([])

const handlePrint = () => {
  window.print()
}

const handleBack = () => {
  router.back()
}

onMounted(async () => {
  batchNo.value = route.query.batch_no || 'BATCH20260419001'
  
  // 模拟API请求获取批次数据
  await new Promise(resolve => setTimeout(resolve, 500))
  
  batchInfo.value = {
    product_name: '测试产品'
  }
  
  // 模拟生成30个二维码
  codesList.value = Array.from({ length: 30 }, (_, index) => ({
    code_id: `CODE${batchNo.value}${String(index + 1).padStart(4, '0')}`,
    product_name: batchInfo.value.product_name,
    batch_no: batchNo.value,
    qr_code_url: `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${encodeURIComponent('CODE' + index)}`
  }))
})
</script>

<style scoped>
.print-page {
  padding: 20px;
  background: #fff;
  min-height: 100vh;
}

.print-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 2px solid #333;
  margin-bottom: 20px;
}

.print-header h2 {
  margin: 0;
  color: #333;
}

.print-actions {
  display: flex;
  gap: 10px;
}

.print-info {
  background: #f5f5f5;
  padding: 15px;
  margin-bottom: 20px;
  border-radius: 8px;
}

.print-info p {
  margin: 5px 0;
  color: #333;
}

.page {
  width: 210mm;
  min-height: 297mm;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 6mm;
  padding: 10mm;
  border: 1px solid #ddd;
  margin: 0 auto;
}

.item {
  border: 1px solid #eee;
  text-align: center;
  padding: 4mm;
  page-break-inside: avoid;
}

.logo {
  margin-bottom: 2mm;
}

.logo-text {
  font-size: 10px;
  font-weight: bold;
  color: #333;
}

.qr-code {
  margin-bottom: 3mm;
}

.qr-code img {
  width: 50mm;
  height: 50mm;
}

.qr-info {
  font-size: 9px;
  color: #333;
}

.code-text {
  font-weight: bold;
  word-break: break-all;
  margin-bottom: 2mm;
}

.batch-text {
  color: #666;
  font-size: 8px;
}

@media print {
  @page {
    size: A4;
    margin: 0;
  }
  
  body {
    margin: 0;
    padding: 0;
  }
  
  .print-header {
    display: none;
  }
  
  .print-info {
    display: none;
  }
  
  .print-page {
    padding: 0;
  }
  
  .page {
    border: none;
    width: 100%;
    height: 100%;
  }
  
  .item {
    border: 1px solid #000;
  }
}
</style>