import { createApp } from 'vue'

import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'

import axios from "axios";
import VueAxios from "vue-axios";
axios.defaults.baseURL = "/api";

import ElementPlus  from 'element-plus'
import 'element-plus/dist/index.css'

import naive from 'naive-ui'

// const naive = create({
//     components: [NButton]
// })

const app = createApp(App)
app.use(router)
app.use(naive)
app.use(VueAxios, axios)
app.config.globalProperties.$axios = axios
app.use(ElementPlus )
app.mount('#app')
