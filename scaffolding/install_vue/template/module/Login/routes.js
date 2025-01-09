import %module_name% from '@/module/%module_name%/views/%module_name%.vue'
import PasswordRecovery from '@/module/%module_name%/views/PasswordRecovery.vue'
import SigninUser from '@/module/%module_name%/views/SigninUser.vue'


const routesLoginUser = [
    {
        path: '/',
        component: %module_name%,
        name: 'home'
    },
    {
        path: '/login',
        component: %module_name%,
        name: 'login'
    },
    {
        path:'/password_recovery',
        component: PasswordRecovery,
        name: 'password_recovery',
    },
    { 
        path:'/signin',
        component: SigninUser,
        name: 'signin'
    },
]

export default routesLoginUser