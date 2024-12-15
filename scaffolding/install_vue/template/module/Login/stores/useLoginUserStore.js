import { defineStore } from "pinia";
import { reactive, ref } from "vue";

export const use%module_name%Store = defineStore('%module_name%Store',()=>{
    const userData = reactive({
        firstName: '',
        lastName: '',
        email:''
    })
    const token = ref('')
    const isAuthenticated = ref(false)

    function loginAction(userDataParam){
        token.value = userDataParam.token
        userData.firstName = userDataParam.first_name
        userData.lastName = userDataParam.last_name
        userData.email = userDataParam.email
        localStorage.setItem('userLogin',JSON.stringify(userDataParam))
        isAuthenticated.value = true
        
    }
    
    function logoutAction(){
        token.value = ''
        userData.firstName = ''
        userData.lastName = ''
        localStorage.removeItem('%module_name%')
        isAuthenticated.value = false
    }

    function loadUser(){
        const RetrieveDataUser = JSON.parse(localStorage.getItem('%module_name%'))
        if (RetrieveDataUser){
            isAuthenticated.value = (RetrieveDataUser.token != '')
            if(isAuthenticated.value){
                token.value = RetrieveDataUser.token
                userData.firstName = RetrieveDataUser.first_name
                userData.lastName = RetrieveDataUser.last_name
                userData.email = RetrieveDataUser.email
            }
        }
    }

    return {isAuthenticated, token, userData, loginAction, logoutAction ,loadUser }
})