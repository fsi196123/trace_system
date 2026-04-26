<template>
  <div class="attack-container">
    <div class="panel-header">
      <span class="icon">🔗</span>
      <span>溯源传播链</span>
      <div class="legend">
        <span class="node high">异常节点</span>
        <span class="line"></span>
        <span class="node normal">正常节点</span>
      </div>
    </div>
    <div class="graph-container">
      <svg ref="svgRef" class="graph-svg"></svg>
      <div class="nodes">
        <div
          v-for="node in nodes"
          :key="node.id"
          class="node"
          :class="[node.type, { pulse: node.risk === 'HIGH' }]"
          :style="{ left: node.x + '%', top: node.y + '%' }"
        >
          {{ node.label }}
        </div>
      </div>
      <svg class="lines-svg" ref="linesRef">
        <line
          v-for="(line, index) in lines"
          :key="index"
          :x1="line.x1 + '%'"
          :y1="line.y1 + '%'"
          :x2="line.x2 + '%'"
          :y2="line.y2 + '%'"
          :class="line.type"
        />
      </svg>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const svgRef = ref()
const linesRef = ref()

const nodes = ref([
  { id: 1, label: '源头窝点A', type: 'high', risk: 'HIGH', x: 10, y: 50 },
  { id: 2, label: '批发商B', type: 'high', risk: 'HIGH', x: 30, y: 30 },
  { id: 3, label: '批发商C', type: 'medium', risk: 'MEDIUM', x: 30, y: 70 },
  { id: 4, label: '零售商D', type: 'normal', risk: 'LOW', x: 50, y: 20 },
  { id: 5, label: '零售商E', type: 'normal', risk: 'LOW', x: 50, y: 50 },
  { id: 6, label: '零售商F', type: 'normal', risk: 'LOW', x: 50, y: 80 },
  { id: 7, label: '消费者', type: 'normal', risk: 'LOW', x: 70, y: 50 },
  { id: 8, label: '监控点', type: 'alert', risk: 'HIGH', x: 85, y: 50 }
])

const lines = ref([
  { x1: 10, y1: 50, x2: 30, y2: 30, type: 'high' },
  { x1: 10, y1: 50, x2: 30, y2: 70, type: 'high' },
  { x1: 30, y1: 30, x2: 50, y2: 20, type: 'medium' },
  { x1: 30, y1: 30, x2: 50, y2: 50, type: 'medium' },
  { x1: 30, y1: 70, x2: 50, y2: 50, type: 'medium' },
  { x1: 30, y1: 70, x2: 50, y2: 80, type: 'medium' },
  { x1: 50, y1: 50, x2: 70, y2: 50, type: 'normal' },
  { x1: 70, y1: 50, x2: 85, y2: 50, type: 'alert' }
])

let timer = null

onMounted(() => {
  timer = setInterval(() => {
    nodes.value = nodes.value.map(node => {
      if (node.risk === 'HIGH') {
        return {
          ...node,
          x: node.x + (Math.random() - 0.5) * 2,
          y: node.y + (Math.random() - 0.5) * 2
        }
      }
      return node
    })

    lines.value = [
      { x1: nodes.value[0].x, y1: nodes.value[0].y, x2: nodes.value[1].x, y2: nodes.value[1].y, type: 'high' },
      { x1: nodes.value[0].x, y1: nodes.value[0].y, x2: nodes.value[2].x, y2: nodes.value[2].y, type: 'high' },
      { x1: nodes.value[1].x, y1: nodes.value[1].y, x2: nodes.value[3].x, y2: nodes.value[3].y, type: 'medium' },
      { x1: nodes.value[1].x, y1: nodes.value[1].y, x2: nodes.value[4].x, y2: nodes.value[4].y, type: 'medium' },
      { x1: nodes.value[2].x, y1: nodes.value[2].y, x2: nodes.value[4].x, y2: nodes.value[4].y, type: 'medium' },
      { x1: nodes.value[2].x, y1: nodes.value[2].y, x2: nodes.value[5].x, y2: nodes.value[5].y, type: 'medium' },
      { x1: nodes.value[4].x, y1: nodes.value[4].y, x2: nodes.value[6].x, y2: nodes.value[6].y, type: 'normal' },
      { x1: nodes.value[6].x, y1: nodes.value[6].y, x2: nodes.value[7].x, y2: nodes.value[7].y, type: 'alert' }
    ]
  }, 2000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.attack-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 12px;
  background: #111827;
  border-radius: 8px;
  border: 1px solid #1f2a44;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  font-size: 14px;
  font-weight: bold;
  color: #00ffcc;
}

.icon {
  font-size: 16px;
}

.legend {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: auto;
  font-size: 11px;
  color: #6b7a99;
  font-weight: normal;
}

.node.high { background: #ff4d4f; }
.node.medium { background: #faad14; color: #000; }
.node.normal { background: #1890ff; }
.node.alert { background: #722ed1; }

.line.high { stroke: #ff4d4f; }
.line.medium { stroke: #faad14; }
.line.normal { stroke: #1890ff; }
.line.alert { stroke: #722ed1; }

.graph-container {
  flex: 1;
  position: relative;
  background: linear-gradient(180deg, #0d1322 0%, #0a0e1a 100%);
  border-radius: 6px;
  overflow: hidden;
}

.graph-svg {
  position: absolute;
  width: 100%;
  height: 100%;
}

.lines-svg {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.lines-svg line {
  stroke-width: 2;
  stroke-dasharray: 5 3;
  animation: dash 1s linear infinite;
}

@keyframes dash {
  to { stroke-dashoffset: -8; }
}

.nodes {
  position: absolute;
  width: 100%;
  height: 100%;
}

.node {
  position: absolute;
  transform: translate(-50%, -50%);
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: bold;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.3s ease;
}

.node:hover {
  transform: translate(-50%, -50%) scale(1.1);
}

.node.pulse {
  animation: nodePulse 1.5s ease-in-out infinite;
}

@keyframes nodePulse {
  0%, 100% { box-shadow: 0 0 5px currentColor; }
  50% { box-shadow: 0 0 20px currentColor, 0 0 30px currentColor; }
}
</style>