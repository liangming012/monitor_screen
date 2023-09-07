import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  optimizeDeps: {
    include: ['element-plus/lib/locale/lang/zh-cn'],
  },
  server:{
    host: '0.0.0.0'
  }
})
