import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import './style.css'
import App from './App.vue'
import {createPinia} from "pinia"
import router from './router/index'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
const app = createApp(App);
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
app.use(ElementPlus, {
  locale: zhCn,
})
app.use(createPinia());
app.use(router);
app.mount('#app');
