<template>
  <div class="system-keys-container">
    <div class="page-header">
      <h2>签名配置</h2>
    </div>

    <el-card>
      <template #header>
        <div class="card-header">
          <span>API密钥管理</span>
          <el-button type="primary" @click="handleCreateKey">
            <el-icon><Plus /></el-icon> 生成新密钥
          </el-button>
        </div>
      </template>
      <el-table :data="keysData" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="key_name" label="密钥名称" />
        <el-table-column prop="api_key" label="API Key" width="350">
          <template #default="scope">
            <code class="api-key">{{ scope.row.api_key }}</code>
          </template>
        </el-table-column>
        <el-table-column prop="secret_key" label="Secret Key" width="350">
          <template #default="scope">
            <code class="api-key">{{ scope.row.secret_key }}</code>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'active' ? 'success' : 'info'">
              {{ scope.row.status === 'active' ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="180" />
        <el-table-column label="操作" width="180">
          <template #default="scope">
            <el-button size="small" type="primary" link @click="handleCopy(scope.row)">
              复制
            </el-button>
            <el-button size="small" type="danger" link @click="handleDelete(scope.row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-card style="margin-top: 20px">
      <template #header>
        <span>签名算法说明</span>
      </template>
      <div class="signature-info">
        <h4>当前签名算法：HMAC-SHA256</h4>
        <p>签名用于验证请求的合法性和完整性，防止请求被篡改。</p>
        <el-steps :active="3" align-center>
          <el-step title="构造签名串" description="将请求参数按字典序排序并拼接" />
          <el-step title="计算签名" description="使用Secret Key和HMAC-SHA256算法计算签名" />
          <el-step title="发送请求" description="将签名附加到请求头中发送" />
        </el-steps>
        <div class="signature-example">
          <h4>签名示例</h4>
          <pre>签名 = HMAC-SHA256(SecretKey, "app_id=xxx&timestamp=xxx&...")</pre>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)

const keysData = ref([
  {
    id: 1,
    key_name: '生产环境密钥',
    api_key: 'ak_live_a8f5f167f44f4965e6b4e7f3f3e3e3e3',
    secret_key: 'sk_live_8f5f167f44f4965e6b4e7f3f3e3e3e3',
    status: 'active',
    create_time: '2026-04-01 10:00:00'
  },
  {
    id: 2,
    key_name: '测试环境密钥',
    api_key: 'ak_test_a8f5f167f44f4965e6b4e7f3f3e3e3e3',
    secret_key: 'sk_test_8f5f167f44f4965e6b4e7f3f3e3e3e3',
    status: 'active',
    create_time: '2026-04-01 10:00:00'
  }
])

const handleCreateKey = async () => {
  ElMessage.info('生成新密钥功能开发中')
}

const handleCopy = (row) => {
  ElMessage.success('密钥已复制到剪贴板')
}

const handleDelete = async (row) => {
  await ElMessageBox.confirm('确定要删除这个密钥吗？此操作不可撤销。', '删除确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
  ElMessage.success('删除成功')
}

onMounted(() => {
  loading.value = false
})
</script>

<style scoped>
.system-keys-container {
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.api-key {
  background: #f5f7fa;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-family: monospace;
}

.signature-info h4 {
  margin: 0 0 10px 0;
  color: #333;
}

.signature-info p {
  color: #666;
  margin-bottom: 20px;
}

.signature-example {
  margin-top: 20px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
}

.signature-example h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
}

.signature-example pre {
  background: #fff;
  padding: 10px;
  border-radius: 4px;
  font-size: 12px;
  font-family: monospace;
  overflow-x: auto;
}
</style>
