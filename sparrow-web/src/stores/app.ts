import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const isSetupComplete = ref(false)
  const token = ref('')
  const user = ref<{ id: string; username: string; role: string } | null>(null)

  function setToken(newToken: string) {
    token.value = newToken
    localStorage.setItem('sparrow_token', newToken)
  }

  function loadToken() {
    token.value = localStorage.getItem('sparrow_token') || ''
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('sparrow_token')
  }

  return { isSetupComplete, token, user, setToken, loadToken, logout }
})
