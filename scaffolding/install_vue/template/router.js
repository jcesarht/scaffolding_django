import {createRouter, createWebHistory } from 'vue-router'
import PageNotFound from '@/views/PageNotFound.vue'
import routesDashboard from '@/module/Dashboard/routes'

const routes = [
    ...routesDashboard,
    {
        path: '/:catchAll(.*)',
        component: PageNotFound, 
        name: 'page_not_found'
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach( (to, from, next) => {
    const store = useLoginUserStore()
    const {loadUser} = store
    loadUser()
    const {isAuthenticated} = store
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
    if( requiresAuth && !isAuthenticated){
        next('/page_not_found')
    }else{
        next()
    }
})

export default router