<template>
  <div class="login-container">
    <div class="left-panel">
      <div class="brand-content">
        <h1>睿码溯源系统</h1>
        <p class="platform">RuiTrace Platform</p>
        <p class="desc">工业级防伪溯源解决方案</p>
        <p class="tagline">让每一件产品都有唯一可信身份</p>
      </div>
    </div>
    <div class="right-panel">
      <div class="login-box">
        <div class="login-header">
          <h2>系统登录</h2>
        </div>
        <div class="login-form">
          <div class="form-group">
            <label for="username">用户名</label>
            <input 
              type="text" 
              id="username" 
              v-model="username" 
              placeholder="请输入用户名"
              @keyup.enter="handleLogin"
            />
          </div>
          <div class="form-group">
            <label for="password">密码</label>
            <input 
              type="password" 
              id="password" 
              v-model="password" 
              placeholder="请输入密码"
              @keyup.enter="handleLogin"
            />
          </div>
          <div v-if="error" class="error-message">
            {{ error }}
          </div>
          <button 
            class="login-button" 
            @click="handleLogin"
            :disabled="isLoading"
          >
            {{ isLoading ? '登录中...' : '登录' }}
          </button>
        </div>
        <div class="login-footer">
          <p>默认账号: admin</p>
          <p>默认密码: admin123</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const username = ref('')
const password = ref('')
const error = ref('')
const isLoading = ref(false)
const emit = defineEmits(['login-success'])

const handleLogin = async () => {
  if (!username.value || !password.value) {
    error.value = '请输入用户名和密码'
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    // 模拟登录请求
    // 实际项目中应该调用后端API
    await new Promise(resolve => setTimeout(resolve, 1000))

    if (username.value === 'admin' && password.value === 'admin123') {
      emit('login-success')
    } else {
      error.value = '用户名或密码错误'
    }
  } catch (err) {
    error.value = '登录失败，请重试'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.left-panel {
  flex: 1;
  background: linear-gradient(135deg, #1f4fff, #0f172a);
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 80px;
}

.brand-content {
  max-width: 500px;
}

.brand-content h1 {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 10px;
}

.platform {
  font-size: 18px;
  opacity: 0.9;
  margin-bottom: 30px;
}

.desc {
  font-size: 20px;
  margin-bottom: 10px;
  font-weight: 500;
}

.tagline {
  font-size: 14px;
  opacity: 0.8;
}

.right-panel {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f7fb;
}

.login-box {
  width: 360px;
  padding: 40px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  font-size: 24px;
  margin-bottom: 8px;
  color: #1f4fff;
}

.login-form {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #606266;
  font-size: 14px;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #1f4fff;
  box-shadow: 0 0 0 2px rgba(31, 79, 255, 0.2);
}

.error-message {
  background: rgba(255, 77, 79, 0.1);
  border: 1px solid rgba(255, 77, 79, 0.3);
  color: #ff4d4f;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 14px;
}

.login-button {
  width: 100%;
  padding: 14px;
  background: #1f4fff;
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-button:hover:not(:disabled) {
  background: #0f3fff;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(31, 79, 255, 0.4);
}

.login-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-footer {
  text-align: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;
}

.login-footer p {
  color: #909399;
  font-size: 12px;
  margin: 5px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-container {
    flex-direction: column;
  }
  
  .left-panel {
    flex: 0 0 30%;
    padding: 40px;
  }
  
  .right-panel {
    flex: 0 0 70%;
  }
  
  .brand-content h1 {
    font-size: 24px;
  }
  
  .platform {
    font-size: 14px;
  }
  
  .desc {
    font-size: 16px;
  }
  
  .tagline {
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .login-box {
    width: 90%;
    padding: 30px;
  }
}
</style>