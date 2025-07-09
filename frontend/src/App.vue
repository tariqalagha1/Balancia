<template>
  <div v-rtl="isRtl">
    <router-view></router-view>
  </div>
</template>

<script>
import { useI18n } from 'vue-i18n'

export default {
  setup() {
    const { locale } = useI18n()
    return {
      isRtl: locale.value === 'ar'
    }
  }
}
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f0f0f3;
}

.card {
  background: #f0f0f3;
  border-radius: 20px;
  box-shadow: 10px 10px 21px #d3d3d6, 
              -10px -10px 21px #ffffff;
  padding: 20px;
  margin: 15px;
}

.btn {
  background: #f0f0f3;
  border: none;
  border-radius: 12px;
  padding: 12px 24px;
  box-shadow: 5px 5px 10px #d3d3d6, 
              -5px -5px 10px #ffffff;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s ease;
}

.btn:hover {
  box-shadow: inset 5px 5px 10px #d3d3d6, 
              inset -5px -5px 10px #ffffff;
}

.form-control {
  background: #f0f0f3;
  border: none;
  border-radius: 12px;
  padding: 12px 15px;
  box-shadow: inset 5px 5px 10px #d3d3d6, 
              inset -5px -5px 10px #ffffff;
  margin: 10px 0;
  width: 100%;
  box-sizing: border-box;
}

[dir="rtl"] {
  text-align: right;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
</style>