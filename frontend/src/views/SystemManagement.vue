<template>
  <div class="system-management">
    <!-- 左侧菜单 -->
    <div class="sidebar">
      <el-menu
        :default-active="activeMenu"
        class="sidebar-menu"
        @select="handleMenuSelect"
      >
        <el-menu-item index="users">
          <template #title>
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </template>
        </el-menu-item>
        <el-menu-item index="roles">
          <template #title>
            <el-icon><Position /></el-icon>
            <span>角色权限</span>
          </template>
        </el-menu-item>
        <el-menu-item index="logs">
          <template #title>
            <el-icon><DataAnalysis /></el-icon>
            <span>操作日志</span>
          </template>
        </el-menu-item>
        <el-menu-item index="api">
          <template #title>
            <el-icon><Link /></el-icon>
            <span>API密钥管理</span>
          </template>
        </el-menu-item>
        <el-menu-item index="config">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>系统配置</span>
          </template>
        </el-menu-item>
      </el-menu>
    </div>

    <!-- 右侧内容 -->
    <div class="content">
      <!-- 用户管理 -->
      <div v-if="activeMenu === 'users'" class="page-content">
        <div class="page-header">
          <h3>用户管理</h3>
          <el-button type="primary" @click="handleCreateUser">
            <el-icon><Plus /></el-icon> 创建用户
          </el-button>
        </div>

        <div class="search-bar">
          <el-input
            v-model="userSearchQuery"
            placeholder="搜索用户名或邮箱"
            clearable
            style="width: 300px"
            @keyup.enter="handleUserSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <el-button type="primary" @click="handleUserSearch" style="margin-left: 10px">
            搜索
          </el-button>
        </div>

        <el-table
          v-loading="loading"
          :data="usersData"
          style="width: 100%"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="username" label="用户名" width="150" />
          <el-table-column prop="email" label="邮箱" width="200" />
          <el-table-column prop="role" label="角色" width="120">
            <template #default="scope">
              <el-tag :type="scope.row.role === 'admin' ? 'primary' : 'success'">
                {{ scope.row.role === 'admin' ? '管理员' : '普通用户' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.status === 'active' ? 'success' : 'info'">
                {{ scope.row.status === 'active' ? '活跃' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="180" />
          <el-table-column label="操作" width="150">
            <template #default="scope">
              <el-button size="small" @click="handleEditUser(scope.row)">
                编辑
              </el-button>
              <el-button
                size="small"
                type="danger"
                @click="handleDeleteUser(scope.row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 角色权限 -->
      <div v-if="activeMenu === 'roles'" class="page-content">
        <div class="page-header">
          <h3>角色权限管理</h3>
          <el-button type="primary" @click="handleCreateRole">
            <el-icon><Plus /></el-icon> 创建角色
          </el-button>
        </div>

        <el-table
          v-loading="loading"
          :data="rolesData"
          style="width: 100%"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="角色名称" width="150" />
          <el-table-column prop="description" label="描述" />
          <el-table-column prop="permissions" label="权限" width="200">
            <template #default="scope">
              <div class="permission-tags">
                <el-tag
                  v-for="perm in scope.row.permissions"
                  :key="perm"
                  size="small"
                  style="margin-right: 5px; margin-bottom: 5px"
                >
                  {{ perm }}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150">
            <template #default="scope">
              <el-button size="small" @click="handleEditRole(scope.row)">
                编辑
              </el-button>
              <el-button
                size="small"
                type="danger"
                @click="handleDeleteRole(scope.row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 操作日志 -->
      <div v-if="activeMenu === 'logs'" class="page-content">
        <div class="page-header">
          <h3>操作日志</h3>
        </div>

        <div class="search-bar">
          <el-input
            v-model="logSearchQuery"
            placeholder="搜索操作内容"
            clearable
            style="width: 300px"
            @keyup.enter="handleLogSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <el-date-picker
            v-model="logDateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 240px; margin-left: 10px"
          />
          <el-button type="primary" @click="handleLogSearch" style="margin-left: 10px">
            搜索
          </el-button>
        </div>

        <el-table
          v-loading="loading"
          :data="logsData"
          style="width: 100%"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="user" label="操作用户" width="150" />
          <el-table-column prop="action" label="操作内容" />
          <el-table-column prop="ip" label="IP地址" width="150" />
          <el-table-column prop="created_at" label="操作时间" width="180" />
        </el-table>
      </div>

      <!-- API密钥管理 -->
      <div v-if="activeMenu === 'api'" class="page-content">
        <div class="page-header">
          <h3>API密钥管理</h3>
          <el-button type="primary" @click="handleCreateApiKey">
            <el-icon><Plus /></el-icon> 生成密钥
          </el-button>
        </div>

        <el-table
          v-loading="loading"
          :data="apiKeysData"
          style="width: 100%"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="key" label="API密钥" width="300" />
          <el-table-column prop="description" label="描述" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.status === 'active' ? 'success' : 'info'">
                {{ scope.row.status === 'active' ? '活跃' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="180" />
          <el-table-column prop="expires_at" label="过期时间" width="180" />
          <el-table-column label="操作" width="150">
            <template #default="scope">
              <el-button size="small" @click="handleRegenerateKey(scope.row)">
                重新生成
              </el-button>
              <el-button
                size="small"
                type="danger"
                @click="handleDeleteApiKey(scope.row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 系统配置 -->
      <div v-if="activeMenu === 'config'" class="page-content">
        <div class="page-header">
          <h3>系统配置</h3>
        </div>

        <el-form :model="systemConfig" label-width="120px">
          <el-form-item label="系统名称">
            <el-input v-model="systemConfig.system_name" />
          </el-form-item>
          <el-form-item label="系统版本">
            <el-input v-model="systemConfig.version" disabled />
          </el-form-item>
          <el-form-item label="API地址">
            <el-input v-model="systemConfig.api_url" />
          </el-form-item>
          <el-form-item label="WebSocket地址">
            <el-input v-model="systemConfig.ws_url" />
          </el-form-item>
          <el-form-item label="数据刷新间隔">
            <el-input-number v-model="systemConfig.refresh_interval" :min="1" :max="60" />
            <span style="margin-left: 10px">秒</span>
          </el-form-item>
          <el-form-item label="地图数据URL">
            <el-input v-model="systemConfig.map_url" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSaveConfig">保存配置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Position, DataAnalysis, Link, Setting, Plus, Search } from '@element-plus/icons-vue'

// 菜单
const activeMenu = ref('users')

// 加载状态
const loading = ref(false)

// 用户管理
const userSearchQuery = ref('')
const usersData = ref([])

// 角色管理
const rolesData = ref([])

// 操作日志
const logSearchQuery = ref('')
const logDateRange = ref([])
const logsData = ref([])

// API密钥
const apiKeysData = ref([])

// 系统配置
const systemConfig = ref({
  system_name: '全国产品溯源管理平台',
  version: '1.0.0',
  api_url: 'http://localhost:8000/api',
  ws_url: 'ws://localhost:8000/ws/scan',
  refresh_interval: 5,
  map_url: 'https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json'
})

// 模拟数据
const mockUsers = [
  { id: 1, username: 'admin', email: 'admin@example.com', role: 'admin', status: 'active', created_at: '2026-04-01 10:00:00' },
  { id: 2, username: 'user1', email: 'user1@example.com', role: 'user', status: 'active', created_at: '2026-04-02 11:00:00' },
  { id: 3, username: 'user2', email: 'user2@example.com', role: 'user', status: 'inactive', created_at: '2026-04-03 12:00:00' }
]

const mockRoles = [
  { id: 1, name: '管理员', description: '系统管理员', permissions: ['user:manage', 'role:manage', 'log:view', 'api:manage', 'config:manage'] },
  { id: 2, name: '普通用户', description: '普通操作权限', permissions: ['log:view'] }
]

const mockLogs = Array.from({ length: 20 }, (_, index) => ({
  id: index + 1,
  user: ['admin', 'user1', 'user2'][Math.floor(Math.random() * 3)],
  action: ['登录系统', '创建用户', '编辑角色', '查看日志', '生成API密钥'][Math.floor(Math.random() * 5)],
  ip: `192.168.1.${Math.floor(Math.random() * 255)}`,
  created_at: new Date(Date.now() - Math.random() * 86400000 * 7).toLocaleString()
}))

const mockApiKeys = Array.from({ length: 5 }, (_, index) => ({
  id: index + 1,
  key: `sk_${Math.random().toString(36).substring(2, 15)}`,
  description: `API Key ${index + 1}`,
  status: index % 2 === 0 ? 'active' : 'inactive',
  created_at: new Date(Date.now() - Math.random() * 86400000 * 30).toLocaleString(),
  expires_at: new Date(Date.now() + Math.random() * 86400000 * 365).toLocaleString()
}))

// 菜单选择
const handleMenuSelect = (key) => {
  activeMenu.value = key
  loadData()
}

// 加载数据
const loadData = () => {
  loading.value = true
  // 模拟API请求
  setTimeout(() => {
    switch (activeMenu.value) {
      case 'users':
        usersData.value = mockUsers
        break
      case 'roles':
        rolesData.value = mockRoles
        break
      case 'logs':
        logsData.value = mockLogs
        break
      case 'api':
        apiKeysData.value = mockApiKeys
        break
    }
    loading.value = false
  }, 500)
}

// 用户管理
const handleCreateUser = () => {
  ElMessage.info('创建用户功能开发中')
}

const handleEditUser = (user) => {
  ElMessage.info('编辑用户功能开发中')
}

const handleDeleteUser = (user) => {
  ElMessage.info('删除用户功能开发中')
}

const handleUserSearch = () => {
  loadData()
}

// 角色管理
const handleCreateRole = () => {
  ElMessage.info('创建角色功能开发中')
}

const handleEditRole = (role) => {
  ElMessage.info('编辑角色功能开发中')
}

const handleDeleteRole = (role) => {
  ElMessage.info('删除角色功能开发中')
}

// 操作日志
const handleLogSearch = () => {
  loadData()
}

// API密钥管理
const handleCreateApiKey = () => {
  ElMessage.info('生成API密钥功能开发中')
}

const handleRegenerateKey = (key) => {
  ElMessage.info('重新生成API密钥功能开发中')
}

const handleDeleteApiKey = (key) => {
  ElMessage.info('删除API密钥功能开发中')
}

// 系统配置
const handleSaveConfig = () => {
  ElMessage.success('配置保存成功')
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.system-management {
  display: flex;
  height: 100%;
  overflow: hidden;
}

.sidebar {
  width: 200px;
  background: #f5f5f5;
  border-right: 1px solid #eaeaea;
}

.sidebar-menu {
  height: 100%;
  border-right: none;
}

.content {
  flex: 1;
  padding: 20px;
  overflow: auto;
}

.page-content {
  height: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h3 {
  color: #333;
  margin: 0;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.permission-tags {
  display: flex;
  flex-wrap: wrap;
}

.el-table {
  margin-bottom: 20px;
}
</style>