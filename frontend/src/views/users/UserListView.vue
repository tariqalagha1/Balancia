<template>
  <div class="container">
    <h1>{{ $t('users.title') }}</h1>
    
    <div class="actions">
      <router-link to="/users/create" class="neumorphic-btn">
        {{ $t('common.create') }}
      </router-link>
    </div>

    <table class="neumorphic-table">
      <thead>
        <tr>
          <th>{{ $t('users.id') }}</th>
          <th>{{ $t('users.username') }}</th>
          <th>{{ $t('users.email') }}</th>
          <th>{{ $t('users.role') }}</th>
          <th>{{ $t('common.actions') }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ $t(`roles.${user.role}`) }}</td>
          <td>
            <router-link :to="`/users/edit/${user.id}`" class="neumorphic-btn small">
              {{ $t('common.edit') }}
            </router-link>
            <button @click="deleteUser(user.id)" class="neumorphic-btn small danger">
              {{ $t('common.delete') }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import userService from '@/services/userService';

export default {
  setup() {
    const { t } = useI18n();
    const users = ref([]);

    const fetchUsers = async () => {
      try {
        users.value = await userService.getAllUsers();
      } catch (error) {
        console.error('Error loading users:', error);
      }
    };

    const deleteUser = async (userId) => {
      if (confirm(t('users.confirmDelete'))) {
        try {
          await userService.deleteUser(userId);
          users.value = users.value.filter(u => u.id !== userId);
        } catch (error) {
          console.error('Error deleting user:', error);
        }
      }
    };

    onMounted(fetchUsers);

    return {
      users,
      deleteUser
    };
  }
};
</script>

<style scoped>
.container {
  padding: 20px;
}

.actions {
  margin-bottom: 20px;
  text-align: right;
}

.neumorphic-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: var(--bg-color);
  border-radius: 15px;
  box-shadow: inset 6px 6px 10px rgba(0, 0, 0, 0.1),
              inset -6px -6px 10px rgba(255, 255, 255, 0.7);
}

.neumorphic-table th,
.neumorphic-table td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.neumorphic-table th {
  font-weight: bold;
  background: rgba(0, 0, 0, 0.02);
}

.neumorphic-table tr:last-child td {
  border-bottom: none;
}

.neumorphic-btn {
  display: inline-block;
  padding: 8px 15px;
  margin: 0 5px;
  border: none;
  border-radius: 10px;
  background: var(--bg-color);
  box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1),
             -5px -5px 10px rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.3s ease;
}

.neumorphic-btn.small {
  padding: 5px 10px;
  font-size: 0.9rem;
}

.neumorphic-btn:hover {
  box-shadow: inset 5px 5px 10px rgba(0, 0, 0, 0.1),
              inset -5px -5px 10px rgba(255, 255, 255, 0.7);
}

.neumorphic-btn.danger {
  color: #ff4757;
}
</style>