import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],       // <-- register Vue plugin
  server: {
    host: true,           // bind to 0.0.0.0 so Docker and external connections work
    port: 5173,
    // proxy: { '/api': 'http://localhost:8000' } if needed
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
})
