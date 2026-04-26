<template>
  <router-view v-if="isLoggedIn" />
  <Login v-else @login-success="handleLoginSuccess" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Login from './views/Login.vue'

const router = useRouter()
const isLoggedIn = ref(false)

const handleLoginSuccess = () => {
  isLoggedIn.value = true
  localStorage.setItem('isLoggedIn', 'true')
  router.push('/')
}

onMounted(() => {
  const savedLogin = localStorage.getItem('isLoggedIn')
  if (savedLogin === 'true') {
    isLoggedIn.value = true
  }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Arial', 'Microsoft YaHei', sans-serif;
  background: #f5f5f5;
}

#app {
  width: 100%;
  height: 100vh;
}
</style>