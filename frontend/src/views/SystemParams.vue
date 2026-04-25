<template>
  <div class="system-params-container">
    <div class="page-header">
      <h2>系统参数</h2>
    </div>

    <el-card>
      <template #header>
        <span>基础配置</span>
      </template>
      <el-form :model="basicForm" label-width="150px">
        <el-form-item label="系统名称">
          <el-input v-model="basicForm.system_name" style="width: 300px" />
        </el-form-item>
        <el-form-item label="系统版本">
          <el-input v-model="basicForm.version" disabled style="width: 200px" />
        </el-form-item>
        <el-form-item label="系统描述">
          <el-input v-model="basicForm.description" type="textarea" rows="3" style="width: 400px" />
        </el-form-item>
      </el-form>
    </el-card>

    <el-card style="margin-top: 20px">
      <template #header>
        <span>API配置</span>
      </template>
      <el-form :model="apiForm" label-width="150px">
        <el-form-item label="API地址">
          <el-input v-model="apiForm.api_url" style="width: 400px" />
        </el-form-item>
        <el-form-item label="WebSocket地址">
          <el-input v-model="apiForm.ws_url" style="width: 400px" />
        </el-form-item>
        <el-form-item label="数据刷新间隔">
          <el-input-number v-model="apiForm.refresh_interval" :min="1" :max="60" />
          <span style="margin-left: 10px">秒</span>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card style="margin-top: 20px">
      <template #header>
        <span>二维码配置</span>
      </template>
      <el-form :model="qrcodeForm" label-width="150px">
        <el-form-item label="二维码URL前缀">
          <el-input v-model="qrcodeForm.qrcode_url_prefix" style="width: 400px" />
          <div class="form-tip">二维码中编码的URL前缀，用于扫码验证</div>
        </el-form-item>
        <el-form-item label="地图数据URL">
          <el-input v-model="qrcodeForm.map_url" style="width: 400px" />
          <div class="form-tip">用于大屏展示的地图数据来源</div>
        </el-form-item>
        <el-form-item label="默认二维码尺寸">
          <el-input-number v-model="qrcodeForm.default_qr_size" :min="100" :max="500" />
          <span style="margin-left: 10px">px</span>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card style="margin-top: 20px">
      <template #header>
        <span>日志配置</span>
      </template>
      <el-form :model="logForm" label-width="150px">
        <el-form-item label="日志保留天数">
          <el-input-number v-model="logForm.retention_days" :min="7" :max="365" />
          <span style="margin-left: 10px">天</span>
        </el-form-item>
        <el-form-item label="日志级别">
          <el-select v-model="logForm.log_level" style="width: 200px">
            <el-option label="DEBUG" value="debug" />
            <el-option label="INFO" value="info" />
            <el-option label="WARNING" value="warning" />
            <el-option label="ERROR" value="error" />
          </el-select>
        </el-form-item>
        <el-form-item label="操作日志">
          <el-switch v-model="logForm.enable_operation_log" />
        </el-form-item>
        <el-form-item label="访问日志">
          <el-switch v-model="logForm.enable_access_log" />
        </el-form-item>
      </el-form>
    </el-card>

    <div class="action-bar">
      <el-button type="primary" @click="handleSave" :loading="saving">保存配置</el-button>
      <el-button @click="handleReset">重置</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const saving = ref(false)

const basicForm = ref({
  system_name: '产品溯源管理系统',
  version: '1.0.0',
  description: '基于区块链技术的产品溯源防伪验证平台'
})

const apiForm = ref({
  api_url: 'http://localhost:8000/api',
  ws_url: 'ws://localhost:8000/ws/scan',
  refresh_interval: 5
})

const qrcodeForm = ref({
  qrcode_url_prefix: 'https://trace.example.com/verify/',
  map_url: 'https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json',
  default_qr_size: 300
})

const logForm = ref({
  retention_days: 30,
  log_level: 'info',
  enable_operation_log: true,
  enable_access_log: true
})

const handleSave = async () => {
  saving.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('配置保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

const handleReset = () => {
  ElMessage.info('已重置为默认配置')
}
</script>

<style scoped>
.system-params-container {
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

.form-tip {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
  line-height: 1.4;
}

.action-bar {
  margin-top: 20px;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}
</style>
