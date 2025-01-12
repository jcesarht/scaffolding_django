import Dashboard from "./views/Dashboard.vue";

const routesDashboard = [
    {
        path: '/dashboard',
        component: Dashboard,
        name: 'dashboard',
        meta: {requiresAuth: true}
    }
]

export default routesDashboard