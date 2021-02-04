import Vue from 'vue'
import App from './App.vue'

// Installing whole package
import CoreuiVue from '@coreui/vue';
Vue.use(CoreuiVue);

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
