import { createApp } from 'vue'
import './style.css' // Import Tailwind CSS output
import App from './App.vue'
import router from './router' // Import the router

createApp(App).use(router).mount('#app')