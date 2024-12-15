<template>
    <div class="bg-gradient-to-b from-blue-200 h-dvh w-dvw flex items-center justify-center">
        <div class="w-11/12 sm:w-5/12 lg:w-4/12 items-center py-10 px-3 sm:px-6 mt-10 sm:mt-9">
            <div class="w-full mb-2 px-1" tabindex="0" ref="informationSignin">
                <h1>Became an User</h1>
            </div>
            <div class="w-full mb-2">
                <base-info-sign :typeInfo="typeInfo" v-show="showSign">
                    {{ bannerMessage }}  
                </base-info-sign>
            </div>
            <form novalidate @submit.prevent="checkSigninForm()" ref="registerForm">
                <UIInputText 
                    name="first_name"
                    placeholder="First Name"
                    required="true"
                    ref="firstNameInput"
                />
                <UIInputText 
                    name="last_name"
                    placeholder="Last Name"
                    ref="lastNameInput"
                />
                <UIInputText 
                    name="login"
                    placeholder="Username"
                    required="true"
                    ref="usernameInput"
                />
                <UIInputText 
                    name="email"
                    placeholder="Email"
                    required="true"
                    ref="emailInput"
                    rule="email"
                />
                <UIInputPassword
                    name="password"
                    placeholder="Password"
                    required="true"
                    minChar=4
                    ref="passwordInput"
                />
                <UIInputPassword
                    name="repeat_password"
                    placeholder="Repeat Password"
                    required="true"
                    minChar=4
                    ref="repeatPasswordInput"
                />
                <UIButton 
                    textButton="Register"
                    ref="buttonLogin"
                    :disable="disableButton"
                />
            </form>
            <div class="w-full mt-8 px-1">
                <div class="float float-left">
                    <router-link :to="{name: 'login' }">Back to Login</router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref } from 'vue';
    import UIInputText from '@/components/UIComponents/UIInputText.vue';
    import UIInputPassword from '@/components/UIComponents/UIInputPassword.vue';
    import UIButton from '@/components/UIComponents/UIButton.vue';
    import baseInfoSign from '@/components/base/baseInfoSign.vue';
    import { useOverlay } from '@/stores/useOverlay';
    import { useSignin } from '../composables/%module_name%';

    //reference compomenent
    const buttonLogin = ref(null)
    const firstNameInput = ref(null)
    const lastNameInput = ref(null)
    const usernameInput = ref(null)
    const emailInput = ref(null)
    const passwordInput = ref(null)
    const repeatPasswordInput = ref(null)
    const showSign = ref(false)
    const bannerMessage = ref("")
    const disableButton = ref(false)
    const registerForm = ref(false)
    const informationSignin = ref(null)
    const typeInfo = ref('alert')
    // overlay
    const overlay = useOverlay()
    const {showOverlay, hiddenOverlay} = overlay
    
    let signinRequest = null

    const checkSigninForm = async ()=>{
        showOverlay()
        resetErroSign()
        if(!disableButton.value){
            disableButton.value = true
            if(!validateErrorsComponents()){
                if (passwordInput.value.valueInput() != repeatPasswordInput.value.valueInput()){
                    showSign.value = true
                    bannerMessage.value = "Passwords do not match. Please check and try again."
                    informationSignin.value.focus()
                }else{
                    let infoMessage = ""
                    const dataUser = {
                        'first_name': firstNameInput.value.valueInput(),
                        'last_name': lastNameInput.value.valueInput(),
                        'username': usernameInput.value.valueInput(),
                        'password': passwordInput.value.valueInput(),
                        'email': emailInput.value.valueInput(),
                    }
                    signinRequest = await useSignin(dataUser);
                    if (!signinRequest.error){
                        typeInfo.value = 'success'
                        infoMessage = "You have successfully registered."
                        showSign.value = true
                        bannerMessage.value = infoMessage
                        resetForm();
                        informationSignin.value.focus()
                    }else{
                        typeInfo.value = 'alert'
                        showSign.value = signinRequest.response.error
                        bannerMessage.value = signinRequest.response.message
                        informationSignin.value.focus()
                    }
                }
            }
        }
        hiddenOverlay()
        disableButton.value = false
    }

    //Verify all component and return if some component have an error
    const validateErrorsComponents = ()=>{
        let validateError = false
        const uiComponents = [
            firstNameInput,
            lastNameInput,
            usernameInput,
            emailInput,
            passwordInput,
            repeatPasswordInput,
        ]

        validateError = uiComponents.find(component => component.value.checkValidateError())
        return validateError
    }

    //reset form
    const resetForm = () =>{
        registerForm.value.reset();
    }

    // reset the error sign
    const resetErroSign = ()=>{
        showSign.value = false
        bannerMessage.value = ""
    }

</script>

<style lang="scss" scoped>

</style>