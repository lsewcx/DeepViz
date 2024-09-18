import { createWebHistory, createRouter, Router, RouteRecordRaw } from 'vue-router'

import conv from '../views/conv.vue'
import index from '../views/index.vue'
import conv3d from '../views/conv3d.vue'
import classification from '../views/classification.vue'

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        component: index,
    },
    {
        path: '/conv/conv2d',
        component: conv,
    },
    {
        path: '/conv/conv3d',
        component: conv3d
    },
    {
        path: '/classification',
        component: classification
    }
]

const router: Router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router