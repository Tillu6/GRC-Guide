// frontend/src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import tilt from './directives/tilt'
// Import global CSS (e.g., Tailwind base styles). 
// Ensure style.css or Tailwind directives are set up correctly.
import './style.css'

// Create and mount the app
const app = createApp(App)
app.directive('tilt', tilt)
app.use(router)
app.mount('#app')
