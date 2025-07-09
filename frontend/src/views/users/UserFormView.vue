<template>
  <div class="container">
    <h1>{{ isEditMode ? $t('users.editUser') : $t('users.createUser') }}</h1>
    
    <form @submit.prevent="submitForm" class="neumorphic-form">
      <div class="form-group">
        <label>{{ $t('users.username') }}</label>
        <input 
          v-model="userData.username" 
          type="text" 
          class="neumorphic-input"
          required
        >
      </div>

      <div class="form-group">
        <label>{{ $t('users.email') }}</label>
        <input 
          v-model="userData.email" 
          type="email" 
          class="neumorphic-input"
          required
        >
      </div>

      <div class="form-group">
        <label>{{ $t('users.role') }}</label>
        <select v-model="userData.role" class="neumorphic-input">
          <option value="admin">{{ $t('roles.admin') }}</option>
          <option value="manager">{{ $t('roles.manager') }}</option>
          <option value="employee">{{ $t('roles.employee') }}</option>
        </select>
      </div>

      <div class="form-group">
        <label>{{ $t('users.password') }}</label>
        <input 
          v-model="userData.password" 
          type="password" 
          class="neumorphic-input"
          :required="!isEditMode"
        >
        <p v-if="isEditMode" class="hint">{{ $t('users.passwordHint') }}</p>
      </div>

      <div class="form-actions">
        <button type="submit" class="neumorphic-btn primary">
          {{ $t('common.save') }}
        </button>
        <router-link to="/users" class="neumorphic-btn">
          {{ $t('common.cancel') }}
        </router-link>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import userService from '@/services/userService';

export default {
  setup() {
    const { t } = useI18n();
    const route = useRoute();
    const router = useRouter();
    
    const userId = route.params.id;
    const isEditMode = !!userId;
    
    const userData = ref({
      username: '',
      email: '',
      role: 'employee',
      password: ''
    });

    const fetchUser = async () => {
      if (isEditMode) {
        try {
          const user = await userService.getUser(userId);
          userData.value = { ...user, password: '' };
        } catch (error) {
          console.error('Error loading user:', error);
          router.push('/users');
        }
      }
    };

    const submitForm = async () => {
      try {
        if (isEditMode) {
          await userService.updateUser(userId, userData.value);
        } else {
          await userService.createUser(userData.value);
        }
        router.push('/users');
      } catch (error) {
        console.error('Error saving user:', error);
        alert(t('common.saveError'));
      }
    };

    onMounted(fetchUser);

    return {
      userData,
      isEditMode,
      submitForm
    };
  }
};
</script>

<style scoped>
.container {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
}

.neumorphic-form {
  background: var(--bg-color);
  border-radius: 20px;
  padding: 30px;
  box-shadow: inset 6px 6px 10px rgba(0, 0, 0, 0.1),
              inset -6px -6px 10px rgba(255, 255, 255, 0.7);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

.neumorphic-input {
  width: 100%;
  padding: 12px 15px;
  border: none;
  border-radius: 10px;
  background: var(--bg-color);
  box-shadow: inset 5px 5px 10px rgba(0, 0, 0, 0.1),
              inset -5px -5px 10px rgba(255, 255, 255, 0.7);
}

select.neumorphic-input {
  appearance: none;
}

.hint {
  font-size: 0.9rem;
  color: #777;
  margin-top: 5px;
}

.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 30px;
}

.neumorphic-btn {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 10px;
  background: var(--bg-color);
  box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1),
             -5px -5px 10px rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  text-decoration: none;
}

.neumorphic-btn.primary {
  color: #fff;
  background: #3498db;
  box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.2),
             -5px -5px 10px rgba(255, 255, 255, 0.5);
}

.neumorphic-btn:hover {
  box-shadow: inset 5px 5px 10px rgba(0, 0, 0, 0.1),
              inset -5px -5px 10px rgba(255, 255, 255, 0.7);
}
</style>