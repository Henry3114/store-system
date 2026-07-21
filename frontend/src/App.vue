<script setup lang="ts">
import { ref } from 'vue'
import LoginPanel from './components/LoginPanel.vue'
import MainPanel from './components/MainPanel.vue'

const loggedIn = ref(!!localStorage.getItem('token'))

function onLoginSuccess() {
  loggedIn.value = true
}

function onLogout() {
  loggedIn.value = false
}
</script>

<template>
  <LoginPanel v-if="!loggedIn" @login-success="onLoginSuccess" />
  <MainPanel v-else @logout="onLogout" />
</template>
