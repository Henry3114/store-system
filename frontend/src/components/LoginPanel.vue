<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../api'

const emit = defineEmits(['login-success'])

const isRegister = ref(false)
const form = ref({ username: '', password: '', store_name: '' })

async function submit() {
  if (!form.value.username || !form.value.password) {
    ElMessage.warning('请填写用户名和密码')
    return
  }

  try {
    const url = isRegister.value ? '/api/auth/register' : '/api/auth/login'
    const body = isRegister.value ? form.value : { username: form.value.username, password: form.value.password }
    const res = await api.post(url, body)
    localStorage.setItem('token', res.data.token)
    localStorage.setItem('username', res.data.username)
    ElMessage.success(isRegister.value ? '注册成功！' : '登录成功！')
    emit('login-success')
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '操作失败')
  }
}
</script>

<template>
  <div class="login-wrapper">
    <div class="login-card">
      <h1 class="login-title">小卖部销售管理系统</h1>
      <p class="login-subtitle">{{ isRegister ? '创建新账号' : '登录' }}</p>

      <el-form label-position="top" @submit.prevent="submit">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="输入用户名" size="large" />
        </el-form-item>

        <el-form-item v-if="isRegister" label="店铺名称">
          <el-input v-model="form.store_name" placeholder="如：老王便利店" size="large" />
        </el-form-item>

        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="输入密码" size="large" show-password />
        </el-form-item>

        <el-button type="primary" size="large" class="login-btn" @click="submit">
          {{ isRegister ? '注册' : '登录' }}
        </el-button>
      </el-form>

      <p class="toggle-link" @click="isRegister = !isRegister">
        {{ isRegister ? '已有账号？点此登录' : '没有账号？点此注册' }}
      </p>
    </div>
  </div>
</template>

<style scoped>
.login-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.login-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  width: 380px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}
.login-title {
  text-align: center;
  color: #303133;
  margin: 0 0 8px;
  font-size: 22px;
}
.login-subtitle {
  text-align: center;
  color: #909399;
  margin-bottom: 24px;
}
.login-btn {
  width: 100%;
  margin-top: 8px;
}
.toggle-link {
  text-align: center;
  margin-top: 16px;
  color: #667eea;
  cursor: pointer;
  font-size: 14px;
}
.toggle-link:hover {
  text-decoration: underline;
}
</style>
