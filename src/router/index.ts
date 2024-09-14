import { createMemoryHistory, createRouter, Router, RouteRecordRaw } from 'vue-router'

import conv from '../views/conv.vue'
import index from '../views/index.vue'

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        component: index,
    },
    {
        path: '/conv',
        component: conv,
    }
]

const router: Router = createRouter({
    history: createMemoryHistory(),
    routes,
})

export default router