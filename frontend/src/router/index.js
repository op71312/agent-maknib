import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routerHistory = createWebHistory()

const routes = [
    {
        path: '/',
        redirect: '/home',
    },
    {
        path: '/home',
        name: 'Home',
        component: Home,
    },
    {
        path: '/:catchAll(.*)',
        redirect: '/home',
    }
]

const router = createRouter({
    history: routerHistory,
    routes: routes,
})

export default router;
