<template>
    <div class="bg-gradient-to-b from-blue-200 h-dvh w-dvw flex items-center justify-center">
        <div class="w-11/12 sm:w-5/12 lg:w-4/12 items-center py-10 px-3 sm:px-6 mt-10 sm:mt-9">
            <div class="w-full mb-2">
                <base-info-sign typeInfo="alert" v-show="showSign">
                    {{ infoMessage }}  
                </base-info-sign>
            </div>
            <form novalidate @submit.prevent="checkLoginForm()">
                <UIInputText 
                    name="login"
                    placeholder="Username"
                    required="true"
                    ref="inputUser"
                />
                <UIInputPassword
                    name="password"
                    placeholder="Password"
                    required="true"
                    minChar=4
                    ref="inputPassword"
                />
                <UIButton 
                    textButton="Login"
                    ref="buttonLogin"
                    :disable="disableButton"
                />
            </form>
            <div class="flex justify-center mt-9">
                <img src="@/assets/vue.svg" alt="logo" />
            </div>
            <div class="w-full mt-8 px-1">
                <div class="float float-left">
                    <router-link :to="{name: 'password_recovery' }">Forget password?</router-link>
                </div>
                <div class="float float-right">
                    <router-link :to="{name: 'signin' }">Create an account</router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';
    import UIInputText from '@/components/UIComponents/UIInputText.vue';
    import UIInputPassword from '@/components/UIComponents/UIInputPassword.vue';
    import UIButton from '@/components/UIComponents/UIButton.vue';
    import baseInfoSign from '@/components/base/baseInfoSign.vue';
    import { useLogin } from '../composables/%module_name%';
    import { useLoginUserStore } from '../stores/use%module_name%Store';
    import { useOverlay } from '@/stores/useOverlay';

    const router = useRouter()

    const showSign = ref(false)
    const infoMessage = ref(false)
    const disableButton = ref(false)
    const inputUser = ref(null)
    const inputPassword = ref(null)
    const buttonLogin = ref(null)
    const store = useLoginUserStore()
    const overlay = useOverlay()

    const { loginAction }  = store
    const { showOverlay, hiddenOverlay } = overlay
    let loginRequest = null

    const checkLoginForm = async ()=>{
        if(!disableButton.value){
            showSign.value = false
            infoMessage.value = ''
            disableButton.value = true

            if (
                !inputUser.value.checkValidateError()
                && !inputPassword.value.checkValidateError()
            ){
                showOverlay()
                loginRequest = await useLogin(inputUser.value.valueInput(),inputPassword.value.valueInput())
                if (!loginRequest.error){
                    const dataUser = loginRequest.response.data
                    loginAction(dataUser) //save in the store
                    router.push({name: 'dashboard'})
                }else{
                    showSign.value = loginRequest.response.error
                    infoMessage.value = loginRequest.response.message
                }
            }
            hiddenOverlay()
            disableButton.value = false       
        }
    }

</script>

<style lang="scss" scoped>
</style>