import { createRouter, createWebHistory } from 'vue-router'

import Login from '@/views/Login.vue'
import Logout from '@/views/Logout.vue'
import Main from '@/views/Main.vue'
import ResultsShow from '@/views/ResultsShow.vue'
import Setting from '@/views/Setting.vue'
import History from '@/views/History.vue'
import Layout from '@/layout/layout.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/login',
            name: 'Login',
            component: Login
        },
        {
            path: '/logout',
            name: 'Logout',
            component: Logout
        },
        {
            path: '/',
            component: Layout,
            children: [
                {
                    path: '',
                    name: 'Main',
                    component: Main
                },
                {
                    path: '/resultsShow',
                    name: 'ResultsShow',
                    component: ResultsShow
                },
                {
                    path: '/settings',
                    name: 'Settings',
                    component: Setting
                },
                {
                    path: '/history',
                    name: 'History',
                    component: History
                }
            ]
        }
    ]
})

export default router