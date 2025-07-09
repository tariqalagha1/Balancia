import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import i18n from './i18n'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(i18n)

app.directive('rtl', (el, binding) => {
  el.dir = binding.value ? 'rtl' : 'ltr'
})

app.mount('#app')