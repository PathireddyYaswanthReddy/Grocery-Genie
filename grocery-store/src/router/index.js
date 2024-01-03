import { createRouter, createWebHistory } from 'vue-router'
import SignUp from '../components/Signup.vue'
import Login from '../components/Login.vue'
import UserHome from '../components/UserHome.vue'
import Account from '../components/Account.vue'
import Admin from '../components/Admin.vue'
import Storemanager from '../components/Storemanager.vue'

const guard = function(to,from,next){
  if(localStorage.getItem('token'))
  {
    next()
  }
  else{
    next('/login')
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/UserHome',
      name: 'UserHome',
      component: UserHome,
      beforeEnter : (to,from,next) => {
        guard(to,from,next)
      }
    },

    {
      path: '/Admin',
      name: 'Admin',
      component: Admin,
      beforeEnter : (to,from,next) => {
        guard(to,from,next)
      }
    },

    {
      path: '/Storemanager',
      name: 'Storemanager',
      component: Storemanager,
      beforeEnter : (to,from,next) => {
        guard(to,from,next)
      }
    },

    {
      path: '/SignUp',
      name: 'SignUp',
      component: SignUp
    },

    {
      path: '/Login',
      name: 'Login',
      component: Login
    },

    {
      path: '/MyAccount',
      name : 'MyAccount',
      component: Account
    }

  ]
})

export default router
