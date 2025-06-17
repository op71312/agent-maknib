import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Level from '../views/Level.vue'

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
        path: '/level',
        name: 'Level',
        component: Level,
    },
    {
        path: '/game/:difficulty',
        name: 'Game',
        component: () => import('../views/Game.vue'),
        props: true
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
