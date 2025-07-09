<template>
  <div class="dashboard">
    <h1>{{ $t('dashboard.title') }}</h1>
    <p>{{ $t('dashboard.welcome', { name: user.name }) }}</p>
    
    <div class="modules">
      <router-link to="/users" class="module-card card">
        <h2>المستخدمين</h2>
        <p>إدارة المستخدمين والصلاحيات</p>
      </router-link>
      
      <router-link to="/invoices" class="module-card card">
        <h2>الفواتير</h2>
        <p>إدارة الفواتير والمدفوعات</p>
      </router-link>
      
      <router-link to="/inventory" class="module-card card">
        <h2>المخزون</h2>
        <p>إدارة المخزون والمنتجات</p>
      </router-link>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

export default {
  setup() {
    const { t } = useI18n()
    const user = ref({
      name: 'محمد',
      role: 'مدير النظام'
    })

    return {
      user,
      t
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.modules {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.module-card {
  display: block;
  text-decoration: none;
  color: inherit;
  transition: transform 0.3s ease;
}

.module-card:hover {
  transform: translateY(-5px);
}
</style>