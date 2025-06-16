import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import FomanticUI from 'vue-fomantic-ui'
import 'fomantic-ui-css/semantic.min.css'
import './style.css'

const app = createApp(App)

app.use(router)
app.use(FomanticUI)
app.mount('#app')