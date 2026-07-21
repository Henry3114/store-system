<script setup lang="ts">
import { onMounted, ref } from 'vue'

const backendStatus = ref<string>('检测中...')

onMounted(async () => {
  try {
    const res = await fetch('/api/health')
    const data = await res.json()
    backendStatus.value = data.status === 'ok' ? '后端连接正常' : '后端异常'
  } catch {
    backendStatus.value = '后端未启动'
  }
})
</script>

<template>
  <div class="app-container">
    <h1>小卖部销售管理系统</h1>
    <p class="subtitle">Phase 0-A — 项目初始化完成</p>
    <el-card class="status-card">
      <p>后端状态：<el-tag :type="backendStatus === '后端连接正常' ? 'success' : 'danger'">{{ backendStatus }}</el-tag></p>
    </el-card>
  </div>
</template>

<style scoped>
.app-container {
  max-width: 600px;
  margin: 80px auto;
  text-align: center;
}
h1 {
  font-size: 28px;
  color: #303133;
  margin-bottom: 8px;
}
.subtitle {
  color: #909399;
  margin-bottom: 32px;
}
.status-card {
  text-align: left;
}
</style>
