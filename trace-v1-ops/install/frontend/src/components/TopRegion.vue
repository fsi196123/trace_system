<template>
  <div class="region-container">
    <div class="panel-header">
      <span class="icon">🏆</span>
      <span>区域排行</span>
    </div>
    <div class="rank-list">
      <div
        v-for="(item, index) in rankings"
        :key="item.region"
        class="rank-item"
      >
        <div class="rank-num" :class="{ top3: index < 3 }">{{ index + 1 }}</div>
        <div class="rank-info">
          <div class="region-name">{{ item.region }}</div>
          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: (item.count / maxCount * 100) + '%', background: getColor(index) }"
            ></div>
          </div>
        </div>
        <div class="rank-count">{{ item.count.toLocaleString() }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const rankings = ref([
  { region: '广东省', count: 15234 },
  { region: '浙江省', count: 12453 },
  { region: '江苏省', count: 10876 },
  { region: '北京市', count: 9823 },
  { region: '上海市', count: 8654 },
  { region: '四川省', count: 7234 },
  { region: '湖北省', count: 6543 },
  { region: '山东省', count: 5987 }
])

const maxCount = computed(() => Math.max(...rankings.value.map(r => r.count)))

const getColor = (index) => {
  const colors = ['#ff4d4f', '#faad14', '#52c41a', '#1890ff', '#722ed1', '#eb2f96', '#fa8c16', '#13c2c2']
  return colors[index % colors.length]
}

let updateTimer = null

onMounted(() => {
  updateTimer = setInterval(() => {
    rankings.value = rankings.value.map(item => ({
      ...item,
      count: item.count + Math.floor(Math.random() * 10)
    }))
  }, 3000)
})
</script>

<style scoped>
.region-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 12px;
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

.rank-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.rank-list::-webkit-scrollbar {
  width: 4px;
}

.rank-list::-webkit-scrollbar-track {
  background: #1f2a44;
}

.rank-list::-webkit-scrollbar-thumb {
  background: #2f4f6f;
  border-radius: 2px;
}

.rank-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.rank-num {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  background: #1f2a44;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  color: #6b7a99;
}

.rank-num.top3 {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.rank-num:nth-child(1).top3 {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.rank-num:nth-child(2).top3 {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.rank-info {
  flex: 1;
  min-width: 0;
}

.region-name {
  font-size: 12px;
  color: #d0d7e0;
  margin-bottom: 3px;
}

.progress-bar {
  height: 4px;
  background: #1f2a44;
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.5s ease;
}

.rank-count {
  font-size: 12px;
  font-weight: bold;
  color: #00ffcc;
  min-width: 50px;
  text-align: right;
}
</style>