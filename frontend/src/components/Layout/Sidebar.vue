<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <h3>产品溯源管理</h3>
    </div>
    <el-menu
      router
      default-active="/"
      class="sidebar-menu"
      :unique-opened="true"
    >
      <el-menu-item index="/">
        <el-icon><DataAnalysis /></el-icon>
        <span>概览大屏</span>
      </el-menu-item>

      <el-menu-item index="/task">
        <el-icon><Timer /></el-icon>
        <span>任务中心</span>
      </el-menu-item>

      <el-sub-menu index="/code">
        <template #title>
          <el-icon><Key /></el-icon>
          <span>溯源码管理</span>
        </template>
        <el-menu-item index="/batch">
          <el-icon><Collection /></el-icon>
          <span>批次管理</span>
        </el-menu-item>
        <el-menu-item index="/code/generate">
          <el-icon><Document /></el-icon>
          <span>单个生成</span>
        </el-menu-item>
        <el-menu-item index="/code/batch">
          <el-icon><Tickets /></el-icon>
          <span>批量生成</span>
        </el-menu-item>
        <el-menu-item index="/code/export">
          <el-icon><Download /></el-icon>
          <span>导出中心</span>
        </el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="/scan">
        <template #title>
          <el-icon><View /></el-icon>
          <span>扫码记录</span>
        </template>
        <el-menu-item index="/scan/logs">
          <el-icon><Document /></el-icon>
          <span>扫码日志</span>
        </el-menu-item>
        <el-menu-item index="/scan/ip">
          <el-icon><Connection /></el-icon>
          <span>IP分析</span>
        </el-menu-item>
        <el-menu-item index="/scan/trace">
          <el-icon><Guide /></el-icon>
          <span>单码追踪</span>
        </el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="/verify">
        <template #title>
          <el-icon><Check /></el-icon>
          <span>防伪验证</span>
        </template>
        <el-menu-item index="/verify/records">
          <el-icon><Document /></el-icon>
          <span>验证记录</span>
        </el-menu-item>
        <el-menu-item index="/verify/risk">
          <el-icon><Warning /></el-icon>
          <span>风险预警</span>
        </el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="/system">
        <template #title>
          <el-icon><Setting /></el-icon>
          <span>系统配置</span>
        </template>
        <el-menu-item index="/system/rules">
          <el-icon><Setting /></el-icon>
          <span>防伪规则</span>
        </el-menu-item>
        <el-menu-item index="/system/keys">
          <el-icon><Key /></el-icon>
          <span>签名配置</span>
        </el-menu-item>
        <el-menu-item index="/system/params">
          <el-icon><Cpu /></el-icon>
          <span>系统参数</span>
        </el-menu-item>
      </el-sub-menu>
    </el-menu>
  </div>
</template>

<script setup>
import {
  DataAnalysis,
  Key,
  Collection,
  Document,
  Tickets,
  Download,
  View,
  Connection,
  Guide,
  Check,
  Warning,
  Setting,
  Cpu,
  Timer

} from '@element-plus/icons-vue'
</script>

<style scoped>
.sidebar {
  width: 220px;
  background: #fff;
  border-right: 1px solid #eaeaea;
  height: 100vh;
  overflow-y: auto;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #eaeaea;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 16px;
  color: #1677FF;
  font-weight: bold;
}

.sidebar-menu {
  border-right: none;
}

.sidebar-menu .el-menu-item,
.sidebar-menu :deep(.el-sub-menu__title) {
  height: 50px;
  line-height: 50px;
  font-size: 14px;
}

.sidebar-menu :deep(.el-sub-menu__title) {
  display: flex;
  align-items: center;
}

.sidebar-menu :deep(.el-sub-menu__title) span {
  flex: 1;
}

.sidebar-menu :deep(.el-menu--inline) {
  background: #fafafa;
}

.sidebar-menu :deep(.el-menu--inline) .el-menu-item {
  height: 45px;
  line-height: 45px;
  padding-left: 52px !important;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background: #e6f7ff;
  color: #1677FF;
}
</style>
