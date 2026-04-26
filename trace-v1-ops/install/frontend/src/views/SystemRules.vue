<template>
  <div class="system-rules-container">
    <div class="page-header">
      <h2>防伪规则配置</h2>
    </div>

    <el-card>
      <template #header>
        <span>防伪验证规则</span>
      </template>
      <el-form :model="rulesForm" label-width="150px">
        <el-form-item label="首扫规则">
          <el-radio-group v-model="rulesForm.first_scan">
            <el-radio label="allow">允许首次验证</el-radio>
            <el-radio label="warning">首次验证预警</el-radio>
            <el-radio label="block">首次验证拦截</el-radio>
          </el-radio-group>
          <div class="form-tip">控制溯源码首次被扫描验证时的行为</div>
        </el-form-item>

        <el-form-item label="多次扫码阈值">
          <el-input-number v-model="rulesForm.multi_scan_threshold" :min="1" :max="100" />
          <span style="margin-left: 10px">次</span>
          <div class="form-tip">同一个溯源码在多长时间内超过此次数将触发预警</div>
        </el-form-item>

        <el-form-item label="扫码时间窗口">
          <el-input-number v-model="rulesForm.scan_window" :min="1" :max="168" />
          <span style="margin-left: 10px">小时</span>
          <div class="form-tip">用于计算多次扫码阈值的时间窗口</div>
        </el-form-item>

        <el-form-item label="异地验证预警">
          <el-switch v-model="rulesForm异地验证预警" />
          <div class="form-tip">当溯源码在距离首次验证地点较远的位置被验证时触发预警</div>
        </el-form-item>

        <el-form-item label="异地距离阈值">
          <el-input-number v-model="rulesForm.distance_threshold" :min="50" :max="1000" />
          <span style="margin-left: 10px">公里</span>
          <div class="form-tip">触发异地验证预警的距离阈值</div>
        </el-form-item>

        <el-form-item label="异常设备检测">
          <el-switch v-model="rulesForm.device_check" />
          <div class="form-tip">检测验证请求是否来自异常或可疑设备</div>
        </el-form-item>

        <el-form-item label="IP黑名单检测">
          <el-switch v-model="rulesForm.ip_blacklist_check" />
          <div class="form-tip">自动拒绝来自黑名单IP的验证请求</div>
        </el-form-item>

        <el-form-item label="风险评分阈值">
          <el-input-number v-model="rulesForm.risk_score_threshold" :min="50" :max="100" />
          <div class="form-tip">超过此分数的验证请求将被标记为高风险</div>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSave" :loading="saving">保存配置</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const saving = ref(false)

const rulesForm = ref({
  first_scan: 'allow',
  multi_scan_threshold: 5,
  scan_window: 24,
  异地验证预警: true,
  distance_threshold: 200,
  device_check: true,
  ip_blacklist_check: true,
  risk_score_threshold: 70
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
  rulesForm.value = {
    first_scan: 'allow',
    multi_scan_threshold: 5,
    scan_window: 24,
    异地验证预警: true,
    distance_threshold: 200,
    device_check: true,
    ip_blacklist_check: true,
    risk_score_threshold: 70
  }
  ElMessage.info('已重置')
}
</script>

<style scoped>
.system-rules-container {
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
</style>
