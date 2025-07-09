<template>
  <div class="login-container">
    <div class="card">
      <h1>{{ $t('login.title') }}</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>{{ $t('login.username') }}</label>
          <input type="text" class="form-control" v-model="username" required>
        </div>
        <div class="form-group">
          <label>{{ $t('login.password') }}</label>
          <input type="password" class="form-control" v-model="password" required>
        </div>
        <button type="submit" class="btn">{{ $t('login.submit') }}</button>
      </form>
      <p v-if="error" class="error">{{ $t('login.error') }}</p>
      <div class="language-toggle">
        <button @click="changeLanguage('ar')" :class="{active: $i18n.locale === 'ar'}">العربية</button>
        <button @click="changeLanguage('en')" :class="{active: $i18n.locale === 'en'}">English</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

export default {
  setup() {
    const username = ref('')
    const password = ref('')
    const error = ref(false)
    const router = useRouter()
    const { locale } = useI18n()

    const handleLogin = async () => {
      try {
        // Replace with actual API call
        const response = await fetch('http://localhost:8000/token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Tenant-ID': 'demo-tenant' // Replace with actual tenant ID
          },
          body: JSON.stringify({
            username: username.value,
            password: password.value
          })
        })

        if (response.ok) {
          const data = await response.json()
          localStorage.setItem('access_token', data.access_token)
          router.push('/')
        } else {
          error.value = true
        }
      } catch (err) {
        error.value = true
      }
    }

    const changeLanguage = (lang) => {
      locale.value = lang
    }

    return {
      username,
      password,
      error,
      handleLogin,
      changeLanguage
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f0f3;
}

.card {
  width: 400px;
  padding: 30px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.error {
  color: red;
  margin-top: 15px;
}

.language-toggle {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.language-toggle button {
  flex: 1;
  padding: 8px;
  background: #f0f0f3;
  border: none;
  border-radius: 8px;
  box-shadow: 3px 3px 6px #d3d3d6, 
              -3px -3px 6px #ffffff;
  cursor: pointer;
}

.language-toggle button.active {
  box-shadow: inset 3px 3px 6px #d3d3d6, 
              inset -3px -3px 6px #ffffff;
}
</style>