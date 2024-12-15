import LoginUser from '@/module/loginUser/views/%module_name%.vue'
import PasswordRecovery from '@/module/loginUser/views/PasswordRecovery.vue'
import SigninUser from '@/module/loginUser/views/SigninUser.vue'


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