import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Challenges from '@/components/Challenges'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/challenges',
      name: 'Challenges',
      component: Challenges
    }
  ],
  mode: 'history'
})
