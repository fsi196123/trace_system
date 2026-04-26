import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('../components/Layout/index.vue'),
    children: [
      {
        path: '',
        name: 'dashboard',
        component: () => import('../views/Dashboard.vue')
      },
      {
        path: 'task',
        name: 'task',
        component: () => import('../views/TaskCenter.vue')
      },
      {
        path: 'batch',
        name: 'batch',
        component: () => import('../views/BatchManagement.vue')
      },
      {
        path: 'code/generate',
        name: 'code-generate',
        component: () => import('../views/CodeGenerate.vue')
      },
      {
        path: 'code/batch',
        name: 'code-batch',
        component: () => import('../views/CodeBatchGenerate.vue')
      },
      {
        path: 'code/export',
        name: 'code-export',
        component: () => import('../views/CodeExport.vue')
      },
      {
        path: 'scan/logs',
        name: 'scan-logs',
        component: () => import('../views/ScanLogs.vue')
      },
      {
        path: 'scan/ip',
        name: 'scan-ip',
        component: () => import('../views/ScanIPAnalysis.vue')
      },
      {
        path: 'scan/trace',
        name: 'scan-trace',
        component: () => import('../views/ScanTrace.vue')
      },
      {
        path: 'verify/records',
        name: 'verify-records',
        component: () => import('../views/VerifyRecords.vue')
      },
      {
        path: 'verify/risk',
        name: 'verify-risk',
        component: () => import('../views/RiskWarning.vue')
      },
      {
        path: 'system/rules',
        name: 'system-rules',
        component: () => import('../views/SystemRules.vue')
      },
      {
        path: 'system/keys',
        name: 'system-keys',
        component: () => import('../views/SystemKeys.vue')
      },
      {
        path: 'system/params',
        name: 'system-params',
        component: () => import('../views/SystemParams.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
